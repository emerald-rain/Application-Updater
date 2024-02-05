import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError
import os

# Initialize a Dropbox object using an API v2 key
dbx = dropbox.Dropbox('sl.BvB2gyx0Zst8HveKkdl9GgRkpSWTtiMqc6MfewTg-ayr7VKxWSQRYMIMHe9AMTXl4jTJgc3s4hwiAxU0O_3wXE4RxWgJLF0uRQDY1u-4WLvlqreI6xWWpJtHidRuz8U6jAplBKZmjVCLrUxE8YdCL2I')

def upload_file(file_path, target_path):
    with open(file_path, 'rb') as f:
        try:
            dbx.files_upload(f.read(), target_path, mode=WriteMode('overwrite'))
            print(f"Uploaded {file_path} to Dropbox.")
        except ApiError as e:
            print(f"Failed to upload {file_path}: {e}")

def download_file(dropbox_path):
    download_dir = os.path.join(os.getcwd(), "Downloaded")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    local_path = os.path.join(download_dir, os.path.basename(dropbox_path))
    try:
        dbx.files_download_to_file(local_path, dropbox_path)
        print(f"Downloaded {dropbox_path} to {local_path}.")
    except ApiError as e:
        print(f"Failed to download {dropbox_path}: {e}")

def list_files(folder_path=''):
    try:
        return dbx.files_list_folder(folder_path).entries
    except ApiError as e:
        print(f"Failed to list files: {e}")
        return []

def delete_file(file_path):
    try:
        dbx.files_delete(file_path)
        print(f"Deleted {file_path}.")
    except ApiError as e:
        print(f"Failed to delete {file_path}: {e}")

def select_file_for_action(folder_path='', action=lambda x: print(x)):
    files = list_files(folder_path)
    if files:
        print("\nFiles in Dropbox:")
        for i, file in enumerate(files, start=1):
            print(f"{i}. {file.name}")
        try:
            choice = int(input("Select a file: ")) - 1
            if 0 <= choice < len(files):
                action(files[choice].path_lower)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")
    else:
        print("No files to display.")

def main():
    while True:
        print("\nDropbox File Manager")
        print("1. Upload a file")
        print("2. Select and download a file")
        print("3. List files")
        print("4. Select and delete a file")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            file_path = input("Enter the path of the file to upload: ")
            target_path = input("Enter the Dropbox target path including filename: ")
            upload_file(file_path, target_path)
        elif choice == '2':
            print("Select a file to download:")
            select_file_for_action(action=download_file)
        elif choice == '3':
            files = list_files()
            if files:
                print("\nFiles in Dropbox:")
                for file in files:
                    print(file.name)
            else:
                print("No files to display.")
        elif choice == '4':
            print("Select a file to delete:")
            select_file_for_action(action=delete_file)
        elif choice == '5':
            print("Exiting.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
