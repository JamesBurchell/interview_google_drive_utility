# Google Drive Utility

## Overview
The **Google Drive Utility** is a Python application that integrates with Google Drive, allowing users to authenticate using OAuth 2.0 and perform various file operations such as listing, uploading, downloading, and deleting files. This application is designed to provide a simple interface for managing files in Google Drive directly from the command line.

## Assumptions
- The user has a valid Google account with sufficient permissions to access Google Drive.
- The utility assumes proper configuration of Google API credentials.
- The user is comfortable with running python
- The user is comfortable with a CLI

## Design Decisions
- The utility uses **IDs of files and folders** for identifying items in Google Drive to simplify interactions. **IDs** were chosen over file and folder names to reduce scope while still demonstrating functionality.
- The **command-line interface** (CLI) is used for user interaction, assuming it is sufficient for demonstration purposes.
- The CLI is implemented as a simple Python script, instead of using a more robust CLI library. This approach is considered adequate to showcase the application's functionality.
- The CLI script is **not** the focus of this project and was implemented purely to demonstrate the underlying functionality.
- **Error handling** is included for common issues, such as invalid file paths and authentication problems.
- The project adheres to **modular software design** principles, maintaining separation of concerns by keeping authentication and file management in distinct modules.

## Limitations
- This utility is not production-ready and should be treated as a demonstration project only.
- While functional, it lacks enhancements and thorough testing that would be necessary for everyday use in a production environment.
- CLI UI is a limited wraper around the core functionality

## Key Features
- **Authentication**: Securely authenticate users with their Google accounts using OAuth 2.0.
- **List Files**: View all files in the user's Google Drive, including file names, types, and last modified dates. List function can take a `folder_id` parameter to limit serach to a Folder.
- **Upload Files**: Upload files from the local system to a specified folder in Google Drive. Upload function can take a `folder_id` parameter to upload a file to a specific folder in Goolge Drive.
- **Download Files**: Download files from Google Drive to the local system.
- **Delete Files**: Remove files from Google Drive.

## Requirements
- Python 3.x
- Google API Client Library for Python
- Google Auth Library for Python

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/JamesBurchell/google-drive.git
cd google-drive
```

### 2. Install Dependencies
Ensure `pip` is installed and run:
```bash
pip install -r requirements.txt
```
*Note: ideally should run in a Python virtual environment.

### 3. Google API Credentials
- Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
- Enable the **Google Drive API** for the project.
- Create OAuth 2.0 credentials and download the `credentials.json` file.
- Place the `credentials.json` file in the project root directory.

### 4. Run the Application
Execute the main script:
```bash
python3 src/main.py
```

## Usage

After running the application, follow these steps:

1. Authenticate with your Google account when prompted.
2. Select an option from the menu:
   - **1**: List files in a specified folder (or root).
   - **2**: Upload a file to a specified folder (or root).
   - **3**: Download a file by ID.
   - **4**: Delete a file by ID.
   - **5**: Exit the program.

## Testing

This project includes unit and integration tests to ensure functionality and reliability. To run the tests, use the following command:
```bash
pytest
```

## Considerations for Future Enhancements
- Implement more detailed error handling and logging.
- Add support for handling Google Drive file/folder names instead of just IDs.
- Extend the application to support batch file operations.
- Improve the user interface with a GUI for broader usage scenarios.

## Documentation
For detailed information on the Google Drive API, refer to the [Google Drive API Documentation](https://developers.google.com/drive).

## License
This project is licensed under the MIT License.
