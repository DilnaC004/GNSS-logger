import os
import urllib.request
import subprocess
import logging
from ftplib import FTP

MAIN_DIR = "GNSS_LOGGER"

logger = logging.getLogger(__name__)


def internet_connection(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False


def synchronize_ftp(ftp_acess, directory="", erase: bool = False, ignore_files: list = []):
    """FTP sync function

    Args:
        ftp_acess (_type_): <server_adress>::<user_name>::<password>
        directory (str, optional): Path to directory which has to be synchronize. Defaults to "".
        erase (bool, optional): Delete files after synchronization. Defaults to False.
        ignore_files (list, optional): Ignore files to synchronization, mainly use for actual loging file . Defaults to [].
    """
    if internet_connection() and ftp_acess:

        try:
            host, user, passwd = ftp_acess.split("::")

            with FTP(host=host, user=user, passwd=passwd) as ftp:

                # check if exist GNSS_LOGGER directory
                if MAIN_DIR not in ftp.nlst():
                    ftp.mkd(MAIN_DIR)

                ftp.cwd(MAIN_DIR)

                # check if exist project directory
                if directory != "" and (directory not in ftp.nlst()):
                    ftp.mkd(directory)

                ftp.cwd(directory)

                # get all unsync files
                rnx_files = get_files_pc_folder(
                    os.path.join("RINEX", directory))
                log_files = get_files_pc_folder(
                    os.path.join("LOGS", directory))
                ftp_files = ftp.nlst()

                sync_files, unsync_files = compare_files_pc_ftp(
                    log_files, rnx_files, ftp_files, directory)

                # SYNCHRONIZATION UNSYNC FILES TO FTP
                for file_path in (f for f in unsync_files if f not in ignore_files):
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as file:
                            try:
                                base_name = os.path.basename(file_path)

                                ftp.storbinary(f"STOR {base_name}", file)
                                logger.info(
                                    f"File {file_path} was saved to ftp")

                            except Exception:
                                logger.exception(
                                    f"Problem with saving file {file_path} on ftp")
                    else:
                        logger.error(f"File {file_path} doesnt exist")

                # DELETE SYNC FILES FROM LOCAL STORAGE
                if erase:
                    for deleting_path in (d for d in sync_files if d not in ignore_files):
                        try:
                            base_name = os.path.basename(deleting_path)
                            # check if file is completely uploaded
                            if ftp.size(base_name) == os.path.getsize(deleting_path):
                                os.remove(deleting_path)
                                logger.info(
                                    f"File {deleting_path} was deleted")
                            else:
                                logger.error(
                                    f"File {base_name} wasnt completely uploaded, deletion was postponed")
                        except Exception:
                            logger.exception(
                                f"Problem with deleting file {deleting_path}")
        except Exception:
            logger.exception("Some error in sync data to ftp ")
    else:
        logger.info(
            "Cannot synchronize data to FTP - no internet connection or ftp access")


def synchronize_usb(file_path, directory=""):

    USBs = connected_USB()

    for usb in USBs:
        try:
            usb_folder_path = os.path.join(usb, MAIN_DIR, directory)
            # try to create all folders
            os.makedirs(usb_folder_path, exist_ok=True)
            # copy files
            subprocess.check_output(
                f"cp {file_path} {usb_folder_path}", shell=True)
            logger.info(f"File {file_path} was saved to usb {usb_folder_path}")
        except:
            logger.exception(
                f"Some error in copying files {file_path}")


def get_files_pc_folder(path):
    return next(os.walk(path), (None, None, []))[2]


def compare_files_pc_ftp(pc_log, pc_rnx, ftp_all, directory):

    no_sync_files = []
    sync_files = []

    for f in pc_log:
        log_path = os.path.join("LOGS", directory, f)
        if not (f in ftp_all):
            no_sync_files.append(log_path)
        else:
            sync_files.append(log_path)

    for f in pc_rnx:
        rnx_path = os.path.join("RINEX", directory, f)
        if not (f in ftp_all):
            no_sync_files.append(rnx_path)
        else:
            sync_files.append(rnx_path)

    return sync_files, no_sync_files


def connected_USB():
    ''' Function which find all connected USB and return their list.'''
    usb = []

    try:
        out = subprocess.check_output(
            'lsblk | grep sd | grep /media', shell=True).decode('utf-8')

        for line in out.split('\n'):
            splitted = line.split()
            if len(splitted) > 1 and splitted[-1] != "":
                usb.append(line.split()[-1])

        return usb

    except Exception:
        logger.error("Cannot find any connected USBs")
        return []


if __name__ == "__main__":
    print(connected_USB())

    for u in connected_USB():
        print(f"USB -- {u}")
