from UI_main_window import Ui_MainWindow
from settings import Settings

from current_tester import CurrentTester
from loading_window import LoadingWindow
from sheet_resistance_measurement import SheetResistanceMeasurement

from hardware import (
    KeithleyMultimeter,
    KeithleySource,
)

import core_functions as cf
import pyvisa

from PySide2 import QtCore, QtGui, QtWidgets

import time
import os
import json
import sys
import functools
from pathlib import Path
from datetime import date
import logging
from logging.handlers import RotatingFileHandler

import matplotlib.pylab as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import math

import webbrowser


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    This class contains the logic of the program and is explicitly seperated
    from the UI classes. However, it is a child class of Ui_MainWindow.
    """

    def __init__(self):
        """
        Initialise instance
        """
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # For some odd reason this is necessary in the main thread already.
        # Otherwise the motor won't initialise and the program crash without an error...
        # try:
        #     global_settings = cf.read_global_settings()
        #     ThorlabMotor(
        #         global_settings["motor_number"], global_settings["motor_offset"]
        #     )
        # except:
        #     cf.log_message(
        #         "Motor can probably not be initialised. Reconnect the motor or change the serial number in the global settings."
        #     )

        # -------------------------------------------------------------------- #
        # -------------------------- Hardware Setup -------------------------- #
        # -------------------------------------------------------------------- #
        # self.motor_run = MotorMoveThread(0, 0, False, self)

        # Execute initialisation thread
        loading_window = LoadingWindow(self)

        # Execute loading dialog
        loading_window.exec()

        # # Update the graphics to the current motor position
        # motor_position = self.motor.read_position()
        # self.gw_animation.move(motor_position)

        # Read global settings first (what if they are not correct yet?)
        # global_settings = cf.read_global_settings()

        # -------------------------------------------------------------------- #
        # ------------------------------ General ----------------------------- #
        # -------------------------------------------------------------------- #

        # Update statusbar
        cf.log_message("Initialising Program")
        self.tabWidget.currentChanged.connect(self.changed_tab_widget)

        # Hide by default and only show if a process is running
        self.progressBar.hide()

        # -------------------------------------------------------------------- #
        # ------------------------- Default Values --------------------------- #
        # -------------------------------------------------------------------- #

        # Automatically overwrite the overwrite values with the defaults when
        # the program is started to ensure that defaults are defaults by default
        default_settings = cf.read_global_settings(default=True)
        settings_data = {}
        settings_data["overwrite"] = []
        settings_data["overwrite"] = default_settings
        settings_data["default"] = []
        settings_data["default"] = default_settings

        # Save the entire thing again to the settings.json file
        with open(
            os.path.join(Path(__file__).parent.parent, "usr", "global_settings.json"),
            "w",
        ) as json_file:
            json.dump(settings_data, json_file, indent=4)

        cf.log_message("Overwrite Settings set to Default")

        # -------------------------------------------------------------------- #
        # ------------------------ Sheet Resistance -------------------------- #
        # -------------------------------------------------------------------- #

        # First init of current tester (should be activated when starting the
        # program)
        self.current_tester = CurrentTester(
            self.keithley_multimeter,
            self.keithley_source,
            parent=self,
        )

        # Start thread
        self.current_tester.start()

        # Connect buttons
        self.sw_browse_pushButton.clicked.connect(self.browse_folder)
        self.sw_activate_output_pushButton.clicked.connect(self.activate_output)
        self.sw_start_measurement_pushButton.clicked.connect(self.start_measurement)

        # Connect toggle switches
        # self.sw_nip_toggleSwitch.clicked.connect(self.reverse_all_voltages)

        # Connect voltage combo box
        # self.sw_ct_voltage_spinBox.valueChanged.connect(
        #     functools.partial(self.voltage_changed, "sw")
        # )

        # -------------------------------------------------------------------- #
        # --------------------------- Menubar -------------------------------- #
        # -------------------------------------------------------------------- #
        self.actionOptions.triggered.connect(self.show_settings)

        # Open the documentation in the browser (maybe in the future directly
        # open the readme file in the folder but currently this is so much
        # easier and prettier)
        self.actionDocumentation.triggered.connect(
            lambda: webbrowser.open(
                "https://github.com/GatherLab/OLED-jvl-measurement/blob/main/README.md"
            )
        )

        self.actionOpen_Log.triggered.connect(lambda: self.open_file("log.out"))

        # -------------------------------------------------------------------- #
        # --------------------- Set Standard Parameters ---------------------- #
        # -------------------------------------------------------------------- #
        # Load correction factors
        correction_factors_file_path = os.path.join(
            Path(__file__).parent.parent,
            "usr",
            "correction_factors.csv",
        )

        correction_factors = pd.read_csv(
            correction_factors_file_path,
            delimiter="\t",
            skiprows=1,
            index_col=False,
        )

        self.sw_activate_output_pushButton.setCheckable(True)
        self.sw_start_measurement_pushButton.setCheckable(True)

        # Sample Geometry
        for shape in correction_factors["shape"].unique():
            self.sw_select_sample_geometry_ComboBox.addItem(shape)

        # Long Side length
        self.sw_long_side_length_spinBox.setMinimum(0)
        self.sw_long_side_length_spinBox.setMaximum(1000)
        self.sw_long_side_length_spinBox.setSingleStep(0.1)
        self.sw_long_side_length_spinBox.setValue(24)
        self.sw_long_side_length_spinBox.setKeyboardTracking(False)

        # Short Side Length
        self.sw_short_side_length_spinBox.setMinimum(0)
        self.sw_short_side_length_spinBox.setMaximum(1000)
        self.sw_short_side_length_spinBox.setSingleStep(0.1)
        self.sw_short_side_length_spinBox.setValue(2)
        self.sw_short_side_length_spinBox.setKeyboardTracking(False)

        # Short Side Length
        self.sw_thickness_spinBox.setMinimum(0)
        self.sw_thickness_spinBox.setMaximum(1000000)
        self.sw_thickness_spinBox.setSingleStep(0.1)
        self.sw_thickness_spinBox.setValue(90)
        self.sw_thickness_spinBox.setKeyboardTracking(False)

        # No of averages
        self.sw_no_of_averages_spinBox.setMinimum(1)
        self.sw_no_of_averages_spinBox.setMaximum(1000000)
        self.sw_no_of_averages_spinBox.setSingleStep(1)
        self.sw_no_of_averages_spinBox.setValue(20)
        self.sw_no_of_averages_spinBox.setKeyboardTracking(False)

        # Update statusbar
        cf.log_message("Program ready")

    # -------------------------------------------------------------------- #
    # ------------------------- Global Functions ------------------------- #
    # -------------------------------------------------------------------- #
    def browse_folder(self):
        """
        Open file dialog to browse through directories
        """
        global_variables = cf.read_global_settings()

        self.global_path = QtWidgets.QFileDialog.getExistingDirectory(
            QtWidgets.QFileDialog(),
            "Select a Folder",
            global_variables["default_saving_path"],
            QtWidgets.QFileDialog.ShowDirsOnly,
        )
        print(self.global_path)
        # file_dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)

        # if file_dialog1.exec():
        #     # Set global path to selected path
        #     self.global_path = file_dialog1.selectedFiles()

        #     # Set the according line edit
        self.sw_folder_path_lineEdit.setText(self.global_path + "/")

    def show_settings(self):
        """
        Shows the settings
        """
        self.settings_window = Settings(self)
        # ui = Ui_Settings()
        # ui.setupUi(self.settings_window, parent=self)

        p = (
            self.frameGeometry().center()
            - QtCore.QRect(QtCore.QPoint(), self.settings_window.sizeHint()).center()
        )

        self.settings_window.move(p)

        # self.settings_window.show()

        result = self.settings_window.exec()

    @QtCore.Slot(KeithleySource)
    def init_source(self, source_object):
        """
        Receives a source object from the init thread
        """
        self.keithley_source = source_object

    @QtCore.Slot(KeithleyMultimeter)
    def init_multimeter(self, multimeter_object):
        """
        Receives a multimeter object from the init thread
        """
        self.keithley_multimeter = multimeter_object

    def open_file(self, path):
        """
        Opens a file on the machine with the standard program
        https://stackoverflow.com/questions/6045679/open-file-with-pyqt
        """
        if sys.platform.startswith("linux"):
            subprocess.call(["xdg-open", path])
        else:
            os.startfile(path)

    def changed_tab_widget(self):
        """
        Function that shall manage the threads that are running when we are
        on a certain tab. For instance the spectrum thread really only must
        run when the user is on the spectrum tab. Otherwise it can be paused.
        This might become important in the future.
        """

        cf.log_message(
            "Switched to tab widget no. " + str(self.tabWidget.currentIndex())
        )

        return

    def safe_read_setup_parameters(self):
        """
        Read setup parameters and if any important field is missing, return a qmessagebox
        """

        # Read out measurement and setup parameters from GUI
        setup_parameters = self.read_setup_parameters()

        # Check if folder path exists
        if (
            setup_parameters["folder_path"] == ""
            or setup_parameters["batch_name"] == ""
        ):
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Please set folder path and batch name first!")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setStyleSheet(
                "background-color: rgb(44, 49, 60);\n"
                "color: rgb(255, 255, 255);\n"
                'font: 63 bold 10pt "Segoe UI";\n'
                ""
            )
            msgBox.exec()

            self.sw_start_measurement_pushButton.setChecked(False)

            cf.log_message("Folder path or batchname not defined")
            raise UserWarning("Please set folder path and batchname first!")

        # Now check if the folder path ends on a / otherwise try to add it
        if not setup_parameters["folder_path"][-1] == "/":
            setup_parameters["folder_path"] = setup_parameters["folder_path"] + "/"
            self.sw_folder_path_lineEdit.setText(setup_parameters["folder_path"])

        # Now check if the read out path is a valid path
        if not os.path.isdir(setup_parameters["folder_path"]):
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Please enter a valid folder path")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setStyleSheet(
                "background-color: rgb(44, 49, 60);\n"
                "color: rgb(255, 255, 255);\n"
                'font: 63 bold 10pt "Segoe UI";\n'
                ""
            )
            msgBox.exec()

            self.sw_start_measurement_pushButton.setChecked(False)

            cf.log_message("Folder path not valid")
            raise UserWarning("Please enter a valid folder path!")

        return setup_parameters

    def make_format(self, current, other):
        """
        function to allow display of both coordinates for figures with two axis
        """

        # current and other are axes
        def format_coord(x, y):
            # x, y are data coordinates
            # convert to display coords
            display_coord = current.transData.transform((x, y))
            inv = other.transData.inverted()
            # convert back to data coords with respect to ax
            ax_coord = inv.transform(display_coord)
            coords = [ax_coord, (x, y)]
            return "Left: {:<40}    Right: {:<}".format(
                *["({:.3f}, {:.3f})".format(x, y) for x, y in coords]
            )

        return format_coord

    # -------------------------------------------------------------------- #
    # -------------------------- Current Tester -------------------------- #
    # -------------------------------------------------------------------- #
    def read_setup_parameters(self):
        """
        Function to read out the current fields entered in the setup tab
        """
        setup_parameters = {
            "folder_path": self.sw_folder_path_lineEdit.text(),
            "batch_name": self.sw_batch_name_lineEdit.text(),
            "device_number": self.sw_device_number_spinBox.value(),
            "sample_geometry": self.sw_select_sample_geometry_ComboBox.currentText(),
            "long_side": self.sw_long_side_length_spinBox.value(),
            "short_side": self.sw_short_side_length_spinBox.value(),
            "thickness": self.sw_thickness_spinBox.value(),
            "no_of_averages": self.sw_no_of_averages_spinBox.value(),
        }

        # Update statusbar
        cf.log_message("Setup parameters read")

        return setup_parameters

    def start_measurement(self):
        """
        Start Measurement
        """
        # If the measurement was already started and the button is clicked
        # again, stop the measurement
        if not self.sw_start_measurement_pushButton.isChecked():
            self.sheet_resistance_measurement.is_killed = True
            return

        # Save read setup parameters
        setup_parameters = self.safe_read_setup_parameters()
        # setup_parameters = self.read_setup_parameters()

        # Read global parameters
        global_settings = cf.read_global_settings()

        # Update statusbar
        cf.log_message("Resistance Measurement Started")

        # Set progress bar to zero
        self.progressBar.show()
        self.progressBar.setProperty("value", 0)

        # Now read in the global settings from file
        # global_settings = cf.read_global_settings()
        self.current_tester.pause = True

        # Instantiate our class
        self.sheet_resistance_measurement = SheetResistanceMeasurement(
            self.keithley_multimeter,
            self.keithley_source,
            global_settings,
            setup_parameters,
            self,
        )

        # Start thread to run measurement
        self.sheet_resistance_measurement.start()

    @QtCore.Slot(float)
    def update_ammeter(self, current_reading):
        """
        Function that is continuously evoked when the current is updated by
        current_tester thread.
        """
        self.sw_applied_current_label_number.setText(
            str(round(current_reading, 4) * 1e3) + " mA"
        )

    @QtCore.Slot(float)
    def update_voltage(self, voltage_reading):
        """
        Function that is continuously evoked when the current is updated by
        current_tester thread.
        """
        self.sw_measured_voltage_label_number.setText(
            str(round(voltage_reading, 6)) + " V"
        )

    @QtCore.Slot(float, float, float, float, float)
    def update_all_labels(
        self,
        current_reading,
        voltage_reading,
        sheet_resistance,
        resisitvity,
        conductivity,
    ):
        """
        Function that is continuously evoked when the current is updated by
        current_tester thread.
        """

        self.update_ammeter(current_reading)
        self.update_voltage(voltage_reading)

        self.sw_sheet_resistance_label_number.setText(
            str(round(sheet_resistance, 2)) + " Ω/□"
        )
        # self.sw_resistivity_label_number.setText(str(round(resisitvity, 4)) + " Ω cm")
        self.sw_resistivity_label_number.setText( str(round(resisitvity * 1000, 3)) + " mΩ cm")
        self.sw_conductivity_label_number.setText(str(round(conductivity, 2)) + " S/cm")

    def activate_output(self):
        """
        Activates Keithley Output if pressed
        """
        if self.sw_activate_output_pushButton.isChecked():
            applied_current = cf.read_global_settings()["applied_current"]
            self.keithley_source.set_current(applied_current)
            time.sleep(0.5)
            self.keithley_source.activate_output()
        else:
            self.keithley_source.deactivate_output()

    def reverse_all_voltages(self):
        """
        Reverse all voltages to prevent the user from needing to swap the cables
        of the source. However, keep the readings and entires positive.
        """
        if self.sw_nip_toggleSwitch.isChecked():
            self.keithley_source.reverse = -1
            cf.log_message("All voltages are reversed")
        else:
            self.keithley_source.reverse = 1
            cf.log_message("Voltages are not reversed")

    def closeEvent(self, event):
        """
        Function that shall allow for save closing of the program
        """

        cf.log_message("Program closed")

        # Kill keithley thread savely
        try:
            self.current_tester.kill()
        except Exception as e:
            cf.log_message("Keithley thread could not be killed")
            cf.log_message(e)

        # Kill connection to spectrometer savely
        try:
            self.spectrometer.close_connection()
        except Exception as e:
            cf.log_message("Spectrometer could not be turned off savely")
            cf.log_message(e)

        # Turn off all outputs etc of Keithley source
        try:
            self.keithley_source.deactivate_output()
        except Exception as e:
            cf.log_message("Keithley source output could not be deactivated")
            cf.log_message(e)

        # Kill connection to Keithleys
        try:
            pyvisa.ResourceManager().close()
        except Exception as e:
            cf.log_message("Connection to Keithleys could not be closed savely")
            cf.log_message(e)

        # if can_exit:
        event.accept()  # let the window close
        self.close()
        # else:
        #     event.ignore()


# Logging
# Prepare file path etc. for logging
LOG_FILENAME = "./usr/log.out"
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.INFO,
    format=(
        "%(asctime)s - [%(levelname)s] -"
        " (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    ),
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

# Activate log_rotate to rotate log files after it reached 1 MB size ()
handler = RotatingFileHandler(LOG_FILENAME, maxBytes=1000000)
logging.getLogger("Rotating Log").addHandler(handler)


# ---------------------------------------------------------------------------- #
# -------------------- This is to execute the program ------------------------ #
# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()

    # Icon (see https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105)
    import ctypes

    if not sys.platform.startswith("linux"):
        myappid = "mycompan.myproduct.subproduct.version"  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app_icon = QtGui.QIcon()
    app_icon.addFile("./icons/program_icon.png", QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)

    ui.show()
    sys.exit(app.exec_())
