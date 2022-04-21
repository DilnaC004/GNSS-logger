import threading
import subprocess
import os
import logging
from synchronize_data import synchronize_ftp, synchronize_usb

logger = logging.getLogger(__name__)

if not os.path.exists("convbin.exe"):
    raise Exception("This folder doesnt contain convbin.exe, its mandatory")


class Convert2RinexAndSync(threading.Thread):
    '''
    The class with the method that take ".ubx" log file 
    and convert it to RINEX format.

    After that are all files synchronized.
    '''

    def __init__(self, log_file_path, project_directory="Test", ftp_acess=None, erase: bool = False):
        super().__init__()
        self._stop_event = threading.Event()
        self.log_file_path = log_file_path
        self.log_file_name = os.path.split(log_file_path)[-1]
        self.project_directory = project_directory
        self.ftp_acess = ftp_acess
        self.erase = erase

    def check_folder(self):

        logging_rinex_dir = "RINEX"
        if not os.path.exists(logging_rinex_dir):
            try:
                os.mkdir(logging_rinex_dir)
            except OSError:
                logger.exception("Creation of the directory {} failed".format(
                    logging_rinex_dir))
            else:
                logger.info("Successfully created the directory {}".format(
                    logging_rinex_dir))

        logging_full_path = os.path.join(
            logging_rinex_dir, self.project_directory)

        if not os.path.exists(logging_full_path):
            try:
                os.mkdir(logging_full_path)
            except OSError:
                logger.exception("Creation of the directory {} failed".format(
                    logging_full_path))
            else:
                logger.info("Successfully created the directory {}".format(
                    logging_full_path))

    def run(self):

        self.check_folder()

        file_name_with_dir = os.path.join(
            self.project_directory, self.log_file_name)
        subprocess.run("convbin -od -os -oi -ot -f 2 -hc 'GNSS logger application' -o ./RINEX/{0}.obs ./LOGS/{0}.ubx".format(
            file_name_with_dir[0:-4]), shell=True)
        self.stop()

    def stop(self):
        self._stop_event.set()
        logger.info("Converting to RINEX is done:")
        logger.info("============================")
        try:
            synchronize_usb(
                os.path.join("RINEX", self.project_directory, self.log_file_name[:-4]) + ".obs", self.project_directory)
            synchronize_usb(self.log_file_path, self.project_directory)
            if self.ftp_acess is not None:
                synchronize_ftp(self.ftp_acess, self.project_directory, self.erase)
                
            logger.info("============================\n")
        except Exception:
            logger.exception(
                "Some error in synchronization data on ftp or USB")
            logger.info("============================\n")
