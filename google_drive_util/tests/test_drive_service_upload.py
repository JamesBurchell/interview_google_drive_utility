import unittest
from unittest.mock import Mock, patch
from googleapiclient.errors import HttpError
from src.google_drive_service import GoogleDriveService 

class TestGoogleDriveServiceUpload(unittest.TestCase):

    def setUp(self):
        self.mock_service = Mock()
        self.drive_service = GoogleDriveService(self.mock_service)

    @patch('src.google_drive_service.MediaFileUpload')
    def test_upload_file_success(self, mock_media_file_upload):

        file_path = "test_path"
        file_name = "test_file"
        folder_id = "test_folder_id"
        file_id = "test_file_id"

        mock_media_file_upload.return_value = Mock()
        self.mock_service.files().create.return_value.execute.return_value = {"id": file_id}

        result = self.drive_service.upload_file(file_path, file_name, folder_id)

        self.assertEqual(result, file_id)
        self.mock_service.files().create.assert_called_once_with(
            body={"name": file_name, "parents": [folder_id]},
            media_body=mock_media_file_upload.return_value,
            fields="id"
        )

    @patch('src.google_drive_service.MediaFileUpload')
    def test_upload_file_error(self, mock_media_file_upload):
        file_path = "test_path"
        file_name = "test_file"
        folder_id = "test_folder_id"

        mock_media_file_upload.return_value = Mock()
        self.mock_service.files().create.return_value.execute.side_effect = HttpError(
            resp=Mock(status=403), content=b'Forbidden'
        )

        result = self.drive_service.upload_file(file_path, file_name, folder_id)

        self.assertIsNone(result)
        self.mock_service.files().create.assert_called_once_with(
            body={"name": file_name, "parents": [folder_id]},
            media_body=mock_media_file_upload.return_value,
            fields="id"
        )

if __name__ == '__main__':
    unittest.main()
