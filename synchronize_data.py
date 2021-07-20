import os
import git
import urllib.request
import subprocess


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


def synchronize_ftp(file_name, directory=""):

    if internet_connection():
        print("File {} was saved to ftp".format(file_name))
    else:
        print("Cannot synchronize data to FTP - no internet connection")


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
