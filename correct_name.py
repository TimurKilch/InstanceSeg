import os

dir_path = 'train/'

for filename in os.listdir(dir_path):
    file_path = os.path.join(dir_path, filename)
    if os.path.isfile(file_path):
        # Разбиваем имя файла на список по последней точке
        name, extension = filename.rsplit('.', 1)
        # Заменяем все точки на символ подчеркивания
        name = name.replace('.', '_')
        # Объединяем имя файла с расширением
        new_filename = f"{name}.{extension}"
        # Изменяем название файла на новое
        os.rename(file_path, os.path.join(dir_path, new_filename))
