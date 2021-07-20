import threading
import subprocess
import os
from synchronize_data import synchronize_git, synchronize_ftp, synchronize_usb


class Convert2RinexAndSync(threading.Thread):
    '''
    The class with the method that take ".ubx" log file 
    and convert it to RINEX format.

    After that are all files synchronized.
    '''

    def __init__(self, log_file_name, directory="Test", ftp_acess=None):
        super().__init__()
        self._stop_event = threading.Event()
        self.log_file_name = log_file_name
        self.directory = directory
        self.ftp_acess = ftp_acess

    def check_folder(self):

        logging_path = "RINEX"
        if not os.path.exists(logging_path):
            try:
                os.mkdir(logging_path)
            except OSError:
                print("Creation of the directory {} failed".format(logging_path))
            else:
                print("Successfully created the directory {}".format(logging_path))

    def run(self):

        self.check_folder()
        print(self.log_file_name[5:-4])
        subprocess.run("convbin -od -os -oi -ot -f 2 -hc 'GNSS logger application' -o ./RINEX/{0}.obs -n ./RINEX/{0}.nav -g ./RINEX/{0}.gnav ./LOGS/{0}.ubx".format(
            self.log_file_name[5:-4]), shell=True)
        self.stop()

    def stop(self):
        self._stop_event.set()
        print("Converting to RINEX is done:")
        print("============================")
        try:
            # synchronize_git()
            synchronize_usb(
                "./RINEX/" + self.log_file_name[5:-4] + ".*", self.directory)
            synchronize_usb(self.log_file_name, self.directory)
            synchronize_ftp(
                "./RINEX/" + self.log_file_name[5:-4] + ".*", self.directory)
            synchronize_ftp(self.log_file_name, self.directory)
            print("============================\n")
        except Exception as err:
            print("Some error in synchronization data on git or USB")
            print(err)
            print("============================\n")
