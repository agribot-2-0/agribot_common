from __future__ import print_function
from drive_api_handler import DriveApiHandler
from change_log_handler import ChangeLog
import argparse


def main():
    parser = argparse.ArgumentParser(description='Upload logs into drive.')
    parser.add_argument('-p',
                        metavar="PATH_TO_LOGS",
                        required=False,
                        default='/home/agribot1/',
                        help="Path to folder 'logs' Must be full path, e.g. /home/agribot/")
    parser.add_argument('-f',
                        metavar="FOLDER_NAME",
                        required=False,
                        default='logs',
                        help="Name of the folder which contains logs, default = logs")
    parser.add_argument(
        '-k',
        metavar="PATH_TO_KEY",
        required=False,
        default='/home/agribot1/agribot/configs/base/drive_api_key/',
        help=
        "Path to the folder which contains the drive_api_key. Key must me named 'credentials.json'."
    )
    args = parser.parse_args()
    path = args.p
    dir = args.f
    key = args.k
    handler = ChangeLog()
    handler.setDir(dir)
    handler.setPath(path)
    handler.setKeyPath(key)

    # SEARCHING IN LOCAL FOLDERS FOR TILL IN HOUR FOLDERS
    while True:
        handler.logChangesInFolder()


if __name__ == "__main__":
    main()
