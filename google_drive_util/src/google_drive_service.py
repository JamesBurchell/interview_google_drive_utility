from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError
import io

class GoogleDriveService:
    def __init__(self, service):
        self.service = service

    # Builds an instance of GoogleDriveService with the service
    @classmethod
    def create(cls, auth):
        service = build('drive', 'v3', credentials=auth.creds)
        return cls(service)

    def list_files(self, folder_id=None):
        try:
            files = []
            page_token = None
            query = f"'{folder_id}' in parents" if folder_id else None

            while True:
                response = self._execute_list(page_token, query)
                files.extend(response.get("files", []))
                page_token = response.get("nextPageToken", None)
                if page_token is None:
                    break

        except HttpError as error:
            print(f"An error occurred: {error}")
            files = None

        return files

    def _execute_list(self, page_token, query):
        return self.service.files().list(
            spaces="drive",
            fields="nextPageToken, files(id, name, mimeType, modifiedTime)",
            pageToken=page_token,
            q=query
        ).execute()

    def upload_file(self, file_path, file_name, folder_id=None):
        try:
            file_metadata = {"name": file_name}
            if folder_id:
                file_metadata['parents'] = [folder_id]

            media = MediaFileUpload(file_path)
            file = self._execute_upload(file_metadata, media)

        except HttpError as error:
            print(f"An error occurred: {error}")
            file = None

        return file.get("id") if file else None

    def _execute_upload(self, file_metadata, media):
        return self.service.files().create(
            body=file_metadata, media_body=media, fields="id"
        ).execute()

    def download_file(self, file_id, destination_path):
        try:
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}.")

        except HttpError as error:
            print(f"An error occurred: {error}")
            file = None

        if file:
            with open(destination_path, 'wb') as f:
                f.write(file.getvalue())

    def delete_file(self, file_id):
        try:
            self._execute_delete(file_id)
        except HttpError as error:
            print(f"An error occurred: {error}")

    def _execute_delete(self, file_id):
        self.service.files().delete(fileId=file_id).execute()