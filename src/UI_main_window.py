# -*- coding: utf-8 -*-

# Initial gui design with QtCreator then translated into python code and adjusted

# from UI_settings_window import Ui_Settings
from costum_widgets import (
    HumbleDoubleSpinBox,
    HumbleSpinBox,
    ToggleSwitch,
    Ui_GoniometerAnimation,
)

from PySide2 import QtCore, QtGui, QtWidgets

import matplotlib.pylab as plt
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
import matplotlib.backends.backend_qt5

import time


# ---------------------------------------------------------------------------- #
# --------------------------- Define Main Window ----------------------------- #
# ---------------------------------------------------------------------------- #
class Ui_MainWindow(object):
    """
    Class that contains all information about the main window
    """

    def setupUi(self, MainWindow):
        """
        Setup that sets all gui widgets at their place
        """

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setStyleSheet(
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
            "}\n"
            "QComboBox {\n"
            "            border: 2px solid rgb(52, 59, 72);\n"
            "            border-radius: 5px;\n"
            "            background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QComboBox:checked {\n"
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
            "HumbleDoubleSpinBox {\n"
            "            border: 2px solid rgb(61, 70, 86);\n"
            "            border-radius: 5px;\n"
            "            background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QScrollArea {\n"
            "            border: 2px solid rgb(61, 70, 86);\n"
            "            border-radius: 5px;\n"
            "}\n"
            "QScrollBar {\n"
            "            border-radius: 5px;\n"
            "            background: rgb(61, 70, 86);\n"
            "}\n"
            "QScrollBar:add-page {\n"
            "            background: rgb(52, 59, 72);\n"
            "}\n"
            "QScrollBar:sub-page {\n"
            "            background: rgb(52, 59, 72);\n"
            "}\n"
        )

        self.center()

        # Define central widget of the MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        # self.centralwidget.setStyleSheet(
        #     "QLineEdit {\n"
        #     "            border: 2px solid rgb(61, 70, 86);\n"
        #     "            border-radius: 5px;\n"
        #     "            background-color: rgb(52, 59, 72);\n"
        #     "}\n"
        #     "QSpinBox {\n"
        #     "            border: 2px solid rgb(61, 70, 86);\n"
        #     "            border-radius: 5px;\n"
        #     "            background-color: rgb(52, 59, 72);\n"
        #     "}\n"
        #     "HumbleDoubleSpinBox {\n"
        #     "            border: 2px solid rgb(61, 70, 86);\n"
        #     "            border-radius: 5px;\n"
        #     "            background-color: rgb(52, 59, 72);\n"
        #     "}\n"
        #     "QScrollArea {\n"
        #     "            border: 2px solid rgb(61, 70, 86);\n"
        #     "            border-radius: 5px;\n"
        #     "}\n"
        #     "QScrollBar {\n"
        #     # "            border: 2px solid rgb(85, 170, 255);\n"
        #     "            border-radius: 5px;\n"
        #     "            background: rgb(61, 70, 86);\n"
        #     "}\n"
        #     "QScrollBar:add-page {\n"
        #     "            background: rgb(52, 59, 72);\n"
        #     "}\n"
        #     "QScrollBar:sub-page {\n"
        #     "            background: rgb(52, 59, 72);\n"
        #     "}\n"
        # )
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(-1, -1, -1, 6)
        self.gridLayout.setObjectName("gridLayout")

        # This here shall be the logo of the program
        # self.gatherlab_picture = QtWidgets.QWidget(self.centralwidget)
        # self.gatherlab_picture.setObjectName("gatherlab_picture")
        self.gatherlab_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("icons/blue_cropped.png")
        self.gatherlab_label.setPixmap(pixmap)
        self.gatherlab_label.setScaledContents(True)
        # self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        # self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        # self.gatherlab_picture.setLayout(self.horizontalLayout_2)
        self.gridLayout.addWidget(self.gatherlab_label, 0, 0, 1, 1)

        # Tab widget
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setStyleSheet(
            "QTabBar {\n"
            "        font-weight: bold;\n"
            "}\n"
            "QTabBar:tab {\n"
            "            background: rgb(52, 59, 72);\n"
            "}\n"
            "QTabBar:tab:selected {\n"
            "            background: rgb(61, 70, 86);\n"
            "            color: rgb(85, 170, 255);\n"
            "}\n"
            "QTabBar:tab:hover {\n"
            "            color: rgb(85, 170, 255);\n"
            "}\n"
            "QTabWidget:pane {\n"
            "            border: 2px solid rgb(52, 59, 72);\n"
            "}\n"
        )

        # -------------------------------------------------------------------- #
        # --------------------------- Setup widget --------------------------- #
        # -------------------------------------------------------------------- #
        self.setup_widget = QtWidgets.QWidget()
        self.setup_widget.setObjectName("setup_widget")
        # self.gridLayout_5 = QtWidgets.QGridLayout(self.setup_widget)
        # self.gridLayout_5.setObjectName("gridLayout_5")
        # self.setup_sub_widget = QtWidgets.QWidget(self.setup_widget)
        # self.setup_sub_widget.setObjectName("setup_sub_widget")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.setup_widget)
        self.gridLayout_7.setObjectName("gridLayout_7")

        # Setup widget header 1
        self.sw_header1_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_header1_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.sw_header1_label.setObjectName("sw_header1_label")
        # self.sw_header1_label.setSizePolicy(sizePolicy)
        # self.sw_header1_label.setMaximumSize(QtCore.QSize(400, 10))
        self.gridLayout_7.addWidget(self.sw_header1_label, 0, 0, 1, 1)

        # Setup widget base folder path
        self.sw_folder_path_horizontalLayout = QtWidgets.QHBoxLayout()
        self.sw_folder_path_horizontalLayout.setObjectName(
            "sw_folder_path_horizontalLayout"
        )
        self.sw_folder_path_lineEdit = QtWidgets.QLineEdit(self.setup_widget)
        self.sw_folder_path_lineEdit.setReadOnly(False)
        self.sw_folder_path_lineEdit.setObjectName("sw_folder_path_lineEdit")
        self.sw_folder_path_horizontalLayout.addWidget(self.sw_folder_path_lineEdit)
        self.sw_browse_pushButton = QtWidgets.QPushButton(self.setup_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sw_browse_pushButton.sizePolicy().hasHeightForWidth()
        )
        self.sw_browse_pushButton.setSizePolicy(sizePolicy)
        self.sw_browse_pushButton.setMinimumSize(QtCore.QSize(60, 0))
        self.sw_browse_pushButton.setObjectName("sw_browse_pushButton")
        self.sw_folder_path_horizontalLayout.addWidget(self.sw_browse_pushButton)
        self.gridLayout_7.addLayout(self.sw_folder_path_horizontalLayout, 1, 1, 1, 1)
        self.sw_folder_path_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_folder_path_label.setObjectName("sw_folder_path_label")
        self.gridLayout_7.addWidget(self.sw_folder_path_label, 1, 0, 1, 1)

        # Setup widget batch name
        self.sw_batch_name_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_batch_name_label.setObjectName("sw_batch_name_label")
        self.gridLayout_7.addWidget(self.sw_batch_name_label, 2, 0, 1, 1)
        self.sw_batch_name_lineEdit = QtWidgets.QLineEdit(self.setup_widget)
        self.sw_batch_name_lineEdit.setObjectName("sw_batch_name_lineEdit")
        self.gridLayout_7.addWidget(self.sw_batch_name_lineEdit, 2, 1, 1, 1)

        # Setup widget device number
        self.sw_device_number_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_device_number_label.setObjectName("sw_device_number_label")
        self.gridLayout_7.addWidget(self.sw_device_number_label, 3, 0, 1, 1)
        self.sw_device_number_spinBox = HumbleSpinBox(self.setup_widget)
        self.sw_device_number_spinBox.setObjectName("sw_device_number_spinBox")
        self.gridLayout_7.addWidget(self.sw_device_number_spinBox, 3, 1, 1, 1)

        # ------------- Define Measurement Parameters ------------------ #
        self.sw_measurement_parameters_widget = QtWidgets.QWidget(self.setup_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.sw_measurement_parameters_widget.sizePolicy().hasHeightForWidth()
        )
        self.sw_measurement_parameters_widget.setSizePolicy(sizePolicy)
        self.sw_measurement_parameters_widget.setObjectName(
            "sw_measurement_parameters_widget"
        )
        self.gridLayout_6 = QtWidgets.QGridLayout(self.sw_measurement_parameters_widget)
        self.gridLayout_6.setObjectName("gridLayout_6")

        # Activate Output
        self.sw_activate_output_pushButton = QtWidgets.QPushButton(
            self.sw_measurement_parameters_widget
        )
        self.sw_activate_output_pushButton.setObjectName(
            "sw_activate_output_pushButton"
        )
        self.gridLayout_6.addWidget(self.sw_activate_output_pushButton, 0, 0, 1, 2)

        # Spacer
        self.verticalSpacer_2 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_6.addItem(self.verticalSpacer_2, 1, 0, 1, 2)

        # Setup widget header
        self.sw_header2_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_header2_label.setStyleSheet('font: 63 bold 10pt "Segoe UI";')
        self.sw_header2_label.setObjectName("sw_header2_label")
        self.gridLayout_6.addWidget(self.sw_header2_label, 2, 0, 1, 2)

        # pin or nip
        # self.sw_nip_HLayout = QtWidgets.QHBoxLayout()
        # self.sw_nip_toggleSwitch = ToggleSwitch()
        # self.sw_nip_label = QtWidgets.QLabel("Reverse Polarity")
        # self.sw_nip_HLayout.addWidget(self.sw_nip_toggleSwitch)
        # self.sw_nip_HLayout.addWidget(self.sw_nip_label)
        # self.gridLayout_6.addLayout(self.sw_nip_HLayout, 1, 0, 1, 2)

        # Sample Geometry
        self.sw_select_sample_geometry_label = QtWidgets.QLabel(
            self.sw_measurement_parameters_widget
        )
        self.sw_select_sample_geometry_label.setObjectName(
            "sw_select_sample_geometry_label"
        )
        self.gridLayout_6.addWidget(self.sw_select_sample_geometry_label, 3, 0, 1, 2)

        self.sw_select_sample_geometry_ComboBox = QtWidgets.QComboBox()
        self.sw_select_sample_geometry_ComboBox.setObjectName(
            "sw_select_sample_geometry_ComboBox"
        )
        self.gridLayout_6.addWidget(self.sw_select_sample_geometry_ComboBox, 4, 0, 1, 2)

        # Long Side Length
        self.sw_long_side_length_label = QtWidgets.QLabel(
            self.sw_measurement_parameters_widget
        )
        self.sw_long_side_length_label.setObjectName("sw_long_side_length_label")
        self.gridLayout_6.addWidget(self.sw_long_side_length_label, 5, 0, 1, 2)

        self.sw_long_side_length_spinBox = HumbleDoubleSpinBox(
            self.sw_measurement_parameters_widget
        )
        self.sw_long_side_length_spinBox.setObjectName("sw_long_side_length_spinBox")
        self.gridLayout_6.addWidget(self.sw_long_side_length_spinBox, 6, 0, 1, 2)

        # Short Side Length
        self.sw_short_side_length_label = QtWidgets.QLabel(
            self.sw_measurement_parameters_widget
        )
        self.sw_short_side_length_label.setObjectName("sw_short_side_length_label")
        self.gridLayout_6.addWidget(self.sw_short_side_length_label, 7, 0, 1, 2)

        self.sw_short_side_length_spinBox = HumbleDoubleSpinBox(
            self.sw_measurement_parameters_widget
        )
        self.sw_short_side_length_spinBox.setObjectName("sw_short_side_length_spinBox")
        self.gridLayout_6.addWidget(self.sw_short_side_length_spinBox, 8, 0, 1, 2)

        # Thickness
        self.sw_thickness_label = QtWidgets.QLabel(
            self.sw_measurement_parameters_widget
        )
        self.sw_thickness_label.setObjectName("sw_thickness_label")
        self.gridLayout_6.addWidget(self.sw_thickness_label, 9, 0, 1, 2)

        self.sw_thickness_spinBox = HumbleDoubleSpinBox(
            self.sw_measurement_parameters_widget
        )
        self.sw_thickness_spinBox.setObjectName("sw_thickness_spinBox")
        self.gridLayout_6.addWidget(self.sw_thickness_spinBox, 10, 0, 1, 2)

        # Spacer
        self.verticalSpacer_1 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_6.addItem(self.verticalSpacer_1, 11, 0, 1, 2)

        # Number of Averages
        self.sw_no_of_averages_label = QtWidgets.QLabel(
            self.sw_measurement_parameters_widget
        )
        self.sw_no_of_averages_label.setObjectName("sw_no_of_averages_label")
        self.gridLayout_6.addWidget(self.sw_no_of_averages_label, 12, 0, 1, 2)

        self.sw_no_of_averages_spinBox = HumbleDoubleSpinBox(
            self.sw_measurement_parameters_widget
        )
        self.sw_no_of_averages_spinBox.setObjectName("sw_no_of_averages_spinBox")
        self.gridLayout_6.addWidget(self.sw_no_of_averages_spinBox, 13, 0, 1, 2)

        # Start Measurement Button
        self.sw_start_measurement_pushButton = QtWidgets.QPushButton(
            self.sw_measurement_parameters_widget
        )
        self.sw_start_measurement_pushButton.setObjectName(
            "sw_reset_hardware_pushButton"
        )
        self.gridLayout_6.addWidget(self.sw_start_measurement_pushButton, 14, 0, 1, 2)

        self.gridLayout_7.addWidget(self.sw_measurement_parameters_widget, 5, 0, 5, 1)

        # ------------- Label number widget ------------------ #
        self.sw_label_number_widget = QtWidgets.QWidget(self.setup_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.sw_label_number_widget.sizePolicy().hasHeightForWidth()
        )
        self.sw_label_number_widget.setSizePolicy(sizePolicy)
        # self.sw_measurement_parameters_widget.setMinimumSize(QtCore.QSize(150, 0))
        # self.sw_measurement_parameters_widget.setMaximumSize(QtCore.QSize(250, 200))
        self.sw_label_number_widget.setObjectName("sw_label_number_widget")

        self.vertical_layout_1 = QtWidgets.QVBoxLayout(self.sw_label_number_widget)
        self.vertical_layout_1.setObjectName("vertical_layout_1")

        # current label number widget
        self.sw_current_label_HLayout = QtWidgets.QHBoxLayout()
        self.sw_current_label_HLayout.setObjectName("sw_current_label_HLayout")

        self.sw_applied_current_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_applied_current_label.setStyleSheet(
            "QLabel {\n" 'font: 63 bold 30pt "Segoe UI";\n' "}"
        )
        self.sw_applied_current_label.setObjectName("sw_applied_current_label")
        self.sw_applied_current_label.setText("Applied Current:\t\t")
        self.sw_current_label_HLayout.addWidget(self.sw_applied_current_label)

        self.sw_applied_current_label_number = QtWidgets.QLabel(self.setup_widget)
        self.sw_applied_current_label_number.setStyleSheet(
            "QLabel {\n" 'font: 63 bold 30pt "Segoe UI";\n' "}"
        )
        self.sw_applied_current_label_number.setObjectName(
            "sw_applied_current_label_number"
        )
        self.sw_current_label_HLayout.addWidget(self.sw_applied_current_label_number)

        self.sw_applied_current_label_number.setText("--.-- mA")

        self.vertical_layout_1.addLayout(self.sw_current_label_HLayout)

        # voltage label number widget
        self.sw_voltage_label_HLayout = QtWidgets.QHBoxLayout()
        self.sw_voltage_label_HLayout.setObjectName("sw_voltage_label_HLayout")

        self.sw_measured_voltage_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_measured_voltage_label.setStyleSheet(
            "QLabel {\n" 'font: 63 bold 30pt "Segoe UI";\n' "}"
        )
        self.sw_measured_voltage_label.setObjectName("sw_measured_voltage_label")
        self.sw_measured_voltage_label.setText("Measured Voltage:\t")
        self.sw_voltage_label_HLayout.addWidget(self.sw_measured_voltage_label)

        self.sw_measured_voltage_label_number = QtWidgets.QLabel(self.setup_widget)
        self.sw_measured_voltage_label_number.setStyleSheet(
            "QLabel {\n" 'font: 63 bold 30pt "Segoe UI";\n' "}"
        )
        self.sw_measured_voltage_label_number.setObjectName(
            "sw_measured_voltage_label_number"
        )
        self.sw_measured_voltage_label_number.setText("--.-- V")
        self.sw_voltage_label_HLayout.addWidget(self.sw_measured_voltage_label_number)

        self.vertical_layout_1.addLayout(self.sw_voltage_label_HLayout)

        # Spacer
        self.verticalSpacer = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.vertical_layout_1.addItem(self.verticalSpacer)

        # Resulting Sheet resistance number widget
        self.sw_sheet_resistance_label_HLayout = QtWidgets.QHBoxLayout()
        self.sw_sheet_resistance_label_HLayout.setObjectName(
            "sw_sheet_resistance_label_HLayout"
        )

        self.sw_sheet_resistance_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_sheet_resistance_label.setStyleSheet(
            "QLabel {\n"
            'font: 63 bold 50pt "Segoe UI";\n'
            "color: rgb(85, 170, 255);\n"
            "}"
        )
        self.sw_sheet_resistance_label.setObjectName("sw_sheet_resistance_label")
        self.sw_sheet_resistance_label.setText("Sheet Resistance:\t\t")
        self.sw_sheet_resistance_label_HLayout.addWidget(self.sw_sheet_resistance_label)

        self.sw_sheet_resistance_label_number = QtWidgets.QLabel(self.setup_widget)
        self.sw_sheet_resistance_label_number.setStyleSheet(
            "QLabel {\n"
            'font: 63 bold 50pt "Segoe UI";\n'
            "color: rgb(85, 170, 255);\n"
            "}"
        )
        self.sw_sheet_resistance_label_number.setObjectName(
            "sw_sheet_resistance_label_number"
        )
        self.sw_sheet_resistance_label_number.setText("--.-- Ω/□")
        self.sw_sheet_resistance_label_HLayout.addWidget(
            self.sw_sheet_resistance_label_number
        )

        self.vertical_layout_1.addLayout(self.sw_sheet_resistance_label_HLayout)

        # Resulting Resistivity
        self.sw_resistivity_label_HLayout = QtWidgets.QHBoxLayout()
        self.sw_resistivity_label_HLayout.setObjectName("sw_resistivity_label_HLayout")

        self.sw_resistivity_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_resistivity_label.setStyleSheet(
            "QLabel {\n"
            'font: 63 bold 50pt "Segoe UI";\n'
            # "color: rgb(85, 170, 255);\n"
            "}"
        )
        self.sw_resistivity_label.setObjectName("sw_resistivity_label")
        self.sw_resistivity_label.setText("Resistivity:\t\t")
        self.sw_resistivity_label_HLayout.addWidget(self.sw_resistivity_label)

        self.sw_resistivity_label_number = QtWidgets.QLabel(self.setup_widget)
        self.sw_resistivity_label_number.setStyleSheet(
            "QLabel {\n"
            'font: 63 bold 50pt "Segoe UI";\n'
            # "color: rgb(85, 170, 255);\n"
            "}"
        )
        self.sw_resistivity_label_number.setObjectName("sw_resistivity_label_number")
        self.sw_resistivity_label_number.setText("--.-- Ω cm")
        self.sw_resistivity_label_HLayout.addWidget(self.sw_resistivity_label_number)

        self.vertical_layout_1.addLayout(self.sw_resistivity_label_HLayout)

        # Resulting Conductivity
        self.sw_conductivity_label_HLayout = QtWidgets.QHBoxLayout()
        self.sw_conductivity_label_HLayout.setObjectName(
            "sw_conductivity_label_HLayout"
        )

        self.sw_conductivity_label = QtWidgets.QLabel(self.setup_widget)
        self.sw_conductivity_label.setStyleSheet(
            "QLabel {\n"
            'font: 63 bold 50pt "Segoe UI";\n'
            # "color: rgb(85, 170, 255);\n"
            "}"
        )
        self.sw_conductivity_label.setObjectName("sw_conductivity_label")
        self.sw_conductivity_label.setText("Conductivity:\t\t")
        self.sw_conductivity_label_HLayout.addWidget(self.sw_conductivity_label)

        self.sw_conductivity_label_number = QtWidgets.QLabel(self.setup_widget)
        self.sw_conductivity_label_number.setStyleSheet(
            "QLabel {\n"
            'font: 63 bold 50pt "Segoe UI";\n'
            # "color: rgb(85, 170, 255);\n"
            "}"
        )
        self.sw_conductivity_label_number.setObjectName("sw_conductivity_label_number")
        self.sw_conductivity_label_number.setText("--.-- S/cm")
        self.sw_conductivity_label_HLayout.addWidget(self.sw_conductivity_label_number)

        self.vertical_layout_1.addLayout(self.sw_conductivity_label_HLayout)

        self.gridLayout_7.addWidget(self.sw_label_number_widget, 5, 1, 5, 1)

        self.tabWidget.addTab(self.setup_widget, "")

        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        # -------------------------------------------------------------------- #
        # ------------------------- Define Menubar --------------------------- #
        # -------------------------------------------------------------------- #

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 973, 31))
        self.menubar.setObjectName("menubar")
        # self.menudfg = QtWidgets.QMenu(self.menubar)
        # self.menudfg.setObjectName("menudfg")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)

        # Define actions for menubar
        self.actionOpen_Logs = QtWidgets.QAction(MainWindow)
        self.actionOpen_Logs.setObjectName("actionOpen_Logs")
        # self.actionOpen_Logfile_on_Machine = QtWidgets.QAction(MainWindow)
        # self.actionOpen_Logfile_on_Machine.setObjectName(
        # "actionOpen_Logfile_on_Machine"
        # )

        self.actionChange_Path = QtWidgets.QAction(MainWindow)
        self.actionChange_Path.setObjectName("actionChange_Path")

        self.actionOptions = QtWidgets.QAction(MainWindow)
        self.actionOptions.setObjectName("actionOptions")

        self.actionDocumentation = QtWidgets.QAction(MainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")

        self.actionLoad_Measurement_Parameters = QtWidgets.QAction(MainWindow)
        self.actionLoad_Measurement_Parameters.setObjectName(
            "actionLoad_Measurement_Parameters"
        )
        self.actionSave_Measurement_Parameters = QtWidgets.QAction(MainWindow)
        self.actionSave_Measurement_Parameters.setObjectName(
            "actionSave_Measurement_Parameters"
        )
        self.actionOpen_Log = QtWidgets.QAction(MainWindow)
        self.actionOpen_Log.setObjectName("actionOpen_Log")
        # self.menudfg.addAction(self.actionLoad_Measurement_Parameters)
        # self.menudfg.addAction(self.actionSave_Measurement_Parameters)
        self.menuSettings.addAction(self.actionOptions)
        self.menuSettings.addAction(self.actionDocumentation)
        self.menuSettings.addAction(self.actionOpen_Log)
        # self.menubar.addAction(self.menudfg.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        # -------------------------------------------------------------------- #
        # ----------------------- Define Statusbar --------------------------- #
        # -------------------------------------------------------------------- #

        # Define progress bar in the status bar
        self.progressBar = QtWidgets.QProgressBar()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QtCore.QSize(150, 15))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setStyleSheet(
            "QProgressBar"
            "{"
            "border-radius: 5px;"
            "background-color: #FFFFFF;"
            "text-align: center;"
            "color: black;"
            'font: 63 bold 10pt "Segoe UI";'
            "}"
            "QProgressBar::chunk "
            "{"
            "background-color: rgb(85, 170, 255);"
            "border-radius: 5px;"
            "}"
        )

        # Define the statusbar itself
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setToolTip("")
        self.statusbar.setStatusTip("")
        self.statusbar.setWhatsThis("")
        self.statusbar.setAccessibleName("")
        self.statusbar.setObjectName("statusbar")
        self.statusbar.addPermanentWidget(self.progressBar)
        # self.statusbar.showMessage("Ready", 10000000)

        MainWindow.setStatusBar(self.statusbar)

        # -------------------------------------------------------------------- #
        # --------------------- Some General things -------------------------- #
        # -------------------------------------------------------------------- #
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        This function basicall contains all the text that is visible in the window.
        I think it is good practice to keep this seperate just in case the program
        would be translated to other languages.
        """

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OLED Characterisation"))
        # self.gatherlab_label.setText(
        # _translate("MainWindow", "Gatherlab JVL Measurement")
        # )
        self.sw_header2_label.setText(
            _translate("MainWindow", "Measurement Parameters")
        )
        self.sw_browse_pushButton.setText(_translate("MainWindow", "Browse"))
        self.sw_long_side_length_spinBox.setSuffix(_translate("MainWindow", " mm"))
        self.sw_short_side_length_spinBox.setSuffix(_translate("MainWindow", " mm"))
        self.sw_thickness_spinBox.setSuffix(_translate("MainWindow", " nm"))
        self.sw_batch_name_label.setText(_translate("MainWindow", "Batch Name"))
        self.sw_batch_name_lineEdit.setStatusTip(
            "Batch name must not contain underscores!"
        )
        self.sw_device_number_label.setText(_translate("MainWindow", "Device Number"))
        self.sw_activate_output_pushButton.setText(
            _translate("MainWindow", "Activate Output")
        )
        # self.sw_header1_label.setToolTip(
        # _translate(
        # "MainWindow",
        # "<html><head/><body><p>The file name the data is saved in in the end"
        # " will be in the format"
        # " yyyy-mm-dd_&lt;batch-name&gt;_d&lt;device-number&gt;_p&lt;pixel-number&gt;.csv.</p></body></html>",
        # )
        # )
        self.sw_header1_label.setText(
            _translate("MainWindow", "Batch Name and File Path")
        )
        self.sw_start_measurement_pushButton.setText(
            _translate("MainWindow", "Start Measurement")
        )
        self.sw_long_side_length_label.setText(
            _translate("MainWindow", "Long Side (mm)")
        )
        self.sw_select_sample_geometry_label.setText(
            _translate("MainWindow", "Select Sample Geometry")
        )

        self.sw_short_side_length_label.setText(
            _translate("MainWindow", "Short Side (mm)")
        )
        self.sw_thickness_label.setText(_translate("MainWindow", "Thickness (nm)"))
        self.sw_no_of_averages_label.setText(
            _translate("MainWindow", "Number of Averages")
        )
        # self.sw_documentation_label.setToolTip(
        # _translate(
        # "MainWindow",
        # "<html><head/><body><p>Please write here any comments to the"
        # " measurement of your batch. The comments will be saved as .md file"
        # " within your selected file path. If there are any issues with the"
        # " measurement setup or the software document it in a seperate line"
        # " starting with [!] to ensure easy debugging.</p></body></html>",
        # )
        # )
        # self.sw_documentation_label.setText(_translate("MainWindow", "Documentation"))
        self.sw_folder_path_label.setText(_translate("MainWindow", "Folder Path"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.setup_widget),
            _translate("MainWindow", "Sheet Resistance"),
        )

        # self.menudfg.setTitle(_translate("MainWindow", "File"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))

        # self.actionOpen_Logs.setText(_translate("MainWindow", "Open Logs"))
        # self.actionOpen_Logfile_on_Machine.setText(
        # _translate("MainWindow", "Open Logfile on Machine")
        # )
        self.actionChange_Path.setText(_translate("MainWindow", "Change Saving Path"))
        self.actionOptions.setText(_translate("MainWindow", "Options"))
        self.actionDocumentation.setText(_translate("MainWindow", "Help"))
        self.actionLoad_Measurement_Parameters.setText(
            _translate("MainWindow", "Load Measurement Parameters")
        )
        self.actionSave_Measurement_Parameters.setText(
            _translate("MainWindow", "Save Measurement Settings")
        )
        self.actionOpen_Log.setText(_translate("MainWindow", "Open Log"))

    # ------------------------------------------------------------------------ #
    # ----------------- User Defined UI related Functions -------------------- #
    # ------------------------------------------------------------------------ #
    def center(self):
        # position and size of main window

        # self.showFullScreen()
        qc = self.frameGeometry()
        # desktopWidget = QtWidgets.QApplication.desktop()
        # PCGeometry = desktopWidget.screenGeometry()
        # self.resize(PCGeometry.height(), PCGeometry.height())
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qc.moveCenter(cp)
        self.move(qc.topLeft())
