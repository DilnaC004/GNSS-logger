import time
import serial
import threading
import pynmea2
import os
import re
from git_comunication import synchronize_data


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

        str_date = time.strftime("%Y_%m_%d", time.localtime()+3600)
        # predelat na hodiny# delete seconds
        str_time = str(gga_time)[0:-3].replace(":", "_")
        new_file_name = logging_path + os.path.sep + str_date + "_" + str_time + ".log"

        if self.file_name == "":
            self.file_name = new_file_name
        elif self.file_name != new_file_name:
            self.file_name = new_file_name
            # synchronize_data()
            print("odeslani starych dat na git")

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
            serial_data = self.serial_object.readline().decode('ascii')

            try:

                self.get_GGA_timestamp(serial_data)

                if self.file_name != "":
                    with open(self.file_name, "a", encoding="utf-8") as f:
                        f.write(serial_data.strip("\n"))

            except:
                print('Some error in data: ', serial_data)

    def stop(self):
        self._stop_event.set()
        self.serial_object.close()

    def stopped(self):
        return self._stop_event.is_set()


serial_thread = SerialNmeaRead('COM5', 38400)
serial_thread.start()

x = input('Enter anything to cancel window:\n')

serial_thread.stop()
print("Thread stopped.")
