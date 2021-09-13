#!/usr/bin/python3
import os.path
import socket
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib import flow
from httplib2 import error
from tqdm import tqdm

SCOPES = ["https://www.googleapis.com/auth/drive"]


class DriveApiHandler():  # pylint: disable=old-style-class
    def __init__(self, killer):
        self._creds = None
        self._service = None
        self._killer = killer

    def check_for_token(self, key_path):
        """Checks for token, if there is none - creates one from key.
        """

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        while True:
            try:
                if os.path.exists(os.path.join(key_path, "token.json")):
                    self._creds = Credentials.from_authorized_user_file(
                        os.path.join(key_path, "token.json"), SCOPES)
                # If there are no (valid) credentials available, let the user log in.
                if not self._creds or not self._creds.valid:
                    if self._creds and self._creds.expired and self._creds.refresh_token:
                        self._creds.refresh(Request())
                    else:
                        flow_ = flow.InstalledAppFlow.from_client_secrets_file(
                            os.path.join(
                                key_path,
                                "client_secret_1088415424839-ftesriv7jrc1hku5v9r0b4uvlo8ionc4." +
                                "apps.googleusercontent.com.json"), SCOPES)
                        self._creds = flow_.run_console()
                    # Save the credentials for the next run
                    with open(os.path.join(key_path, "token.json"), "w") as token:
                        token.write(self._creds.to_json())
                self._service = build("drive", "v3", credentials=self._creds)
            except socket.timeout as err:
                self._killer.exception_message = str(err)
                continue
            except error.ServerNotFoundError as err:
                self._killer.exception_message = str(err)
                continue
            else:
                break

    def get_file_list(self, parent='root'):
        while True:
            try:
                results = self._service.files().list(
                    q="'" + parent +
                    "' in parents and mimeType!='application/vnd.google-apps.folder' " +
                    "and trashed = false",
                    fields="files(id, name, md5Checksum)",
                ).execute()
                return results.get("files", [])
            except socket.timeout as err:
                self._killer.exception_message = str(err)
                continue
            except error.ServerNotFoundError as err:
                self._killer.exception_message = str(err)
                continue
            else:
                break

    def get_directory_list(self, parent='root'):
        while not self._killer.kill_now:
            try:
                results = self._service.files().list(
                    q="'" + parent +
                    "' in parents and mimeType='application/vnd.google-apps.folder' " +
                    "and trashed = false",
                    fields="files(id, name)",
                ).execute()
                return results.get("files", [])
            except socket.timeout as err:
                self._killer.exception_message = str(err)
                continue
            except error.ServerNotFoundError as err:
                self._killer.exception_message = str(err)
                continue
            else:
                break

    def create_directory(self, name, parent='root'):
        while not self._killer.kill_now:
            try:
                file_metadata = {
                    "name": name,
                    "parents": [parent],
                    "mimeType": "application/vnd.google-apps.folder"
                }
                return self._service.files().create(body=file_metadata,
                                                    fields="id").execute().get('id')
            except socket.timeout as err:
                self._killer.exception_message = str(err)
                continue
            except error.ServerNotFoundError as err:
                self._killer.exception_message = str(err)
                continue
            else:
                break

    def update_txt_file(self, name, path, parent='root'):
        while not self._killer.kill_now:
            try:
                print("  Uploading file {}".format(name))  # pylint: disable=superfluous-parens
                temp_file_id = None
                file_metadata = {"name": name, "mimeType": "txt/csv"}
                media = MediaFileUpload(os.path.join(path, name),
                                        resumable=True,
                                        chunksize=256 * 1024)
                remote_file_list = self.get_file_list(parent=parent)
                for remote_file in remote_file_list:
                    if remote_file['name'] == name:
                        temp_file_id = remote_file['id']
                request = self._service.files().update(body=file_metadata,
                                                       media_body=media,
                                                       fileId=temp_file_id)
            except socket.timeout as err:
                self._killer.exception_message = str(err)
                continue
            except error.ServerNotFoundError as err:
                self._killer.exception_message = str(err)
                continue
            else:
                break
        response = None
        last_status = 0
        pbar = tqdm(total=100)
        while response is None:
            try:
                status, response = request.next_chunk()
                if status:
                    pbar.update(int(status.progress() * 100) - last_status)
                    last_status = int(status.progress() * 100)
            except socket.timeout as err:
                self._killer.exception_message = str(err)
                continue
            except OSError as err:
                self._killer.exception_message = str(err)
                continue
            except error.ServerNotFoundError as err:
                self._killer.exception_message = str(err)
                continue
        pbar.update(100 - last_status)
        pbar.close()

    def create_txt_file(self, name, path, parent='root'):
        while not self._killer.kill_now:
            try:
                file_metadata = {"name": name, "parents": [parent], "mimeType": "txt/csv"}
                self._service.files().create(body=file_metadata, fields="id").execute()
                self.update_txt_file(name=name, path=path, parent=parent)

            except socket.timeout as err:
                self._killer.exception_message = str(err)
                continue
            except error.ServerNotFoundError as err:
                self._killer.exception_message = str(err)
                continue
            else:
                break
