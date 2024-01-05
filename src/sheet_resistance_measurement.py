from PySide2 import QtCore

from hardware import KeithleySource, KeithleyMultimeter

from tests.tests import MockKeithleySource, MockKeithleyMultimeter

import core_functions as cf

import time
import datetime as dt
import pandas as pd
import numpy as np
import os
from pathlib import Path


class SheetResistanceMeasurement(QtCore.QThread):
    """
    QThread that shall do all the work for the current tester in the setup tab.
    It is mainly needed for updating the current reading. However, I figure
    at the moment, that it is probably also good to have the other current
    tester functionalities in this class. Mainly because it does not make
    sense to return a current reading while the keithley has to be resetted,
    for instance. So it is not only okay but kind of demanded to have this in
    a single thread.
    """

    # Define costum signals
    # https://stackoverflow.com/questions/36434706/pyqt-proper-use-of-emit-and-pyqtsignal
    # With pyside2 https://wiki.qt.io/Qt_for_Python_Signals_and_Slots
    update_all_labels_signal = QtCore.Signal(float, float, float, float, float)
    update_progress_bar = QtCore.Signal(str, float)
    hide_progress_bar = QtCore.Signal()

    def __init__(
        self,
        keithley_multimeter,
        keithley_source,
        global_parameters,
        measurement_parameters,
        parent=None,
    ):

        super(SheetResistanceMeasurement, self).__init__()

        self.is_killed = False

        # Reset Arduino and Keithley
        self.keithley_multimeter = keithley_multimeter
        self.keithley_source = keithley_source

        self.keithley_source.as_current_source(100)
        self.keithley_source.set_current(global_parameters["applied_current"])

        self.global_parameters = global_parameters
        self.measurement_parameters = measurement_parameters
        self.current_tester = parent.current_tester

        # Connect signal to the updater from the parent class
        self.update_all_labels_signal.connect(parent.update_all_labels)
        self.update_progress_bar.connect(parent.progressBar.setProperty)
        self.hide_progress_bar.connect(parent.progressBar.hide)

        self.parent = parent

        # Define dataframe
        self.df_data = pd.DataFrame(
            columns=[
                "applied_current",
                "measured_voltage",
                "sheet_resistance",
                "resistivity",
                "conductivity",
            ]
        )

    def run(self):
        """
        Class that runs the measurement
        """
        import pydevd

        pydevd.settrace(suspend=False)

        self.keithley_source.activate_output()
        time.sleep(2)
        self.keithley_source.read_current()
        self.keithley_multimeter.measure_voltage()
        # The finite width correction has to be done based on empirical
        # values (for rectangular shaped samples). Those can be found in
        # a separate file.
        if self.measurement_parameters["sample_geometry"] == "rectangular":
            finite_thickness_correction = np.log(2) / np.log(
                np.sinh(
                    self.measurement_parameters["thickness"]
                    * 1e-6
                    / self.global_parameters["probe_spacing"]
                )
                / np.sinh(
                    self.measurement_parameters["thickness"]
                    * 1e-6
                    / (2 * self.global_parameters["probe_spacing"])
                )
            )
            correction_factors_file_path = os.path.join(
                Path(__file__).parent.parent,
                "usr",
                "rectangular_correction_factors.csv",
            )
            correction_factors = pd.read_csv(
                correction_factors_file_path,
                delimiter="\t",
                skiprows=1,
                index_col=False,
            )
            width_probe_spacing_ratio = (
                self.measurement_parameters["short_side"]
                / self.global_parameters["probe_spacing"]
            )
            length_width_ratio = (
                self.measurement_parameters["long_side"]
                / self.measurement_parameters["short_side"]
            )
            closest_width_probe_spacing = correction_factors[
                correction_factors["width_probe_spacing"]
                == correction_factors.iloc[
                    correction_factors["width_probe_spacing"]
                    .sub(width_probe_spacing_ratio)
                    .abs()
                    .argmin()
                ]["width_probe_spacing"]
            ]

            finite_width_correction = closest_width_probe_spacing.iloc[
                closest_width_probe_spacing["length_width"]
                .sub(length_width_ratio)
                .abs()
                .argmin()
            ]["correction_factor"]

        for i in range(int(self.measurement_parameters["no_of_averages"])):
            # Read current and voltage
            current_reading = max(self.keithley_source.read_current(), 1e-12)
            voltage_reading = self.keithley_multimeter.measure_voltage()

            self.df_data.loc[i, "applied_current"] = current_reading
            self.df_data.loc[i, "measured_voltage"] = voltage_reading

            # Check the shape of the sample
            if self.measurement_parameters["sample_geometry"] == "rectangular":
                # Actual Calculation
                # For the thickness a conversion to cm is needed (10-7) to get the units right
                resistivity = (
                    4.53236
                    * (self.measurement_parameters["thickness"] * 1e-7)
                    * voltage_reading
                    / current_reading
                    * finite_thickness_correction
                    * finite_width_correction
                )

                sheet_resistance = resistivity / (
                    self.measurement_parameters["thickness"] * 1e-7
                )
                conductivity = 1 / resistivity

                self.df_data.loc[i, "sheet_resistance"] = sheet_resistance
                self.df_data.loc[i, "resistivity"] = resistivity
                self.df_data.loc[i, "conductivity"] = conductivity
            else:
                cf.log_message(
                    "The software does not yet work for non-rectangularily shaped samples."
                )
                return

            # Update Signals
            self.update_all_labels_signal.emit(
                self.df_data["applied_current"].mean(),
                self.df_data["measured_voltage"].mean(),
                self.df_data["sheet_resistance"].mean(),
                self.df_data["resistivity"].mean(),
                self.df_data["conductivity"].mean(),
            )

            if self.is_killed:
                cf.log_message("Measurement aborted.")
                self.hide_progress_bar.emit()
                self.current_tester.pause = False
                self.quit()
                return

            self.update_progress_bar.emit(
                "value", int(i / self.measurement_parameters["no_of_averages"] * 100)
            )

            time.sleep(float(1 / self.global_parameters["measurement_interval"]))

        self.save_data()
        self.hide_progress_bar.emit()
        self.current_tester.pause = False
        self.parent.sw_start_measurement_pushButton.setChecked(False)
        self.keithley_source.deactivate_output()

    def save_data(self):
        """
        Function to save the measured data to file. This should probably be
        integrated into the AutotubeMeasurement class
        """
        # Define Header
        line03 = (
            "Sample length: "
            + str(self.measurement_parameters["long_side"])
            + " mm\t"
            + "Sample width: "
            + str(self.measurement_parameters["short_side"])
            + " mm\t"
            + "Sample thickness: "
            + str(self.measurement_parameters["thickness"])
            + " nm"
        )
        line04 = (
            "Applied Current: "
            + str(self.global_parameters["applied_current"])
            + " mA\t"
            + "Measurements per Second: "
            + str(self.global_parameters["measurement_interval"])
            + "\tNumber of Averages: "
            + str(self.measurement_parameters["no_of_averages"])
        )
        line05 = (
            "Average Current: ("
            + str(round(self.df_data["applied_current"].mean(), 2))
            + " +- "
            + str(round(self.df_data["applied_current"].std(), 2))
            + ") mA\t"
            + "Average Voltage: ("
            + str(round(self.df_data["measured_voltage"].mean(), 4))
            + " +- "
            + str(round(self.df_data["measured_voltage"].std(), 4))
            + ") V\t"
        )
        line06 = (
            "Average Sheet Resistance: ("
            + str(round(self.df_data["sheet_resistance"].mean(), 4))
            + " +- "
            + str(round(self.df_data["sheet_resistance"].std(), 4))
            + ") Ohm/sq\t"
            + "Average Resistivity: ("
            + str(round(self.df_data["resistivity"].mean(), 4))
            + " +- "
            + str(round(self.df_data["resistivity"].std(), 4))
            + ") Ohm cm\t"
            + "Average Conductivity: ("
            + str(round(self.df_data["conductivity"].mean(), 4))
            + " +- "
            + str(round(self.df_data["conductivity"].std(), 4))
            + ") S/cm"
        )

        line07 = "### Measurement data ###"
        line08 = "Applied Current\t Measured Voltage\t Sheet resistivity\t Resisitivity\t Conductivity"
        line09 = "mA\t V\t Ohm/sq\t Ohm cm\t S/cm\n"

        header_lines = [
            line03,
            line04,
            line05,
            line06,
            line07,
            line08,
            line09,
        ]

        # Write header lines to file
        file_path = (
            self.measurement_parameters["folder_path"]
            + dt.date.today().strftime("%Y-%m-%d_")
            + self.measurement_parameters["batch_name"]
            + "_d"
            + str(self.measurement_parameters["device_number"])
            + "_res"
            + ".csv"
        )

        # Convert to mA
        self.df_data["applied_current"] = self.df_data["applied_current"] * 1000

        # Format the dataframe for saving (no. of digits)
        self.df_data["applied_current"] = self.df_data["applied_current"].map(
            lambda x: "{0:.2f}".format(x)
        )
        self.df_data["measured_voltage"] = self.df_data["measured_voltage"].map(
            lambda x: "{0:.6f}".format(x)
        )
        self.df_data["sheet_resistance"] = self.df_data["sheet_resistance"].map(
            lambda x: "{0:.1f}".format(x)
        )
        self.df_data["resistivity"] = self.df_data["resistivity"].map(
            lambda x: "{0:.6f}".format(x)
        )
        self.df_data["conductivity"] = self.df_data["conductivity"].map(
            lambda x: "{0:.6f}".format(x)
        )

        # Save file
        cf.save_file(self.df_data, file_path, header_lines)

    def kill(self):
        """
        Kill this thread by stopping the loop
        """
        # Turn keithley off
        self.keithley_source.deactivate_output()

        # Trigger interruption of run sequence
        self.is_killed = True
