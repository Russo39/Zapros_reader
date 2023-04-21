import os

request_dir = 'Запросы'

def check_and_remove_xlsx():
    file_list = []
    with os.scandir(request_dir) as files:
        for file in files:
            if file.name.endswith('.xlsx'):
                file_list.append(file.name)
                print(file.name)
    if len(file_list) != 0:
        for i in file_list:
            os.remove(f'{request_dir}\\{i}')

def delete_single_xlsx(filepath_and_name):
    os.remove(filepath_and_name)

def check_request_folder():
    check_folder = os.path.exists('Запросы')
    if check_folder != True:
        os.mkdir("Запросы") 