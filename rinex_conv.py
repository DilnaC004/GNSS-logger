import threading
import subprocess
import os
from git_comunication import synchronize_data


class Convert2RinexAndSync(threading.Thread):
    '''
    The class with the method that take ".ubx" log file 
    and convert it to RINEX format.

    After that are all files synchronized.
    '''

    def __init__(self, log_file_name):
        super().__init__()
        self._stop_event = threading.Event()
        self.log_file_name = log_file_name

    def check_folder(self):

        logging_path = "RINEX"
        if not os.path.exists(logging_path):
            try:
                os.mkdir(logging_path)
            except OSError:
                print("Creation of the directory %s failed" % logging_path)
            else:
                print("Successfully created the directory %s " % logging_path)

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
        # synchronize_data()
        print("Synchronizing is done:")
        print("============================\n")
