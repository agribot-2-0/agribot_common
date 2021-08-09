import time
import os
from drive_api_handler import DriveApiHandler


class ChangeLog:
    def __init__(self):
        self._drive_handler = DriveApiHandler()
        self._file_id = None
        self._path = None
        self._dir = None

    def set_dir(self, new_dir):
        self._dir = new_dir

    def set_path(self, new_path):
        self._path = os.path.join(new_path, self._dir)

    def check_for_token_from_path(self, new_key):
        self._drive_handler.check_for_token(new_key)
        self.set_file_id()

    def set_file_id(self):
        items = self._drive_handler.get_directory_list()

        if not items:
            self._file_id = self._drive_handler.create_directory()
        else:
            for item in items:
                if item["name"] == "Logs":
                    self._file_id = item["id"]
            if self._file_id == None:
                self._file_id = self._drive_handler.create_directory()

    def log_changes_in_directory(self, *, path=None, id=None):
        if path == None:
            path = self._path
        if id == None:
            id = self._file_id

        local_dir_list = [
            path_name for path_name in os.listdir(path)
            if os.path.isdir(os.path.join(path, path_name))
        ]
        local_file_list = [
            path_name for path_name in os.listdir(path)
            if os.path.isfile(os.path.join(path, path_name))
        ]
        remote_dir_list = [
            path_name['name'] for path_name in self._drive_handler.get_directory_list(parent=id)
        ]
        remote_file_list = [
            path_name['name'] for path_name in self._drive_handler.getFileList(parent=id)
        ]

        for local_file in local_file_list:
            if local_file not in remote_file_list:
                self._drive_handler.create_txt_file(path=path, name=local_file, parent=id)

        for local_directory in local_dir_list:
            if local_directory not in remote_dir_list:
                self._drive_handler.create_directory(name=local_directory, parent=id)

        remote_dir_list_with_id = [
            name for name in self._drive_handler.get_directory_list(parent=id)
        ]

        for remote_directory in remote_dir_list_with_id:
            self.log_changes_in_directory(path=os.path.join(path, remote_directory['name']),
                                          id=remote_directory['id'])
