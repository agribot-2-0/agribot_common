import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive"]


class DriveApiHandler:
    def __init__(self):
        self.creds = None
        self.service = None

    def checkForToken(self, key_path):
        """Checks for token, if there is none - creates one from credentials.json.
        """

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(key_path + "token.json"):
            self.creds = Credentials.from_authorized_user_file(key_path + "token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(key_path + "credentials.json",
                                                                 SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(key_path + "token.json", "w") as token:
                token.write(self.creds.to_json())
        self.service = build("drive", "v3", credentials=self.creds)

    def getResults(self, *, parent='root', type='folder'):
        type_str = None
        if type == 'folder':
            type_str = "and mimeType='application/vnd.google-apps.folder'"
        elif type == 'file':
            type_str = "and mimeType!='application/vnd.google-apps.folder'"
        else:
            raise ValueError("Wrong value in keyword type. Expected 'folder' or 'file'.")
        results = self.service.files().list(
            q="'" + str(parent) + "' in parents " + type_str + " and trashed = false",
            pageSize=10,
            fields="nextPageToken, files(id, name)",
        ).execute()
        return results.get("files", [])

    def create(self, *, name='Logs', parents='root', type='folder'):
        if type == 'folder':
            type = "application/vnd.google-apps.folder"
        elif type == 'file':
            type = "txt/csv"
        else:
            raise ValueError("Wrong value in keyword type. Expected 'folder' or 'file'.")
        file_metadata = {
            "name": str(name),
            "parents": [str(parents)],
            "mimeType": str(type),
        }
        file = (self.service.files().create(body=file_metadata, fields="id").execute())
        return file.get('id')