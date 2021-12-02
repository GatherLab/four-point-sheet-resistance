import psutil
import numpy as np


class MockKeithleySource:
    """
    Mock class for testing
    """

    def __init__(self, keithley_source_address, current_compliance):
        print(keithley_source_address + str(current_compliance))

    def as_voltage_source(self, current_compliance):
        print("Keithley initialised as voltage source")

    def as_current_source(self, voltage_compliance):
        print("Keithley initialised as current source")

    def reset(self):
        print("Keithley source resetted")

    def init_buffer(self, buffer_name, buffer_length):
        print("Buffer written")

    def empty_buffer(self, buffer_name):
        print("MockKeithleySource buffer emptied")

    def activate_output(self):
        print("Output activated")

    def deactivate_output(self):
        print("output deactivated")

    def read_current(self):
        return float(psutil.cpu_percent() / 100)

    def read_voltage(self):
        return float(psutil.cpu_percent() / 100)

    def set_voltage(self, voltage):
        print("Voltage set to " + str(voltage))

    def set_current(self, current):
        print("Current set to " + str(current))


class MockKeithleyMultimeter:
    """
    Mock class for testing
    """

    def __init__(self, keithley_multimeter_address):
        print(keithley_multimeter_address)

    def reset(self):
        print("Multimeter resetted")

    def set_fixed_range(self, value):
        print("Fixed range set")

    def set_auto_range(self):
        print("Auto range set")

    def measure_voltage(self):
        # print("Voltage read")
        return np.random.rand(1)[0]