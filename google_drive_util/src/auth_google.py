from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os

class GoogleDriveAuth:
    def __init__(self, client_secret_file):
        self.creds = None
        self.client_secret_file = client_secret_file
        self.token_file = 'token.json'
        self.scopes = ['https://www.googleapis.com/auth/drive']

    def authenticate(self):
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secret_file, 
                    scopes=self.scopes
                )
                self.creds = flow.run_local_server(port=0)

            with open(self.token_file, 'w') as token:
                token.write(self.creds.to_json())

        return self.creds
    
