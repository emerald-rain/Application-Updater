import dropbox
import os
import zipfile
import shutil
import subprocess
import sys

ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'  # Dropbox public token
GAME_FOLDER_PATH = os.getcwd()  # Get the current working directory
VERSION_FILE_PATH = os.path.join(GAME_FOLDER_PATH, 'version.txt')  # Recognizing local text file with installed game version
DROPBOX_VERSION_FILE = '/' + 'version.txt'  # Path to the current version file on Dropbox cloud

dbx = dropbox.Dropbox(ACCESS_TOKEN)

def get_version(path, is_remote=False):
    if is_remote:  # Getting the latest version on the cloud
        try:
            _, res = dbx.files_download(path)
            return res.content.decode().strip()
        except dropbox.exceptions.ApiError as err:
            print(f'Failed to download version file: {err}')
            return None
    else:  # Getting the local version
        try:
            with open(path, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            return None

def update_game():
    try:
        local_version = get_version(VERSION_FILE_PATH)
        remote_version = get_version(DROPBOX_VERSION_FILE, is_remote=True)
        if remote_version is None or local_version == remote_version:
            print("Game is up to date. Launching...")
        else:
            print(f"Local version: {local_version} || Latest version: {remote_version} ")
            print(f"The download of the latest version begins. On average, it takes ~150mb.")
            archive_name = f'{remote_version}.zip'
            local_archive_path = os.path.join(GAME_FOLDER_PATH, archive_name)

            try:
                dbx.files_download_to_file(local_archive_path, '/' + archive_name)
                print(f"Downloaded {archive_name} successfully.")
            except dropbox.exceptions.ApiError as err:
                print(f'Failed to download the game archive: {err}')
                return

            for item in os.listdir(GAME_FOLDER_PATH):
                item_path = os.path.join(GAME_FOLDER_PATH, item)
                if item_path not in [(os.path.join(GAME_FOLDER_PATH, "launcher.exe")), VERSION_FILE_PATH, local_archive_path]:
                    try:
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                    except PermissionError as e:
                        print(f"Failed to delete {item_path}: {e}")

            with zipfile.ZipFile(local_archive_path, 'r') as zip_ref:
                zip_ref.extractall(GAME_FOLDER_PATH)
            os.remove(local_archive_path)
            with open(VERSION_FILE_PATH, 'w') as file:
                file.write(remote_version)
            print(f"Game successfully updated to version: {remote_version}")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press to Enter to exit...")

    # Launch the game
    game_exe_path = os.path.join(GAME_FOLDER_PATH, 'GAME.exe')
    subprocess.run(game_exe_path, shell=True)

    # Exit the script after launching the game
    sys.exit()

if __name__ == '__main__':
    update_game()
