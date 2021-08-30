#!/usr/bin/python3
from __future__ import print_function
import argparse
import signal
import time
from httplib2 import error
from agribot_common.logs_backup.change_log_handler import ChangeLog
from agribot_common.logs_backup.graceful_killer import Killer


def main():
    killer = Killer()
    parser = argparse.ArgumentParser(description='Upload logs into drive.')
    parser.add_argument('-p',
                        metavar="PATH_TO_LOGS",
                        required=False,
                        default='/home/agribot1/logs',
                        help="Path to folder to be uploaded to Drive.")
    parser.add_argument('-k',
                        metavar="PATH_TO_KEY",
                        required=False,
                        default='/home/agribot1/agribot/configs/base/drive_api_key/',
                        help="Path to the folder which contains the drive_api_key.")
    parser.add_argument('-yaml',
                        metavar="PATH_TO_YAML_FILE",
                        required=False,
                        default="/home/agribot1/agribot/configs/base/robot.yaml",
                        help="Path to yaml file containing robots serial number (RSN).")
    args = parser.parse_args()
    path = args.p
    key = args.k
    path_to_yaml = args.yaml
    handler = ChangeLog(killer, path_to_yaml_file=path_to_yaml)
    handler.check_for_token_from_path(key)

    # Recursively uploading all files and folders in given directory
    while not killer.kill_now:
        try:
            handler.log_changes_in_directory(path=path)
            time.sleep(1)
        except OSError as err:
            killer.exception_message = str(err)
            killer.kill_now = True
        except error.HttpLib2Error as err:
            killer.exception_message = str(err)
            killer.kill_now = True

    print("Exited successfully.")


if __name__ == "__main__":
    main()
