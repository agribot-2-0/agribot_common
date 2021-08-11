#!/usr/bin/python3
import os
import yaml
from agribot_common.logs_backup.drive_api_handler import DriveApiHandler


class ChangeLog:  # pylint: disable=old-style-class
    def __init__(self, path_to_yaml_file=None):
        self._drive_handler = DriveApiHandler()
        self._file_id = None
        self._rsn = None
        with open(path_to_yaml_file) as yaml_file:
            self._rsn = yaml.load(yaml_file, Loader=yaml.FullLoader)['rsn']

    def check_for_token_from_path(self, new_key):
        self._drive_handler.check_for_token(new_key)
        self.initiate_file_id()

    def initiate_file_id(self):
        directories = self._drive_handler.get_directory_list()
        directory = next((dir for dir in directories if dir["name"] == "Logs" + str(self._rsn)),
                         None)

        if directory is None:
            self._file_id = self._drive_handler.create_directory(name="Logs" + str(self._rsn))
        else:
            self._file_id = directory["id"]

    def log_changes_in_directory(self, path, dir_id=None):
        if dir_id is None:
            dir_id = self._file_id

        local_dir_list = [
            path_name for path_name in os.listdir(path)
            if os.path.isdir(os.path.join(path, path_name))
        ]
        local_file_list = [
            path_name for path_name in os.listdir(path)
            if os.path.isfile(os.path.join(path, path_name))
        ]
        remote_dir_list = [
            path_name['name'] for path_name in self._drive_handler.get_directory_list(parent=dir_id)
        ]
        remote_file_list = [
            path_name['name'] for path_name in self._drive_handler.get_file_list(parent=dir_id)
        ]

        for local_file in local_file_list:
            if local_file not in remote_file_list:
                self._drive_handler.create_txt_file(path=path, name=local_file, parent=dir_id)

        for local_directory in local_dir_list:
            if local_directory not in remote_dir_list:
                self._drive_handler.create_directory(name=local_directory, parent=dir_id)

        remote_dir_list_with_id = [
            name for name in self._drive_handler.get_directory_list(parent=dir_id)
        ]

        for remote_directory in remote_dir_list_with_id:
            self.log_changes_in_directory(path=os.path.join(path, remote_directory['name']),
                                          dir_id=remote_directory['id'])
