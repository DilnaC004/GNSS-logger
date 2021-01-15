import os
import git
import urllib.request


def synchronize_data():
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
        print("Git - Current folder isn't Git repository")
        return False


if __name__ == "__main__":
    synchronize_data()
