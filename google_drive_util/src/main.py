import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from auth_google import GoogleDriveAuth
from google_drive_service import GoogleDriveService


PATH_TO_CLIENT_SECERT_FILE = './credentials.json'

def main():
    print("\n---------------------------------")
    print("Starting the Google Drive Utility")

    print("Authenticating with Google...")
    auth = GoogleDriveAuth(PATH_TO_CLIENT_SECERT_FILE)
    auth.authenticate()
    print("Authenticated.")

    drive_service = GoogleDriveService.create(auth)
    
    print("---------------------------------")
    
    while True:
        print("\nChoose an action:")
        print("1. List files")
        print("2. Upload a file")
        print("3. Download a file")
        print("4. Delete a file")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            folder_id = input("\nEnter the Folder ID to list to (leave blank for root): ")
            print("\n--- Listing File & Folders ----")
            print("-------------------------------")
            files = drive_service.list_files(folder_id if folder_id else None)
            for file in files:
                print(f"[ ID: {file['id']} | Name: {file['name']} | Type: {file['mimeType']} | Modified: {file['modifiedTime']} ]")
            print("---------------------------------")

        elif choice == '2':
            file_name = input("\nEnter the Name to save the file as in Google Drive: ")
            folder_id = input("Enter the Folder ID to upload to (leave blank for root): ")
            
            while True:  # So it won't blow up if the file path is wrong
                file_path = input("Enter the Path of the File to upload: ")
                
                if os.path.isdir(file_path):
                    print(file_path, "is a directory. Must be a vaild file path. Please try again")
                    continue
                if not os.path.exists(file_path):
                    print("Invalid File Path. Please try again.")
                    continue

                break
                
            file_id = drive_service.upload_file(file_path, file_name, folder_id if folder_id else None)
            
            print("\n--- Uploaded File ---")
            print("File ID:",file_id)
            print("File Name:", file_name)
            print("---------------------------------")

        elif choice == '3':
            file_id = input("\nEnter the File ID of the file to download: ")

            while True:
                destination_path = input("Enter the destination path to save the downloaded file: ")

                if not os.path.isdir(os.path.dirname(destination_path)) or not os.path.basename(destination_path):
                    print("Invalid File Path. Path must include file name. Please try again.")
                    continue

                break
            
            drive_service.download_file(file_id, destination_path)
            print("\n-------------")
            print("File downloaded successfully to:", destination_path)
            print("---------------------------------")

        elif choice == '4':
            file_id = input("\nEnter the File ID of the file to Delete: ")
            drive_service.delete_file(file_id)
            print("\nFile deleted successfully with ID:", file_id)
            print("---------------------------------")

        elif choice == '5':
            print("Exiting the program.\n")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()