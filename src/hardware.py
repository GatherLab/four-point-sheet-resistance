import pyvisa  # Keithley Module
import serial  # Arduino Module

import core_functions as cf

import sys
import time
import logging
import re
import numpy as np
import math
import copy

from PySide2 import QtCore, QtGui, QtWidgets


class KeithleySource:
    """
    Class that manages all functionality of our Keithley voltage/current source
    """

    def __init__(self, keithley_source_address, current_compliance):
        """
        Initialise Hardware. This function must be improved later as well.
        For the time being it is probably alright.
        """
        # Define a mutex
        self.mutex = QtCore.QMutex(QtCore.QMutex.Recursive)

        # Keithley Finding Device
        rm = pyvisa.ResourceManager()
        # The actual addresses for the Keithleys can be accessed via rm.list_resources()
        visa_resources = rm.list_resources()

        # Check if keithley source is present at the given address
        if keithley_source_address not in visa_resources:
            cf.log_message("The SourceMeter seems to be absent or switched off.")
            raise IOError("The SourceMeter seems to be absent or switched off.")

        self.keith = rm.open_resource(keithley_source_address)

        # As a standard initialise the Keithley as a voltage source
        self.as_current_source(current_compliance)

        # Reverse voltages
        self.reverse = 1

    def as_voltage_source(self, current_compliance):
        """
        Function that initalises the Keithley as a voltage source
        """
        self.mutex.lock()
        # Write operational parameters to Sourcemeter (Voltage to OLED)
        self.reset()
        # set voltage as source
        self.keith.write("Source:Function Volt")
        # choose current for measuring
        self.keith.write('Sense:Function "Current"')
        # set compliance
        self.keith.write("Source:Volt:ILimit " + str(current_compliance * 1e-3))
        # reads back the set voltage
        self.keith.write("Source:Volt:READ:BACK ON")
        # sets the read-out speed and accuracy (0.01 fastest, 10 slowest but highest accuracy)
        self.keith.write("Current:NPLCycles 1")
        self.keith.write("Current:AZero OFF")  # turn off autozero
        self.keith.write("Source:Volt:Delay:AUTO OFF")  # turn off autodelay

        # Set voltage mode indicator
        self.mode = "voltage"
        self.mutex.unlock()

    def as_current_source(self, voltage_compliance):
        """
        Initialise (or reinitialise) class as current source
        """
        self.mutex.lock()
        # Write operational parameters to Sourcemeter (Voltage to OLED)
        self.reset()
        # Write operational parameters to Sourcemeter (Current to OLED)
        self.keith.write("Source:Function Current")  # set current as source

        self.keith.write('Sense:Function "Volt"')  # choose voltage for measuring
        self.keith.write(
            "Source:Current:VLimit " + str(voltage_compliance)
        )  # set voltage compliance to compliance
        self.keith.write(
            "Source:Current:READ:BACK OFF"
        )  # record preset source value instead of measuring it anew. NO CURRENT IS MEASURED!!! (Costs approx. 1.5 ms)
        self.keith.write("Volt:AZero OFF")  # turn off autozero
        self.keith.write("Source:Current:Delay:AUTO OFF")  # turn off autodelay

        # Set current mode indicator
        self.mode = "current"
        self.mutex.unlock()

    def reset(self):
        """
        reset instrument
        """
        self.mutex.lock()
        self.keith.write("*rst")
        self.keith.write(
            "Source:Current:VLimit " + str(100)
        )  # set voltage compliance to compliance
        self.mutex.unlock()

    def init_buffer(self, buffer_name, buffer_length):
        """
        Initialise buffer of source meter
        """
        self.mutex.lock()
        # if the buffer already exists, delete it first to prevent the error
        # "parameter error TRACe:MAKE cannot use an existing reading buffer name keithley"
        # try:
        # self.keith.write('TRACe:DELete "' + buffer_name + '"')
        # except:
        # cf.log_message("Buffer " + buffer_name + " does not exist yet")
        self.keith.write(
            'Trace:Make "' + buffer_name + '", ' + str(max(buffer_length, 10))
        )

        # Keithley empties the buffer
        self.keith.write("Trace:Clear " + '"' + buffer_name + '"')
        self.buffer_name = buffer_name
        self.mutex.unlock()

    def empty_buffer(self, buffer_name):
        """
        Function that empties the Keithley's buffer for the next run
        """
        self.mutex.lock()
        self.keith.write("Trace:Clear " + '"' + buffer_name + '"')
        self.mutex.unlock()

    def activate_output(self):
        """
        Activate output
        """
        self.mutex.lock()
        self.keith.write("Output ON")
        self.mutex.unlock()

    def deactivate_output(self):
        """
        Turn power off
        """
        self.mutex.lock()
        self.keith.write("Output OFF")
        self.mutex.unlock()

    def read_current(self):
        """
        Read current on Keithley source meter
        """
        return self.reverse * float(self.keith.query("MEASure:CURRent:DC?"))

    def read_voltage(self):
        """
        Read voltage on Keithley source meter
        """
        return self.reverse * float(self.keith.query("MEASure:VOLTage:DC?"))

    def read_buffer(self, buffer_name):
        return float(self.keith.query('Read? "' + buffer_name + '"')[:-1])

    def set_voltage(self, voltage):
        """
        Set the voltage on the source meter (only in voltage mode)
        """

        self.mutex.lock()
        voltage = float(voltage)
        if self.mode == "voltage":
            self.keith.write("Source:Volt " + str(self.reverse * voltage))
        else:
            logging.warning(
                "You can not set the voltage of the Keithley source in current mode"
            )
        self.mutex.unlock()

    def set_current(self, current):
        """
        Set the current on the source meter (only in current mode)
        """
        self.mutex.lock()
        current = float(current)
        # set current to source_value
        if self.mode == "current":
            self.keith.write("Source:Current " + str(self.reverse * current * 1e-3))
        else:
            logging.warning(
                "You can not set the current of the Keithley source in voltage mode"
            )
        self.mutex.unlock()


class KeithleyMultimeter:
    """
    Class that manages all functionality of our Keithley multi meter
    """

    def __init__(self, keithley_multimeter_address):
        # Define a mutex
        self.mutex = QtCore.QMutex(QtCore.QMutex.NonRecursive)

        # Keithley Finding Device
        rm = pyvisa.ResourceManager()
        # The actual addresses for the Keithleys can be accessed via rm.list_resources()
        visa_resources = rm.list_resources()

        if keithley_multimeter_address not in visa_resources:
            cf.log_message("The Multimeter seems to be absent or switched off.")
            raise IOError("The Multimeter seems to be absent or switched off.")

        self.keithmulti = rm.open_resource(keithley_multimeter_address)

        # Write operational parameters to Multimeter (Voltage from Photodiode)
        # reset instrument
        self.reset()

    def reset(self):
        """
        Reset instrument
        """
        self.mutex.lock()
        self.keithmulti.write("*rst")

        # Write operational parameters to Multimeter (Voltage from Photodiode)
        # sets the voltage range
        self.keithmulti.write("SENSe:VOLTage:DC:RANGe 10")
        # sets the voltage resolution
        self.keithmulti.query("VOLTage:DC:RESolution?")
        # sets the read-out speed and accuracy (0.01 fastest, 10 slowest but highest accuracy)
        self.keithmulti.write("VOLTage:NPLCycles 1")
        # sets the trigger to activate immediately after 'idle' -> 'wait-for-trigger'
        self.keithmulti.write("TRIGer:SOURce BUS")
        # sets the trigger to activate immediately after 'idle' -> 'wait-for-trigger'
        self.keithmulti.write("TRIGer:DELay 0")
        # Activate wait for trigger mode
        self.keithmulti.write("INITiate")
        self.mutex.unlock()

    # def set_fixed_range(self, value):
    #     """
    #     Sets a fixed voltage range if the user selected so
    #     """
    #     # Turn off the auto range function of the multimeter
    #     self.keithmulti.write("SENSe:VOLTage:DC:RANGe:AUTO OFF")
    #     # Set the range of the multimeter to a fixed value
    #     self.keithmulti.write("CONF:VOLTage:DC:RANGe " + str(value))

    # def set_auto_range(self):
    #     """
    #     Sets automatic detection of the multimeter range
    #     """
    #     # Turn on the auto range function of the multimeter
    #     self.keithmulti.write("SENSe:VOLTage:DC:RANGe:AUTO ON")

    def measure_voltage(self, multimeter_range=0):
        """
        Returns an actual voltage reading on the keithley multimeter
        """
        if multimeter_range == 0:
            return float(self.keithmulti.query("MEASure:VOLTage:DC?"))
        else:
            return float(
                self.keithmulti.query("MEASure:VOLTage:DC? " + str(multimeter_range))
            )
