#!/usr/bin/python3
from __future__ import print_function
import hashlib
import os
import yaml
from agribot_common.logs_backup.drive_api_handler import DriveApiHandler


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as file_name:
        for chunk in iter(lambda: file_name.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


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
        directory = next((dir for dir in directories if dir["name"] == "agribot_log_backup"), None)

        if directory is None:
            self._file_id = self._drive_handler.create_directory(name="agribot_log_backup")
            self._file_id = self._drive_handler.create_directory(name=self._rsn,
                                                                 parent=self._file_id)
        else:
            self._file_id = directory["id"]
            directories = self._drive_handler.get_directory_list(parent=self._file_id)
            directory = next((dir for dir in directories if dir["name"] == self._rsn), None)

            if directory is None:
                self._file_id = self._drive_handler.create_directory(name=self._rsn,
                                                                     parent=self._file_id)
            else:
                self._file_id = directory["id"]

    def log_changes_in_directory(self, path, dir_id=None):

        print(path)
        if dir_id is None:
            dir_id = self._file_id

        local_dir_list = [
            local_dir for local_dir in os.listdir(path)
            if os.path.isdir(os.path.join(path, local_dir))
        ]
        local_file_list = [
            dict(name=local_file, checksum=md5(os.path.join(path, local_file)))
            for local_file in os.listdir(path) if os.path.isfile(os.path.join(path, local_file))
        ]
        remote_dir_list = [
            remote_dir['name']
            for remote_dir in self._drive_handler.get_directory_list(parent=dir_id)
        ]
        remote_file_list = [
            dict(name=remote_file['name'], checksum=remote_file['md5Checksum'])
            for remote_file in self._drive_handler.get_file_list(parent=dir_id)
        ]

        for local_file in local_file_list:
            if not any(remote_file['name'] == local_file['name']
                       for remote_file in remote_file_list):
                self._drive_handler.create_txt_file(path=path,
                                                    name=local_file['name'],
                                                    parent=dir_id)
            elif any((local_file["name"] == remote_file['name']
                      and local_file['checksum'] != remote_file['checksum'])
                     for remote_file in remote_file_list):
                self._drive_handler.update_txt_file(path=path,
                                                    name=local_file['name'],
                                                    parent=dir_id)

        for local_dir in local_dir_list:
            if local_dir not in remote_dir_list:
                self._drive_handler.create_directory(name=local_dir, parent=dir_id)

        remote_dir_list_with_id = [
            name for name in self._drive_handler.get_directory_list(parent=dir_id)
        ]

        for remote_dir in remote_dir_list_with_id:
            self.log_changes_in_directory(path=os.path.join(path, remote_dir['name']),
                                          dir_id=remote_dir['id'])
