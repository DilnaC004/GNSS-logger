import threading
import subprocess
import os
from git_comunication import synchronize_data


def save_file_to_USB(file_name):

    USBs = connected_USB()

    for usb in USBs:
        try:
            out = subprocess.check_output(
                "cp {} {}".format(file_name, usb), shell=True)
        except:
            print("Some error in copying files {}".format(file_name))
            print(out)
        pass


def connected_USB():
    ''' Function which find all connected USB and return their list.'''
    usb = []

    try:
        out = subprocess.check_output(
            'lsblk | grep sd | grep /media', shell=True).decode('ascii')

        for line in out.split('\n'):
            splitted = line.split()
            if len(splitted) > 1 and splitted[-1] != "":
                usb.append(line.split()[-1])

        return usb

    except:
        print("Some error in finding connected USBs")
        return []


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
        synchronize_data()
        save_file_to_USB("./RINEX/" + self.log_file_name[5:-4] + ".*")
        print("Synchronizing is done:")
        print("============================\n")
