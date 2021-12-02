from PySide2 import QtCore
import core_functions as cf
import time

from hardware import (
    KeithleySource,
    KeithleyMultimeter,
)
from tests.tests import (
    MockKeithleySource,
    MockKeithleyMultimeter,
)


class InitThread(QtCore.QThread):
    """
    Worker thread that is only meant to do the initialisation, before the program is started
    """

    update_loading_dialog = QtCore.Signal(int, str)
    kill_dialog = QtCore.Signal()
    ask_retry = QtCore.Signal()
    emit_source = QtCore.Signal(KeithleySource)
    emit_multimeter = QtCore.Signal(KeithleyMultimeter)

    def __init__(self, widget=None):
        super(InitThread, self).__init__()

        # Connect signals
        self.update_loading_dialog.connect(widget.update_loading_dialog)
        self.kill_dialog.connect(widget.kill_dialog)
        self.ask_retry.connect(widget.ask_retry)
        self.emit_source.connect(widget.parent.init_source)
        self.emit_multimeter.connect(widget.parent.init_multimeter)
        self.widget = widget

        # Variable that checks if initialisation shall be repeated
        self.repeat = False

    def run(self):
        """
        Function that initialises the parameters before the main program is called
        """
        import pydevd

        pydevd.settrace(suspend=False)

        # self.update_loading_dialog.emit("Test")
        # Read global settings first (what if they are not correct yet?)

        global_settings = cf.read_global_settings()

        # Check if Keithley source is on and can be used
        try:
            keithley_source = KeithleySource(
                global_settings["keithley_source_address"],
                100,
            )
            cf.log_message("Keithley SourceMeter successfully initialised")
            keithley_source_init = True
        except Exception as e:
            keithley_source = MockKeithleySource(
                global_settings["keithley_source_address"],
                100,
            )
            cf.log_message(
                "The Keithley SourceMeter could not be initialised! Please reconnect the device and check the serial number in the settings file!"
            )
            cf.log_message(e)
            keithley_source_init = False

        self.emit_source.emit(keithley_source)

        time.sleep(0.1)
        self.update_loading_dialog.emit(50, "Checking for Keithley multimeter")

        # Check if Keithley multimeter is present
        try:
            keithley_multimeter = KeithleyMultimeter(
                global_settings["keithley_multimeter_address"]
            )
            cf.log_message("Keithley Multimeter successfully initialised")
            keithley_multimeter_init = True
        except Exception as e:
            keithley_multimeter = MockKeithleyMultimeter(
                global_settings["keithley_multimeter_address"]
            )
            cf.log_message(
                "The Keithley Multimeter could not be initialised! Please reconnect the device and check the serial number in the settings file!"
            )
            cf.log_message(e)
            keithley_multimeter_init = False

        time.sleep(0.1)
        self.emit_multimeter.emit(keithley_multimeter)

        # If one of the devices could not be initialised for whatever reason,
        # ask the user if she wants to retry after reconnecting the devices or
        # continue without some of the devices
        if keithley_source_init == False or keithley_multimeter_init == False:
            device_not_loading_message = []
            if keithley_source_init == False:
                device_not_loading_message.append("Source")
            if keithley_multimeter_init == False:
                device_not_loading_message.append("Multimeter")

            if (
                len(device_not_loading_message) > 1
                and len(device_not_loading_message) < 5
            ):
                a = ", ".join(device_not_loading_message[:-1])
                b = a + " and " + device_not_loading_message[-1]
            elif len(device_not_loading_message) == 1:
                b = device_not_loading_message[0]
            elif len(device_not_loading_message) == 5:
                b = "None"

            c = b + " could not be initialised."

            if len(device_not_loading_message) == 5:
                c = "None of the devices could be initialised."

            self.update_loading_dialog.emit(
                100,
                c,
            )
            self.ask_retry.emit()

        else:
            self.update_loading_dialog.emit(100, "One more moment")
            time.sleep(0.5)
            self.kill_dialog.emit()
