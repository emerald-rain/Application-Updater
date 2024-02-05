import dropbox
import os
import zipfile
import shutil

# Constants
ACCESS_TOKEN = 'sl.BvDrdfuojaA2wV8BMKJyxP1CNzV_YaKmIQQay2JsoGwYEBjjSykcjW3blTRCDhdnj7ykLkNM7wHSSd5FpJxDSN9z1qj235TY8o9tbTe0W5y2ZTAfwT8ntgpb7WISUkGF0C3tk6dj66ty0FNjr_neuJU'
# Automatically sets the game folder path to the launcher's current directory
GAME_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE_NAME = 'version.txt'
VERSION_FILE_PATH = os.path.join(GAME_FOLDER_PATH, VERSION_FILE_NAME)
# Assuming the version file is in the root of your Dropbox app folder
DROPBOX_VERSION_FILE = '/' + VERSION_FILE_NAME

# Initialize Dropbox client
dbx = dropbox.Dropbox(ACCESS_TOKEN)

def get_dropbox_version():
    """Get the latest game version from Dropbox."""
    try:
        md, res = dbx.files_download(DROPBOX_VERSION_FILE)
    except dropbox.exceptions.ApiError as err:
        print('Failed to download version file from Dropbox:', err)
        return None
    data = res.content.decode()
    return data.strip()

def get_local_version():
    """Get the local version of the game."""
    try:
        with open(VERSION_FILE_PATH, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def update_game():
    """Update the game to the latest version."""
    local_version = get_local_version()
    remote_version = get_dropbox_version()

    if remote_version is None or local_version == remote_version:
        print("Game is up to date.")
        return

    print("Updating game to version:", remote_version)
    # The archive name on Dropbox should match the version
    archive_name = f'{remote_version}.zip'
    # Assuming the archive is stored at the root of the Dropbox app folder
    dropbox_archive_path = '/' + archive_name
    local_archive_path = os.path.join(GAME_FOLDER_PATH, archive_name)

    # Downloading the latest game archive
    try:
        dbx.files_download_to_file(local_archive_path, dropbox_archive_path)
    except dropbox.exceptions.ApiError as err:
        print('Failed to download the game archive:', err)
        return

    # Clean existing game files except the launcher
    for item in os.listdir(GAME_FOLDER_PATH):
        item_path = os.path.join(GAME_FOLDER_PATH, item)
        if os.path.isfile(item_path) and item != os.path.basename(__file__) and item != VERSION_FILE_NAME:
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    # Unpack the new version
    with zipfile.ZipFile(local_archive_path, 'r') as zip_ref:
        zip_ref.extractall(GAME_FOLDER_PATH)

    # Remove the downloaded archive after extraction
    os.remove(local_archive_path)

    # Update the local version file
    with open(VERSION_FILE_PATH, 'w') as f:
        f.write(remote_version)

    print("Game updated successfully to version:", remote_version)

if __name__ == '__main__':
    update_game()
