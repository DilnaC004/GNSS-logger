import time
import serial
import threading
import pynmea2
import os
import re
from rinex_conv import Convert2RinexAndSync


class SerialNmeaRead(threading.Thread):
    '''
    The class with the method that reads the serial port in the backgroud.
    '''

    def __init__(self, com_port, baudrate=38400):
        super().__init__()
        self._stop_event = threading.Event()
        self.serial_object = serial.Serial(com_port, baudrate)
        self.file_name = ""

    def define_file_name(self, gga_time):

        logging_path = "LOGS"
        if not os.path.exists(logging_path):
            try:
                os.mkdir(logging_path)
            except OSError:
                print("Creation of the directory %s failed" % logging_path)
            else:
                print("Successfully created the directory %s " % logging_path)

        str_date = time.strftime("%Y_%m_%d", time.localtime())
        # predelat na hodiny# delete seconds
        str_time = str(gga_time)[0:-3].replace(":", "_")
        new_file_name = logging_path + os.path.sep + str_date + "_" + str_time + ".ubx"

        if self.file_name == "":
            self.file_name = new_file_name
        elif self.file_name != new_file_name:
            old_file_name = self.file_name
            # update new name
            self.file_name = new_file_name
            # convert *.ubx log to RINEX and synchronize data
            Convert2RinexAndSync(old_file_name).start()

    def get_GGA_timestamp(self, serial_data):

        match = re.search("\$GNGGA.*\*..", serial_data)

        if match:
            GGA_message = serial_data[match.start():match.end()]
            GGA_parse = pynmea2.parse(GGA_message)
            self.define_file_name(GGA_parse.timestamp)

    def run(self):
        '''
        The method that actually gets data from the port
        '''
        while not self.stopped():
            serial_data = self.serial_object.readline()

            try:

                self.get_GGA_timestamp(
                    serial_data.decode("ascii", errors="replace"))

                if self.file_name != "":
                    with open(self.file_name, "ab") as f:
                        f.write(serial_data)

            except:
                print('Some error in data: ', serial_data)

    def stop(self):
        self._stop_event.set()
        self.serial_object.close()

    def stopped(self):
        return self._stop_event.is_set()


serial_thread = SerialNmeaRead('/dev/ttyACM2', 38400)
serial_thread.start()

x = input('Enter anything to cancel window:\n')

serial_thread.stop()
print("Thread stopped.")
