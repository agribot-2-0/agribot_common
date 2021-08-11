#!/usr/bin/python3
import os.path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib import flow

SCOPES = ["https://www.googleapis.com/auth/drive"]


class DriveApiHandler:
    def __init__(self):
        self._creds = None
        self.service = None

    def check_for_token(self, key_path):
        """Checks for token, if there is none - creates one from credentials.json.
        """

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(os.path.join(key_path, "token.json")):
            self._creds = Credentials.from_authorized_user_file(
                os.path.join(key_path, "token.json"), SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self._creds or not self._creds.valid:
            if self._creds and self._creds.expired and self._creds.refresh_token:
                self._creds.refresh(Request())
            else:
                flow_ = flow.InstalledAppFlow.from_client_secrets_file(
                    os.path.join(key_path, "credentials.json"), SCOPES)
                self._creds = flow_.run_console()
            # Save the credentials for the next run
            with open(os.path.join(key_path, "token.json"), "w") as token:
                token.write(self._creds.to_json())
        self.service = build("drive", "v3", credentials=self._creds)

    def get_file_list(self, parent='root'):
        results = self.service.files().list(
            q="'" + str(parent) +
            "' in parents and mimeType!='application/vnd.google-apps.folder' and trashed = false",
            pageSize=10,
            fields="nextPageToken, files(id, name)",
        ).execute()
        return results.get("files", [])

    def get_directory_list(self, parent='root'):
        results = self.service.files().list(
            q="'" + str(parent) +
            "' in parents and mimeType='application/vnd.google-apps.folder' and trashed = false",
            pageSize=10,
            fields="nextPageToken, files(id, name)",
        ).execute()
        return results.get("files", [])

    def create_txt_file(self, *, name, parent='root', path):  #pylint: disable=syntax-error
        file_metadata = {"name": str(name), "parents": [str(parent)], "mimeType": "txt/csv"}
        media = MediaFileUpload(str(os.path.join(path, name)))
        self.service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    def create_directory(self, *, name, parent='root'):  #pylint: disable=syntax-error
        file_metadata = {
            "name": str(name),
            "parents": [str(parent)],
            "mimeType": "application/vnd.google-apps.folder"
        }
        file = (self.service.files().create(body=file_metadata, fields="id").execute())
        return file.get('id')
