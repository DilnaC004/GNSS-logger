import os
import argparse
from datetime import datetime


def find_files_in_directory(path: str, max_age: int):

    folders = []
    files = []

    dt_now = datetime.now()

    if not os.path.exists(path):
        return []

    for f in os.scandir(path):

        if f.is_dir():
            folders.append(f)

        if f.is_file() and (dt_now - datetime.fromtimestamp(f.stat().st_mtime)).days >= max_age:
            files.append(f.path)

    for F in folders:
        files_nested = find_files_in_directory(F.path, max_age)
        files.extend(files_nested)

    return files


def main(days: int):

    log_files = find_files_in_directory("./LOGS", max_age=days)
    rnx_files = find_files_in_directory("./RINEX", max_age=days)

    for path in [*log_files, *rnx_files]:
        try:
            print(f"File {path} was removed")
            os.remove(path)
        except Exception as error:
            print(f"File {path} cannot be removed:")
            print(error)


if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--days", default=60,
                    help="Files in directories LOGS and RINEX, which are older than input count of days will be deleted. Defaults 30 days")
    args = ap.parse_args()

    main(int(args.days))
