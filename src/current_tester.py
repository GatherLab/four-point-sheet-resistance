from PySide2 import QtCore

from hardware import KeithleySource, KeithleyMultimeter

from tests.tests import MockKeithleySource, MockKeithleyMultimeter

# for testing reasons
import time


class CurrentTester(QtCore.QThread):
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
    update_ammeter_signal = QtCore.Signal(float)
    update_voltage_signal = QtCore.Signal(float)

    def __init__(
        self,
        keithley_multimeter,
        keithley_source,
        parent=None,
    ):

        super(CurrentTester, self).__init__()

        self.is_killed = False
        self.pause = False

        # Reset Arduino and Keithley
        self.keithley_multimeter = keithley_multimeter
        self.keithley_source = keithley_source

        # Connect signal to the updater from the parent class
        self.update_ammeter_signal.connect(parent.update_ammeter)
        self.update_voltage_signal.connect(parent.update_voltage)

    def run(self):
        """
        Class that continuously reads the current on the Keithley source and
        communicates with the main class. It has to be kept in separate
        classes to allow for threading. It is started with the .start()
        method from the QThread class
        """
        import pydevd

        pydevd.settrace(suspend=False)

        while True:
            current_reading = self.keithley_source.read_current()
            self.update_ammeter_signal.emit(current_reading)

            voltage_reading = self.keithley_multimeter.measure_voltage()
            self.update_voltage_signal.emit(voltage_reading)

            time.sleep(0.5)

            if self.pause:
                while True:
                    time.sleep(0.5)

                    if not self.pause:
                        break

            if self.is_killed:
                self.quit()
                break

    def kill(self):
        """
        Kill this thread by stopping the loop
        """
        # Turn arduino relays off
        # self.keithley_multimeter.trigger_relay(0)
        # self.keithley_multimeter.close_serial_connection()

        # Turn keithley off
        self.keithley_source.deactivate_output()
        self.pause = False

        # Trigger interruption of run sequence
        self.is_killed = True
