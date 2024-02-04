import dropbox
from dropbox.files import WriteMode

def upload_to_dropbox(file_path_local, file_path_dropbox, access_token):
    dbx = dropbox.Dropbox(access_token)

    try:
        with open(file_path_local, 'rb') as f:
            dbx.files_upload(f.read(), file_path_dropbox, mode=WriteMode('overwrite'))
        print(f'File {file_path_local} has been successfully uploaded to Dropbox at path {file_path_dropbox}')
    except dropbox.exceptions.ApiError as e:
        print(f'An error occurred while using the Dropbox API: {e}')

# Замените значения ниже на ваши реальные данные
local_file_path = r'C:\Users\Angelica\Documents\GitHub\Unity-Game-Update-Launcer\1.4.1.zip'
dropbox_file_path = '/1.4.1.zip'
your_access_token = ''

# Вызов функции загрузки
upload_to_dropbox(local_file_path, dropbox_file_path, your_access_token)
