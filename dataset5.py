import os
import json
from pycocotools.coco import COCO

# путь к файлу аннотации
annotation_file = 'train/_annotations.coco.json'

# путь к папке с изображениями
image_folder = 'train/'

# список имен файлов в папке с изображениями
file_names = os.listdir(image_folder)

# загрузка аннотации
coco = COCO(annotation_file)

# список идентификаторов изображений в аннотации
image_ids = coco.getImgIds()

# проход по всем файлам в папке с изображениями
for file_name in file_names:
    # проверка, является ли файл изображением
    if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
        # проверка наличия изображения в аннотации
        image_id = int(file_name.split('.')[0])
        if image_id not in image_ids:
            # удаление файла, если его нет в аннотации
            os.remove(os.path.join(image_folder, file_name))

# обновление списка файлов после удаления
file_names = os.listdir(image_folder)

# проход по всем изображениям в аннотации
for image_id in image_ids:
    # получение имени файла из информации об изображении
    image_info = coco.loadImgs(image_id)[0]
    file_name = image_info['file_name']

    # проверка наличия файла
    if file_name not in file_names:
        print(file_name)
        print(f"Image with ID {image_id} and file name {file_name} will be deleted.")
        # удаление записи об изображении, если его нет в папке
        annotations = coco.getAnnIds(imgIds=image_id)
        coco.dataset['annotations'] = [ann for ann in coco.dataset['annotations'] if ann['id'] not in annotations]
        coco.dataset['images'] = [img for img in coco.dataset['images'] if img['id'] != image_id]

# обновление аннотации в файле
with open(annotation_file, 'w') as f:
    json.dump(coco.dataset, f)
