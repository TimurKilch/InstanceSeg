import os
import json
from pycocotools.coco import COCO

# путь к файлу аннотации
annotation_file = 'train/_annotations.coco.json'

# путь к папке с изображениями
image_folder = 'train/'

# список идентификаторов изображений в аннотации
coco = COCO(annotation_file)
image_ids = coco.getImgIds()
sum = 0
# проход по всем файлам в папке с изображениями
for filename in os.listdir(image_folder):
    # проверка, является ли файл изображением
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        try:
            # проверка наличия изображения в аннотации
            image_id = int(filename.split('.')[0])
            if image_id not in image_ids:
                # удаление записи об изображении, если его нет в папке
                annotations = coco.getAnnIds(imgIds=image_id)
                coco.dataset['annotations'] = [ann for ann in coco.dataset['annotations'] if ann['id'] not in annotations]
                coco.dataset['images'] = [img for img in coco.dataset['images'] if img['id'] != image_id]
        except Exception as e:
            sum += 1
            print(f"{sum} : {e}")
# обновление аннотации в файле
with open(annotation_file, 'w') as f:
    json.dump(coco.dataset, f)
