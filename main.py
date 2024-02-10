import requests
import zipfile
import os
from io import BytesIO
import shutil

# Your Dropbox links
DROPBOX_VERSION_LINK = ""
DROPBOX_ARCHIVE_LINK = ""

# Local version file and update directory
LOCAL_VERSION_FILE = "version.txt"
UPDATE_DIRECTORY = os.getcwd()

# Download a file from a given URL.
def download_file(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
    return response.content

# Parse a version string and return a tuple of integers.
def read_version_from_string(version_string): 
    return tuple(map(int, version_string.strip().split('.')))

# Compare two version tuples.
def is_newer_version(local_version, online_version):
    return online_version > local_version

def clear_update_directory():
    for item in os.listdir(UPDATE_DIRECTORY):
        item_path = os.path.join(UPDATE_DIRECTORY, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception as e:
            return

    print("Update directory cleared.")

# Extract the archive to the update directory.
def update_application(archive_bytes):
    user_response = input("Do you want to delete all existing files in the update directory before installing? (y/n): ")
    if user_response.lower() == 'y':
        clear_update_directory()

    with zipfile.ZipFile(BytesIO(archive_bytes), 'r') as archive:
        archive.extractall(UPDATE_DIRECTORY)
    print("Application updated successfully.")

def main():
    try:
        # Download and read the online version
        online_version_string = download_file(DROPBOX_VERSION_LINK).decode('utf-8')
        online_version = read_version_from_string(online_version_string)
        
        # Read the local version
        try:
            with open(LOCAL_VERSION_FILE, 'r') as file:
                local_version_string = file.read()
            local_version = read_version_from_string(local_version_string)
        except:
            print("The version file could not be read. If this is the first run, you have nothing to worry about.")
            local_version = read_version_from_string("0.0.0")
        
        # Compare versions
        if is_newer_version(local_version, online_version):
            input(f"New version available: {online_version_string}. Press Enter to start downloading the update archive...")
            archive_bytes = download_file(DROPBOX_ARCHIVE_LINK)
            update_application(archive_bytes)
        else:
            print("No update necessary.")
    except Exception as e:
        print(f"Error updating application: {e}")

if __name__ == "__main__":
    main()
