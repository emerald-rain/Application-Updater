# ApplicationUpdater is a simple solution to update any application.

## How to upload new updates to Dropbox without changing the link
To update files in Dropbox without changing the link, use the file versioning feature. Dropbox will not change the link to a newly uploaded file with the same name, but will replace it. You can also check the file properties to see when and what version was uploaded. Update the version.txt in the same way.

## Features

- **Version Checking**: Compares the local application version with the remote version hosted on Dropbox.
- **Automatic Updates**: Downloads and extracts the update files if a newer version is found.
- **Directory Cleanup**: Option to clear the update directory before applying new updates.
- **Easy Configuration**: Simple configuration through Dropbox shared links and local paths.

## Configuration

Before running the script, configure the following variables in `main.py`:

- `DROPBOX_VERSION_LINK`: The direct Dropbox link to the version text file.
- `DROPBOX_ARCHIVE_LINK`: The direct Dropbox link to the application update ZIP file.
- `LOCAL_VERSION_FILE`: The path to the local version text file.
- `UPDATE_DIRECTORY`: The directory path where updates should be applied, set to the current working directory by default.
