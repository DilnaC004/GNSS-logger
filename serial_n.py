import os
import re
import serial
import logging
import pynmea2
import threading
from rinex_conv import Convert2RinexAndSync

logger = logging.getLogger(__name__)


class SerialNmeaRead(threading.Thread):
    '''
    The class with the method that reads the serial port in the backgroud.
    '''

    def __init__(self, directory: str, com_port: str, baudrate: int = 38400, ftp_acess: str = None, erase: bool = False, compress: bool = False):
        super().__init__()
        self._stop_event = threading.Event()
        self.directory = directory
        self.serial_object = serial.Serial(com_port, int(baudrate))
        self.ftp_acess = ftp_acess
        self.file_name = ""
        self.erase = erase
        self.compress = compress

    def define_file_name(self, ZDA_file_name: str):

        logging_dir = os.path.join("LOGS", self.directory)
        if not os.path.exists(logging_dir):
            try:
                os.makedirs(logging_dir)
            except OSError:
                logger.exception(
                    f"Creation of the directory {logging_dir} failed")
            else:
                logger.info(
                    f"Successfully created the directory {logging_dir}")

        actual_file_name = os.path.join(
            logging_dir, ZDA_file_name)

        actual_file_str = f"Actual logging file is {actual_file_name} ."

        if self.file_name == "":
            self.file_name = actual_file_name

            logger.info(actual_file_str)
            print(actual_file_str)

        elif self.file_name != actual_file_name:
            logger.info(actual_file_str)
            print(actual_file_str)

            old_file_name = self.file_name
            # update new name
            self.file_name = actual_file_name
            # convert *.ubx log to RINEX and synchronize data
            Convert2RinexAndSync(
                old_file_name, self.directory, self.ftp_acess, self.erase, [self.file_name], self.compress).start()

    def get_ZDA_timestamp(self, serial_data: str):

        match = re.search("\$GNZDA.*\*..", serial_data)

        if match:
            ZDA_message = serial_data[match.start():match.end()]
            ZDA_parse = pynmea2.parse(ZDA_message)

            # if develop True, files will be separated after 10 minutes
            BOOL_DEVELOP = False

            if BOOL_DEVELOP:
                ZDA_file_name = f"{ZDA_parse.year}_{ZDA_parse.month}_{ZDA_parse.day}_{str(ZDA_parse.timestamp)[0:2]}_{str(ZDA_parse.timestamp)[3]}0_00.ubx"
            else:
                ZDA_file_name = f"{ZDA_parse.year}_{ZDA_parse.month}_{ZDA_parse.day}_{str(ZDA_parse.timestamp)[0:2]}_00_00.ubx"

            self.define_file_name(ZDA_file_name)

    def get_GGA_timestamp(self, serial_data: str):

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
            try:
                serial_data = self.serial_object.readline()

                self.get_ZDA_timestamp(
                    serial_data.decode("ascii", errors="replace"))

                if self.file_name != "":
                    # open file as append-binary
                    with open(self.file_name, "ab") as f:
                        f.write(serial_data)

            except Exception:
                logger.exception(f"Some error in data: {serial_data}")

    def stop(self):
        self._stop_event.set()
        self.serial_object.close()

    def stopped(self):
        return self._stop_event.is_set()
