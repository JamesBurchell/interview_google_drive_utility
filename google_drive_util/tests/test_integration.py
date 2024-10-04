import unittest
import os
from src.auth_google import GoogleDriveAuth
from src.google_drive_service import GoogleDriveService

# This is a full integration test and will require access to a google drive.
# Will need to supply a creds file.
# A user will need to accept the OAuth

class TestIntegration(unittest.TestCase):
    def test_happy_path_list_upload_download_delete(self):

        client_secret_file = './credentials.json'
        self.assertTrue(os.path.exists(client_secret_file), "Credentials file not found")
        
        # This test folder will serve as a sandbox env for this integration test.
        # This is due to there being no dedicated sandbox env for test. Instead this test
        # could be ran against a Drive with a large amount of files/folders and I want to 
        # limiit noise.
        folder_metadata = {
            'name': 'Strac Test Folder',
            'mimeType': 'application/vnd.google-apps.folder'
        }

        try:
            auth = GoogleDriveAuth(client_secret_file)
            auth.authenticate()
            drive_service = GoogleDriveService.create(auth)
            self.assertIsNotNone(drive_service)
            
            # Make Test Folder to test against
            test_folder = drive_service.service.files().create(body=folder_metadata, fields='id').execute()
            self.assertIsNotNone(test_folder)
            
            test_folder_id = test_folder.get('id')
            self.assertIsNotNone(test_folder_id)
            print("Test Folder ID:", test_folder_id)
        
            # Should be no files in a new Folder
            files = drive_service.list_files(test_folder_id)
            self.assertEqual(len(files), 0)

            # Make a test File to be uploaded
            test_file_path = 'strac_test_file.txt'
            test_file_message = 'This is a test file.'
            with open(test_file_path, 'w') as f:
                f.write(test_file_message)
       
            # Should be able to upload a file
            txt_file_id = drive_service.upload_file(test_file_path, test_file_path, test_folder_id)
            self.assertIsNotNone(txt_file_id)

            # Should list out recently uploaded file
            files = drive_service.list_files(test_folder_id)
            self.assertIsNotNone(files)
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0]['name'], test_file_path)

            # Test download
            download_path = f"downloaded_{test_file_path}"
            drive_service.download_file(txt_file_id, download_path)
            self.assertTrue(os.path.exists(download_path))
            with open(download_path, 'r') as f:
                content = f.read()
            self.assertEqual(content, test_file_message)

            # Test delete
            drive_service.delete_file(txt_file_id)

            files = drive_service.list_files(test_folder_id)
            self.assertEqual(len(files), 0)

        finally:
            # Delete the test folder in Drive
            drive_service.delete_file(test_folder_id)

            # Delete the test files Locally
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
            if os.path.exists(download_path):
                os.remove(download_path)


if __name__ == '__main__':
    unittest.main()