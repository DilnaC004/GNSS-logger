import os
import git
import urllib.request
import subprocess
import logging
from ftplib import FTP

MAIN_DIR = "GNSS_LOGGER"

logger = logging.getLogger(__name__)

def synchronize_git():
    '''
    Function check if actual directory is Git repository and
    if is, synchronize all untracked files to remote repository.
    '''
    if check_git_directory():
        # Initialize repository
        r = git.Repo.init(os.path.curdir)
        # Find untracked files and idexing them
        untracked_files = r.untracked_files
        if len(untracked_files) > 0:
            for uF in untracked_files:
                r.index.add(uF)
            # Create commit
            r.index.commit("Upload new data logs")
            # Upload data to remote Repository - nutne otestovat co se stane, kdyz neni internet
            if internet_connection():
                r.remotes.origin.push()
                logger.info("Git - New files uploaded : {}".format(untracked_files))
            else:
                logger.error("Git - Cannot synchronize data - no internet connection")

        else:
            logger.info("Git - No changes in repository")


def internet_connection(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False


def check_git_directory():

    if os.path.isdir(".git"):
        return True
    else:
        logger.info("Git - Current directory isn't Git repository")
        return False


def synchronize_ftp(ftp_acess, directory=""):

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

                unsync_files = compare_files_pc_ftp(
                    log_files, rnx_files, ftp_files, directory)

                for file_path in unsync_files:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as file:
                            try:
                                ftp.storbinary(
                                    "STOR {}".format(os.path.basename(file_path)), file)
                                logger.info("File {} was saved to ftp".format(file_path))
                            except Exception:
                                logger.exception(
                                    "Problem with saving file {} on ftp".format(file_path))

                    else:
                        logger.error("File {} doesnt exist".format(file_path))
        except Exception:
            logger.exception("Some error in sync data to ftp ")
    else:
        logger.info("Cannot synchronize data to FTP - no internet connection or ftp access")


def synchronize_usb(file_path, directory=""):

    USBs = connected_USB()

    for usb in USBs:
        try:
            usb_folder_path = os.path.join(usb, MAIN_DIR, directory)
            # try to create all folders
            os.makedirs(usb_folder_path, exist_ok=True)
            # copy files
            out = subprocess.check_output(
                "cp {} {}".format(file_path, usb_folder_path), shell=True)
            logger.info("File {} was saved to usb {}".format(
                file_path, usb_folder_path))
        except:
            logger.exception("Some error in copying files {}".format(file_path))


def get_files_pc_folder(path):
    return next(os.walk(path), (None, None, []))[2]


def compare_files_pc_ftp(pc_log, pc_rnx, ftp_all, directory):

    no_sync_files = []

    for f in pc_log:
        if not (f in ftp_all):
            no_sync_files.append(os.path.join("LOGS", directory, f))

    for f in pc_rnx:
        if not (f in ftp_all):
            no_sync_files.append(os.path.join("RINEX", directory, f))

    return no_sync_files


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
