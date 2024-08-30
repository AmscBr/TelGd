#Lista todos os diretorios e ids da raiz do Gdrive

"""from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

file_list = drive.ListFile({'q' : "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    print('title: %s, id: %s' % (file1['title'], file1['id']))"""

#Lista as subpastas de um diretorio especifico no caso "garagem  id = '1sWxe1yxrPUWGtgKO1iO7Ykf_e-xDbtKh'"

"""from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

file_list = drive.ListFile({'q' : "'1sWxe1yxrPUWGtgKO1iO7Ykf_e-xDbtKh' in parents and trashed=false"}).GetList()
for file1 in file_list:
    print('title: %s, id: %s' % (file1['title'], file1['id']))"""

# Função para listar todas as subpastas recursivamente

"""from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

def list_all_subfolders(parent_id, indent=0):
    query = f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    folder_list = drive.ListFile({'q': query}).GetList()
    
    for folder in folder_list:
        print(' ' * indent + 'title: %s, id: %s' % (folder['title'], folder['id']))
        # Chama a função recursivamente para listar subpastas dentro desta pasta
        list_all_subfolders(folder['id'], indent + 4)

# ID do diretório pai
parent_id = '1sWxe1yxrPUWGtgKO1iO7Ykf_e-xDbtKh'

# Chamar a função
list_all_subfolders(parent_id)"""

#Retorna a ID do Título de um arquivo

from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

def get_id_of_title(title, parent_directory_id):
    foldered_list = drive.ListFile({'q': "'"+parent_directory_id+"' in parents and trashed=false"}).GetList()
    for file in foldered_list:
        if file['title'] == title:
            return file['id']
    return None

# ID do diretório "garagem"
parent_directory_id = '1sWxe1yxrPUWGtgKO1iO7Ykf_e-xDbtKh'

# Exemplo de uso da função
title = '2024'
file_id = get_id_of_title(title, parent_directory_id)
print(f'O ID do arquivo "{title}" é: {file_id}')









