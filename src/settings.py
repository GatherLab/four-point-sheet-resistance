# -*- coding: utf-8 -*-
from PySide2 import QtCore, QtGui, QtWidgets

import json
import os
import core_functions as cf
from pathlib import Path

from loading_window import LoadingWindow
from UI_settings_window import Ui_Settings


class Settings(QtWidgets.QDialog, Ui_Settings):
    """
    Settings window
    """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)

        self.parent = parent

        # Load from file to fill the lines
        default_settings = cf.read_global_settings()

        self.keithley_source_address_lineEdit.setText(
            str(default_settings["keithley_source_address"])
        )
        self.keithley_multimeter_address_lineEdit.setText(
            str(default_settings["keithley_multimeter_address"])
        )
        self.probe_spacing_spinBox.setValue(float(default_settings["probe_spacing"]))
        self.applied_current_spinBox.setValue(
            float(default_settings["applied_current"])
        )
        self.measurement_interval_spinBox.setValue(
            float(default_settings["measurement_interval"])
        )
        self.default_saving_path_lineEdit.setText(
            str(default_settings["default_saving_path"])
        )

        # Connect buttons to functions
        self.load_defaults_pushButton.clicked.connect(self.load_defaults)
        self.save_settings_pushButton.clicked.connect(self.save_settings)

        self.initial_settings = json.loads(
            json.dumps(default_settings), parse_float=str
        )

    def save_settings(self):
        """
        Save the settings the user just entered
        """

        # Gather the new settings
        settings_data = {}
        settings_data["overwrite"] = []
        settings_data["overwrite"] = {
            "keithley_source_address": self.keithley_source_address_lineEdit.text(),
            "keithley_multimeter_address": self.keithley_multimeter_address_lineEdit.text(),
            "probe_spacing": self.probe_spacing_spinBox.value(),
            "applied_current": self.applied_current_spinBox.value(),
            "measurement_interval": self.measurement_interval_spinBox.value(),
            "default_saving_path": self.default_saving_path_lineEdit.text(),
        }

        # Load the default parameter settings
        default_settings = cf.read_global_settings(default=True)

        # Add the default parameters to the new settings json
        settings_data["default"] = []
        settings_data["default"] = default_settings

        # Save the entire thing again to the settings.json file
        with open(
            os.path.join(Path(__file__).parent.parent, "usr", "global_settings.json"),
            "w",
        ) as json_file:
            json.dump(settings_data, json_file, indent=4)

        cf.log_message("Settings saved")

        # Close window on accepting
        self.accept()

        reload_window_comparison = {
            k: settings_data["overwrite"][k]
            for k in self.initial_settings
            if k in settings_data["overwrite"]
            and self.initial_settings[k] != settings_data["overwrite"][k]
        }
        # If any of the parameters that require a reinitialisation has been changed, then do one
        if any(
            key in reload_window_comparison.keys()
            for key in [
                "keithley_source_address",
                "keithley_multimeter_address",
            ]
        ):
            # Before closing the window, reinstanciate the devices with the new
            # parameters
            loading_window = LoadingWindow(self.parent)

            # Execute loading dialog
            loading_window.exec()
        else:
            # Otherwise just do the necessary tweaks to the paramters
            if self.parent.sw_top_emitting_toggleSwitch.isChecked():
                offset_angle = float(settings_data["overwrite"]["motor_offset"]) + 180
            else:
                offset_angle = float(settings_data["overwrite"]["motor_offset"])

            self.parent.motor.change_offset_angle(offset_angle, relative=False)
            self.parent.spectrometer.non_linearity_correction = bool(
                settings_data["overwrite"]["spectrometer_non_linearity_correction"]
            )
            self.parent.motor.change_velocity(
                float(settings_data["overwrite"]["motor_speed"])
            )

    def load_defaults(self):
        """
        Load default settings (in case the user messed up the own settings)
        """

        # Read default settings
        default_settings = cf.read_global_settings(default=True)

        self.keithley_source_address_lineEdit.setText(
            str(default_settings["keithley_source_address"])
        )
        self.keithley_multimeter_address_lineEdit.setText(
            str(default_settings["keithley_multimeter_address"])
        )
        self.probe_spacing_spinBox.setValue(float(default_settings["probe_spacing"]))
        self.applied_current_spinBox.setValue(
            float(default_settings["applied_current"])
        )
        self.measurement_interval_spinBox.setValue(
            float(default_settings["measurement_interval"])
        )
        self.default_saving_path_lineEdit.setText(
            default_settings["default_saving_path"]
        )
