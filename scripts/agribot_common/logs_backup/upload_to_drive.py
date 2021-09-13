#!/usr/bin/python3
import argparse
import time
from httplib2 import error
from agribot_common.logs_backup.change_log_handler import ChangeLog
from agribot_common.logs_backup.graceful_killer import Killer


def main():
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
    parser.add_argument('-t',
                        metavar="EXCEPTION_LOG_PERIOD",
                        required=False,
                        default=600,
                        help="Time after which the script will print which " +
                        "exception is being handled while in exception loop.")
    parser.add_argument('-i',
                        metavar="INTERVAL_BETWEEN_UPLOAD_MESSAGES",
                        default=600,
                        help="Time after which a message informing about the" +
                        " percentage of uploaded file data will be shown.")
    args = parser.parse_args()
    path = args.p
    key = args.k
    path_to_yaml = args.yaml
    timer = int(args.t)
    interval = args.i
    killer = Killer(time=timer)
    handler = ChangeLog(killer, time=timer, interval=interval, path_to_yaml_file=path_to_yaml)
    handler.initiate(key)

    # Recursively uploading all files and folders in given directory
    while not killer.kill_now:
        try:
            handler.log_changes_in_directory(path=path)
            time.sleep(1)
        except OSError as err:
            killer.add_exception(str(err))
            killer.kill_now = True
        except error.HttpLib2Error as err:
            killer.add_exception(str(err))
            killer.kill_now = True

    print("Exited successfully.")  # pylint: disable=superfluous-parens


if __name__ == "__main__":
    main()
