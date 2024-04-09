from io import BytesIO
from zipfile import ZipFile
import os


# Возвращает название файла без его расширения
def remove_extension(file):
    extension_pos = file.rfind(".")
    if extension_pos >= 0:
        return file[:extension_pos]
    else:
        return file


# Удаление файла
def remove_file(file):
    # Если файл существует
    if os.path.exists(file):
        os.remove(file)


# Удаление списка файлов
def remove_files(files):
    for file in files:
        # Удаление файла
        remove_file(file)


# Создание zip-архива со списком файлов
def make_zip_archive(files):
    stream = BytesIO()
    with ZipFile(stream, 'w') as zf:
        for file in files:
            zf.write(file, file)
    stream.seek(0)
    return stream
