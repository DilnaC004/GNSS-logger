import os
import git


def synchronize_data():
    if check_git_directory():
        # inicitalizace repositare
        r = git.Repo.init(os.path.curdir)
        # vyhledani netrackovanych souboru
        untracked_files = r.untracked_files
        # vytvoreni commitu
        for uF in untracked_files:
            r.index.add(uF)
        # nahrani na server - nutne otestovat co se stane, kdyz neni internet

     #print("neco nefunguje")


def check_git_directory():

    if os.path.isdir(".git"):
        print("Current folder is Git repository")
        return True
    else:
        print("Current folder isn't Git repository")
        return False


if __name__ == "__main__":
    # print(os.path.curdir)
    # check_git_directory()
    synchronize_data()
