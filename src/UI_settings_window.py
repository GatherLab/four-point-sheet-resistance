# -*- coding: utf-8 -*-
from PySide2 import QtCore, QtGui, QtWidgets

import json
import core_functions as cf

from loading_window import LoadingWindow

from costum_widgets import HumbleSpinBox, ToggleSwitch, HumbleDoubleSpinBox


class Ui_Settings(object):
    def setupUi(self, Settings, parent=None):
        # Note: this is not how it should be done but currently I don't know
        # how to do it differently. This is only needed to be able to emit
        # signals to the main window
        self.parent = parent

        Settings.setObjectName("Settings")
        Settings.resize(509, 300)
        Settings.setStyleSheet(
            "QWidget {\n"
            "            background-color: rgb(44, 49, 60);\n"
            "            color: rgb(255, 255, 255);\n"
            '            font: 63 10pt "Segoe UI";\n'
            "}\n"
            "QPushButton {\n"
            "            border: 2px solid rgb(52, 59, 72);\n"
            "            border-radius: 5px;\n"
            "            background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QPushButton:hover {\n"
            "            background-color: rgb(57, 65, 80);\n"
            "            border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {\n"
            "            background-color: rgb(35, 40, 49);\n"
            "            border: 2px solid rgb(43, 50, 61);\n"
            "}\n"
            "QPushButton:checked {\n"
            "            background-color: rgb(35, 40, 49);\n"
            "            border: 2px solid rgb(85, 170, 255);\n"
            "}"
            "QLineEdit {\n"
            "            border: 2px solid rgb(61, 70, 86);\n"
            "            border-radius: 5px;\n"
            "            background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QSpinBox {\n"
            "            border: 2px solid rgb(61, 70, 86);\n"
            "            border-radius: 5px;\n"
            "            background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QDoubleSpinBox {\n"
            "            border: 2px solid rgb(61, 70, 86);\n"
            "            border-radius: 5px;\n"
            "            background-color: rgb(52, 59, 72);\n"
            "}\n"
        )
        self.gridLayout = QtWidgets.QGridLayout(Settings)
        self.gridLayout.setContentsMargins(25, 10, 25, 10)
        self.gridLayout.setObjectName("gridLayout")

        # Device settings
        self.device_settings_header_label = QtWidgets.QLabel(Settings)
        self.device_settings_header_label.setMinimumSize(QtCore.QSize(0, 20))
        self.device_settings_header_label.setStyleSheet(
            'font: 75 bold 10pt "Segoe UI";'
        )
        self.device_settings_header_label.setObjectName("device_settings_header_label")
        self.gridLayout.addWidget(self.device_settings_header_label, 0, 0, 1, 2)

        self.header_line_1 = QtWidgets.QFrame()
        self.header_line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.header_line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout.addWidget(self.header_line_1, 1, 0, 1, 2)
        self.header_line_1.setStyleSheet(
            "QFrame {\n" "            border: 2px solid rgb(52, 59, 72);\n" "}\n"
        )

        # Keithley source address
        self.keithley_source_address_label = QtWidgets.QLabel(Settings)
        self.keithley_source_address_label.setObjectName(
            "keithley_source_address_label"
        )
        self.gridLayout.addWidget(self.keithley_source_address_label, 2, 0, 1, 1)
        self.keithley_source_address_lineEdit = QtWidgets.QLineEdit(Settings)
        self.keithley_source_address_lineEdit.setObjectName(
            "keithley_source_address_lineEdit"
        )
        self.keithley_source_address_lineEdit.setMinimumSize(QtCore.QSize(270, 0))
        # self.keithley_source_address_lineEdit.setText(
        # u"USB0::0x05E6::0x2450::04102170::INSTR"
        # )
        self.gridLayout.addWidget(self.keithley_source_address_lineEdit, 2, 1, 1, 1)

        # Keithley multimeter address
        self.keithley_multimeter_address_label = QtWidgets.QLabel(Settings)
        self.keithley_multimeter_address_label.setObjectName(
            "keithley_multimeter_address_label"
        )
        self.gridLayout.addWidget(self.keithley_multimeter_address_label, 3, 0, 1, 1)
        self.keithley_multimeter_address_lineEdit = QtWidgets.QLineEdit(Settings)
        self.keithley_multimeter_address_lineEdit.setObjectName(
            "keithley_multimeter_address_lineEdit"
        )
        # self.keithley_multimeter_address_lineEdit.setText(
        # u"USB0::0x05E6::0x2100::8003430::INSTR"
        # )
        self.gridLayout.addWidget(self.keithley_multimeter_address_lineEdit, 3, 1, 1, 1)

        # Probe Spacing
        self.probe_spacing_label = QtWidgets.QLabel(Settings)
        self.probe_spacing_label.setObjectName("probe_spacing_label")
        self.gridLayout.addWidget(self.probe_spacing_label, 4, 0, 1, 1)
        self.probe_spacing_spinBox = HumbleDoubleSpinBox(Settings)
        self.probe_spacing_spinBox.setObjectName("probe_spacing_spinBox")
        self.gridLayout.addWidget(self.probe_spacing_spinBox, 4, 1, 1, 1)

        # Applied Current
        self.applied_current_label = QtWidgets.QLabel(Settings)
        self.applied_current_label.setObjectName("applied_current_label")
        self.gridLayout.addWidget(self.applied_current_label, 5, 0, 1, 1)
        self.applied_current_spinBox = HumbleDoubleSpinBox(Settings)
        self.applied_current_spinBox.setObjectName("applied_current_spinBox")
        self.gridLayout.addWidget(self.applied_current_spinBox, 5, 1, 1, 1)

        # Measurement Interval
        self.measurement_interval_label = QtWidgets.QLabel(Settings)
        self.measurement_interval_label.setObjectName("measurement_interval_label")
        self.gridLayout.addWidget(self.measurement_interval_label, 6, 0, 1, 1)
        self.measurement_interval_spinBox = HumbleSpinBox(Settings)
        self.measurement_interval_spinBox.setObjectName("measurement_interval_spinBox")
        self.gridLayout.addWidget(self.measurement_interval_spinBox, 6, 1, 1, 1)

        # Global Software Settings
        self.global_settings_header_label = QtWidgets.QLabel(Settings)
        self.global_settings_header_label.setMinimumSize(QtCore.QSize(0, 20))
        self.global_settings_header_label.setStyleSheet(
            'font: 75 bold 10pt "Segoe UI";'
        )
        self.global_settings_header_label.setObjectName("global_settings_header_label")
        self.gridLayout.addWidget(self.global_settings_header_label, 7, 0, 1, 2)

        self.header_line_3 = QtWidgets.QFrame()
        self.header_line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.header_line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout.addWidget(self.header_line_3, 8, 0, 1, 2)
        self.header_line_3.setStyleSheet(
            "QFrame {\n" "            border: 2px solid rgb(52, 59, 72);\n" "}\n"
        )

        # Standard Saving Path
        self.default_saving_path_label = QtWidgets.QLabel(Settings)
        self.default_saving_path_label.setObjectName("default_saving_path_label")
        self.gridLayout.addWidget(self.default_saving_path_label, 9, 0, 1, 1)
        self.default_saving_path_lineEdit = QtWidgets.QLineEdit(Settings)
        self.default_saving_path_lineEdit.setObjectName("default_saving_path_lineEdit")
        self.gridLayout.addWidget(self.default_saving_path_lineEdit, 9, 1, 1, 1)

        # Push Buttons
        self.buttons_HBoxLayout = QtWidgets.QHBoxLayout()
        self.load_defaults_pushButton = QtWidgets.QPushButton(Settings)
        self.load_defaults_pushButton.setObjectName("load_defaults_pushButton")
        self.buttons_HBoxLayout.addWidget(self.load_defaults_pushButton)

        self.save_settings_pushButton = QtWidgets.QPushButton(Settings)
        self.save_settings_pushButton.setObjectName("save_settings_pushButton")
        self.buttons_HBoxLayout.addWidget(self.save_settings_pushButton)

        self.gridLayout.addLayout(self.buttons_HBoxLayout, 10, 0, 1, 2)

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Options"))
        self.device_settings_header_label.setText(
            _translate("Settings", "Device Settings")
        )
        self.keithley_source_address_label.setText(
            _translate("Settings", "Keithley Source Address")
        )
        self.keithley_multimeter_address_label.setText(
            _translate("Settings", "Keithley Multimeter Address")
        )
        self.probe_spacing_label.setText(_translate("Settings", "Probe Spacing (mm)"))
        self.applied_current_label.setText(
            _translate("Settings", "Applied Current (mA)")
        )

        self.measurement_interval_label.setText(
            _translate("Settings", "Measurement Frequency (1/s)")
        )

        self.global_settings_header_label.setText(
            _translate("Settings", "Software Settings")
        )

        self.default_saving_path_label.setText(
            _translate("Settings", "Default Saving Path")
        )

        self.save_settings_pushButton.setText(_translate("Settings", "Save Settings"))
        self.load_defaults_pushButton.setText(_translate("Settings", "Load Defaults"))
