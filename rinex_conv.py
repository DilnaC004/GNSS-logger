import os
import logging
import platform
import threading
import subprocess

from synchronize_data import synchronize_ftp, synchronize_usb

logger = logging.getLogger(__name__)

CURRENT_SYSTEM = platform.system()

if CURRENT_SYSTEM == "Windows":
    PROCESSING_PROGRAM = "convbin.exe"
    if not os.path.exists(PROCESSING_PROGRAM):
        raise Exception(
            f"{CURRENT_SYSTEM} -- This folder doesnt contain convbin.exe, its mandatory")
if CURRENT_SYSTEM == "Linux":
    PROCESSING_PROGRAM = "./convbin"
    if not os.path.exists(PROCESSING_PROGRAM):
        raise Exception(
            f"{CURRENT_SYSTEM} -- This folder doesnt contain convbin, its mandatory")
else:
    raise Exception(
        f"This operating system isnt supported -- {CURRENT_SYSTEM}")


class Convert2RinexAndSync(threading.Thread):
    '''
    The class with the method that take ".ubx" log file 
    and convert it to RINEX format.

    After that are all files synchronized.
    '''

    def __init__(self, log_file_path, project_directory="Test", ftp_acess=None, erase: bool = False, ignore_files: list = []):
        super().__init__()
        self._stop_event = threading.Event()
        self.log_file_path = log_file_path
        self.log_file_name = os.path.split(log_file_path)[-1]
        self.project_directory = project_directory
        self.ftp_acess = ftp_acess
        self.erase = erase
        self.ignore_files = ignore_files
        self.processing_program = PROCESSING_PROGRAM

    def check_folder(self):

        logging_rinex_dir = "RINEX"
        if not os.path.exists(logging_rinex_dir):
            try:
                os.mkdir(logging_rinex_dir)
            except OSError:
                logger.exception(
                    f"Creation of the directory {logging_rinex_dir} failed")
            else:
                logger.info(
                    f"Successfully created the directory {logging_rinex_dir}")

        logging_full_path = os.path.join(
            logging_rinex_dir, self.project_directory)

        if not os.path.exists(logging_full_path):
            try:
                os.mkdir(logging_full_path)
            except OSError:
                logger.exception(
                    f"Creation of the directory {logging_full_path} failed")
            else:
                logger.info(
                    f"Successfully created the directory {logging_full_path}")

    def run(self):
        try:
            self.check_folder()

            file_name_with_dir = os.path.join(
                self.project_directory, self.log_file_name)
            subprocess.run("{0} -od -os -oi -ot -f 2 -hc 'GNSS logger application' -o ./RINEX/{1}.obs ./LOGS/{1}.ubx".format(
                self.processing_program, file_name_with_dir[0:-4]), shell=True)
        except Exception:
            logger.exception(
                "Some error in converting ubx to RINEX file")

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
                synchronize_ftp(
                    self.ftp_acess, self.project_directory, self.erase, self.ignore_files)

            logger.info("============================\n")
        except Exception:
            logger.exception(
                "Some error in synchronization data on ftp or USB")
            logger.info("============================\n")
