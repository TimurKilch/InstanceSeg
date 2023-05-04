import os
import json
from pycocotools.coco import COCO
###################################################### Чистилка датасета от лишних записей в аннотации #####################
# путь к файлу аннотации
annotation_file = 'test/_annotations.coco.json'

# путь к папке с изображениями
image_folder = 'test/'

# список имен файлов в папке с изображениями
file_names = os.listdir(image_folder)

# загрузка аннотации
coco = COCO(annotation_file)

# список информации об изображениях в аннотации
images_info = coco.loadImgs(coco.getImgIds())

# проход по всем изображениям в аннотации
for image_info in images_info:
    # получение имени файла из информации об изображении
    file_name = image_info['file_name']

    # проверка наличия файла
    if file_name not in file_names:
        print(file_name)
        # удаление записи об изображении, если его нет в папке
        image_id = image_info['id']
        annotations = coco.getAnnIds(imgIds=image_id)
        coco.dataset['annotations'] = [ann for ann in coco.dataset['annotations'] if ann['id'] not in annotations]
        coco.dataset['images'] = [img for img in coco.dataset['images'] if img['id'] != image_id]

# обновление аннотации в файле
with open(annotation_file, 'w') as f:
    json.dump(coco.dataset, f)
    print(f"{file_name} deleted")
