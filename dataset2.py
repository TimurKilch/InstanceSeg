import json
import os

# Path to the COCO annotation file
annotation_path = 'train/_annotations_coco.json'

# Path to the folder containing the images
image_folder_path = 'train/'

# Load the annotation file
with open(annotation_path, 'r') as f:
    annotation = json.load(f)

# Get the list of image filenames from the annotation
image_filenames = [img['file_name'] for img in annotation['images']]

# Get the list of image filenames in the image folder
folder_image_filenames = os.listdir(image_folder_path)

# Remove images from the image folder for which there is no information in the annotation
for filename in folder_image_filenames:
    if filename not in image_filenames:
        os.remove(os.path.join(image_folder_path, filename))

# Remove entries from the annotation for images that are missing from the image folder
new_images = []
new_annotations = []
for img in annotation['images']:
    if img['file_name'] in folder_image_filenames:
        new_images.append(img)
        for ann in annotation['annotations']:
            if ann['image_id'] == img['id']:
                new_annotations.append(ann)

annotation['images'] = new_images
annotation['annotations'] = new_annotations

# Save the new annotation file
with open(annotation_path, 'w') as f:
    json.dump(annotation, f)
