# Game Updater Documentation

## Overview
This script automates the process of keeping a game up to date by comparing the local game version with the version available on Dropbox. If the Dropbox version is newer, the script downloads the updated game archive, replaces the old files, and launches the updated game.

## Requirements
- Python 3.x
- Dropbox SDK for Python
- An active internet connection

## Setup
1. **Install Dropbox SDK**: Run `pip install dropbox` to install the Dropbox SDK for Python.
2. **Access Token**: Obtain a Dropbox API access token and insert it into the `ACCESS_TOKEN` variable in the script.

## How It Works
1. **Version Check**: The script compares the local version of the game, read from `version.txt`, against the version available on Dropbox.
2. **Download & Update**: If Dropbox has a newer version, the script downloads the updated game archive (.zip), deletes the old game files (except for `launcher.exe` and `version.txt`), and extracts the new files into the game directory.
3. **Launch Game**: After updating, the script launches the game executable (`GAME.exe`).

## Usage
1. Navigate to the script's directory.
2. Run the script using Python: `python script_name.py`
3. The script checks for updates and launches the game.

## Note
- Ensure the `ACCESS_TOKEN` is kept secure and not shared publicly.
- The script assumes the game archive on Dropbox and the local version are both named according to their version (e.g., `1.0.0.zip`).

## Troubleshooting
- **Permission Errors**: Ensure the script has the necessary permissions to delete and write files in the game directory.

## Conclusion
This script simplifies keeping your game updated and reduces manual work. Ensure you have the correct permissions and your Dropbox API access token is valid to avoid any disruptions.
