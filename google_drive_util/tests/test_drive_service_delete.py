import unittest
from unittest.mock import Mock, patch
from googleapiclient.errors import HttpError
from src.google_drive_service import GoogleDriveService 


class TestGoogleDriveServiceDelete(unittest.TestCase):

    def setUp(self):
        
        #  Make mock so no real google calls are made
        self.mock_service = Mock()
        self.drive_service = GoogleDriveService(self.mock_service)

    def test_delete_file_success(self):
        file_id = "test_file_id"
        self.mock_service.files().delete.return_value.execute.return_value = None

        self.drive_service.delete_file(file_id)

        self.mock_service.files().delete.assert_called_once_with(fileId=file_id)
        self.mock_service.files().delete().execute.assert_called_once()

    def test_delete_file_http_error(self):
        file_id = "test_file_id"
        http_error = HttpError(resp=Mock(status=404), content=b'File not found')
        self.mock_service.files().delete.return_value.execute.side_effect = http_error

        with patch('builtins.print') as mock_print:
            self.drive_service.delete_file(file_id)

        self.mock_service.files().delete.assert_called_once_with(fileId=file_id)
        self.mock_service.files().delete().execute.assert_called_once()
        mock_print.assert_called_once()
        self.assertIn("An error occurred: <HttpError 404", mock_print.call_args[0][0])

if __name__ == '__main__':
    unittest.main()