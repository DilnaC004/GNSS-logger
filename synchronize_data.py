import os
import git
import urllib.request
import subprocess
from ftplib import FTP


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
                print("Git - New files uploaded :", untracked_files)
            else:
                print("Git - Cannot synchronize data - no internet connection")

        else:
            print("Git - No changes in repository")


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
        print("Git - Current directory isn't Git repository")
        return False


def synchronize_ftp(ftp_acess, file_names, directory=""):

    if isinstance(file_names, list):
        file_names = [file_names]

    if internet_connection() and ftp_acess:

        try:
            host, user, passwd = ftp_acess.split("|")

            with FTP(host=host, user=user, passwd=passwd) as ftp:

                # check if exist GNSS_LOGGER directory
                main_logger_dir = "GNSS_LOGGER"
                if main_logger_dir not in ftp.nlst():
                    ftp.mkd(main_logger_dir)

                ftp.cwd(main_logger_dir)

                # check if exist project directory
                if directory != "" and (directory not in ftp.nlst()):
                    ftp.mkd(directory)

                ftp.cwd(directory)

                for file_name in file_names:

                    if os.path.exists(file_name):
                        with open(file_name, 'rb') as file:
                            try:
                                ftp.storbinary(
                                    "STOR {}".format(file_name), file)
                                print("File {} was saved to ftp".format(file_name))
                            except:
                                print(
                                    "Problem with saving file {} on ftp".format(file_name))
                    else:
                        print("File {} doesnt exist".format(file_name))
        except Exception as error:
            print("Some error in sync data to ftp :\n{}".format(error))
    else:
        print("Cannot synchronize data to FTP - no internet connection or ftp access")


def synchronize_usb(file_name, directory=""):

    USBs = connected_USB()

    for usb in USBs:
        try:
            out = subprocess.check_output(
                "cp {} {}".format(file_name, os.path.join(usb, directory)), shell=True)
            print("File {} was saved to usb {}".format(file_name, usb))
        except:
            print("Some error in copying files {}".format(file_name))
            print(out)
        pass


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

    except Exception as err:
        print("Some error in finding connected USBs")
        print(err)
        return []


if __name__ == "__main__":
    print(connected_USB())
