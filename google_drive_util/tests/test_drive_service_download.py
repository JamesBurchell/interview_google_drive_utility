import unittest
from unittest.mock import Mock, patch
from googleapiclient.errors import HttpError
from src.google_drive_service import GoogleDriveService

class TestGoogleDriveServiceDownload(unittest.TestCase):

    def setUp(self):
        self.mock_service = Mock()
        self.drive_service = GoogleDriveService(self.mock_service)

    @patch('src.google_drive_service.MediaIoBaseDownload')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('io.BytesIO', new_callable=Mock)
    def test_download_file_success(self, mock_bytes_io, mock_open, mock_media_io_base_download):
        file_id = "test_file_id"
        destination_path = "test_destination_path"
        mock_request = Mock()
        self.mock_service.files().get_media.return_value = mock_request

        mock_downloader = mock_media_io_base_download.return_value

        # Create mock status objects with a progress method
        mock_status_1 = Mock()
        mock_status_1.progress = Mock(return_value=0.5)
        mock_status_2 = Mock()
        mock_status_2.progress = Mock(return_value=1.0)

        mock_downloader.next_chunk.side_effect = [
            (mock_status_1, False), 
            (mock_status_2, True)
        ]

        # Mock BytesIO instance
        mock_bytes_io_instance = mock_bytes_io.return_value

       
        self.drive_service.download_file(file_id, destination_path)

        self.mock_service.files().get_media.assert_called_once_with(fileId=file_id)
       
        # Ensure the same BytesIO object is used in the assertion
        mock_media_io_base_download.assert_called_once_with(mock_bytes_io_instance, mock_request)
        mock_open.assert_called_once_with(destination_path, 'wb')
        mock_open().write.assert_called_once()

    @patch('src.google_drive_service.MediaIoBaseDownload')
    def test_download_file_error(self, mock_media_io_base_download):
        file_id = "test_file_id"
        destination_path = "test_destination_path"
        self.mock_service.files().get_media.side_effect = HttpError(
            resp=Mock(status=404), content=b'Not Found'
        )

        self.drive_service.download_file(file_id, destination_path)

        self.mock_service.files().get_media.assert_called_once_with(fileId=file_id)
        mock_media_io_base_download.assert_not_called()

if __name__ == '__main__':
    unittest.main()
