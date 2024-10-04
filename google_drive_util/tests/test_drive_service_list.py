import unittest
from unittest.mock import Mock, patch
from googleapiclient.errors import HttpError
from src.google_drive_service import GoogleDriveService

class TestGoogleDriveServiceListFiles(unittest.TestCase):

    def setUp(self):
        self.mock_service = Mock()
        self.drive_service = GoogleDriveService(self.mock_service)

    def test_list_files_success(self):
        mock_files_list = self.mock_service.files.return_value.list.return_value
        mock_files_list.execute.side_effect = [
            {'files': [{'id': '1', 'name': 'file1.txt'}, {'id': '2', 'name': 'file2.txt'}], 'nextPageToken': 'token'},
            {'files': [{'id': '3', 'name': 'file3.txt'}], 'nextPageToken': None}
        ]
        folder_id = "test_folder_id"

        files = self.drive_service.list_files(folder_id)

        self.assertEqual(len(files), 3)
        self.assertEqual(files[0]['id'], '1')
        self.assertEqual(files[1]['id'], '2')
        self.assertEqual(files[2]['id'], '3')
        self.mock_service.files.return_value.list.assert_any_call(
            spaces="drive",
            fields="nextPageToken, files(id, name, mimeType, modifiedTime)",
            pageToken=None,
            q=f"'{folder_id}' in parents"
        )
        self.mock_service.files.return_value.list.assert_any_call(
            spaces="drive",
            fields="nextPageToken, files(id, name, mimeType, modifiedTime)",
            pageToken='token',
            q=f"'{folder_id}' in parents"
        )

    @patch('src.google_drive_service.GoogleDriveService._execute_list')
    def test_list_files_http_error(self, mock_execute_list):

        mock_execute_list.side_effect = HttpError(Mock(), b'Error')
        folder_id = "test_folder_id"

        files = self.drive_service.list_files(folder_id)

        self.assertIsNone(files)

if __name__ == '__main__':
    unittest.main()
