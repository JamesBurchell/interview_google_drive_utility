import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.auth_google import GoogleDriveAuth

class TestGoogleDriveAuth(unittest.TestCase):
    
    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.auth_google.InstalledAppFlow.from_client_secrets_file')
    def test_authenticate_new_flow(self, mock_flow, mock_open, mock_exists):
        # Mock the flow to return a mock credentials object
        cred_path='path/to/client_secret.json'
        mock_creds = MagicMock()
        mock_flow.return_value.run_local_server.return_value = mock_creds

        # Instantiate the GoogleDriveAuth class and call authenticate
        auth = GoogleDriveAuth(cred_path)
        creds = auth.authenticate()

        # Assertions
        mock_flow.assert_called_once_with(auth.client_secret_file, scopes=auth.scopes)
        mock_flow.return_value.run_local_server.assert_called_once()
        mock_open.assert_called_once_with(auth.token_file, 'w')
        self.assertEqual(creds, mock_creds)

    @patch('os.path.exists', return_value=True)
    @patch('google.oauth2.credentials.Credentials.from_authorized_user_file')
    def test_authenticate_existing_valid_token(self, mock_from_authorized_user_file, mock_exists):
        # Mock the Credentials.from_authorized_user_file to return a mock credentials object
        cred_path='path/to/client_secret.json'
        mock_creds = MagicMock(valid=True)
        mock_from_authorized_user_file.return_value = mock_creds

        # Instantiate the GoogleDriveAuth class and call authenticate
        auth = GoogleDriveAuth(cred_path)
        creds = auth.authenticate()

        # Assertions
        mock_exists.assert_called_once_with(auth.token_file)
        mock_from_authorized_user_file.assert_called_once_with(auth.token_file, auth.scopes)
        self.assertEqual(creds, mock_creds)
        self.assertTrue(creds.valid)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('google.oauth2.credentials.Credentials.from_authorized_user_file')
    @patch('src.auth_google.Request')
    def test_authenticate_existing_expired_token(self, mock_request, mock_from_authorized_user_file, mock_exists, mock_open):
        cred_path='path/to/client_secret.json'
        mock_creds = MagicMock(valid=False, expired=True, refresh_token=True)
        mock_creds.to_json.return_value = '{"token": "mock_token"}'
        mock_from_authorized_user_file.return_value = mock_creds

        auth = GoogleDriveAuth(cred_path)
        auth.authenticate()

        mock_exists.assert_called_once_with(auth.token_file)
        mock_from_authorized_user_file.assert_called_once_with(auth.token_file, auth.scopes)
        
        # Ensure the mock_request is used correctly
        mock_creds.refresh.assert_called_once_with(mock_request())  # Use mock_request() to get the mock instance
        mock_open.assert_called_once_with(auth.token_file, 'w')
        mock_open().write.assert_called_once_with('{"token": "mock_token"}')

if __name__ == '__main__':
    unittest.main()