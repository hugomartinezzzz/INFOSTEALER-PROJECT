from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/drive']


def authenticate():
    credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    return service


def list_files():
    service = authenticate()
    try:
        results = service.files().list().execute()
        files = results.get('files', [])

        if not files:
            print('No se encontraron archivos.')
        else:
            print('Archivos en Google Drive:')
            for file in files:
                print(f'Nombre: {file["name"]}, ID: {file["id"]}')

    except Exception as e:
        print('Se produjo un error:', e)


def download_file(file_id, file_name):
    service = authenticate()
    try:
        request = service.files().get_media(fileId=file_id)
        file_metadata = service.files().get(fileId=file_id).execute()
        file_extension = os.path.splitext(file_metadata['name'])[1]
        if file_extension:
            file_name += file_extension
        fh = open(file_name, 'wb')
        downloader = request.execute()
        fh.write(downloader)
        fh.close()
        print('Archivo descargado con éxito.')
    except Exception as e:
        print('Se produjo un error:', e)

# Mostrar la lista de archivos en Google Drive


list_files()

# Solicitar al usuario que ingrese la ID del archivo
file_id = input('Ingrese la ID del archivo que desea descargar: ')

# Solicitar al usuario que ingrese el nombre deseado del archivo descargado (sin extensión)
file_name = input('Ingrese el nombre deseado para el archivo descargado (sin extensión): ')

# Llamar a la función download_file con los parámetros ingresados por el usuario
download_file(file_id, file_name)





