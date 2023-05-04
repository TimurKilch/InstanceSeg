import os
import torch
import numpy as np
from PIL import Image

from pycocotools.coco import COCO
from torchvision.datasets.vision import VisionDataset
import albumentations as A
from albumentations.pytorch import ToTensorV2

class COCOInstanceSegmentationDataset(VisionDataset):
    def __init__(self, root, ann_file, transforms=None):
        super(COCOInstanceSegmentationDataset, self).__init__(root)
        self.coco = COCO(ann_file)
        self.ids = list(sorted(self.coco.imgs.keys()))
        self.transforms = transforms

    def __getitem__(self, index):
        coco = self.coco
        img_id = self.ids[index]
        ann_ids = coco.getAnnIds(imgIds=img_id)
        annotations = coco.loadAnns(ann_ids)

        # Read the image
        path = coco.loadImgs(img_id)[0]['file_name']
        image = Image.open(os.path.join(self.root, path)).convert('RGB')

        # Read the masks
        masks = []
        for ann in annotations:
            mask = coco.annToMask(ann)
            masks.append(mask)
        masks = np.stack(masks, axis=0)

        # Convert to bounding boxes
        boxes = []
        for ann in annotations:
            x, y, w, h = ann['bbox']
            boxes.append([x, y, x + w, y + h])
        boxes = torch.as_tensor(boxes, dtype=torch.float32)

        # Labels and other attributes
        labels = [ann['category_id'] for ann in annotations]
        labels = torch.as_tensor(labels, dtype=torch.int64)

        iscrowd = [ann['iscrowd'] for ann in annotations]
        iscrowd = torch.as_tensor(iscrowd, dtype=torch.uint8)

        target = {
            'boxes': boxes,
            'labels': labels,
            'masks': masks,
            'image_id': torch.tensor([img_id], dtype=torch.int64),
            'area': torch.as_tensor([ann['area'] for ann in annotations], dtype=torch.float32),
            'iscrowd': iscrowd
        }

        if self.transforms:
            transformed = self.transforms(image=np.array(image), mask=masks, bboxes=boxes, labels=labels)
            image = transformed['image']
            target['masks'] = np.array(transformed['mask'])
            target['boxes'] = torch.tensor(transformed['bboxes'], dtype=torch.float32)
            target['labels'] = torch.tensor(transformed['labels'], dtype=torch.int64)

        return image, target

    def __len__(self):
        return len(self.ids)

def get_transforms(train=True):
    transforms = []
    if train:
        transforms.append(A.HorizontalFlip(p=0.5))
        # Add more data augmentation techniques if needed
    transforms.extend([
        A.Resize(height=512, width=512, p=1),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225], max_pixel_value=255.0, p=1),
        ToTensorV2()
    ])
    return A.Compose(transforms, bbox_params=A.BboxParams(format='pascal'))


#########################################################

# Set up the pre-trained Mask R-CNN model
model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)

# Replace the classifier with a new one for your number of classes
num_classes = 4
in_features = model.roi_heads.box_predictor.cls_score.in_features
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
hidden_layer = 256
model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask, hidden_layer, num_classes)

# Set up the data loaders for your train, valid, and test sets
train_dataset = COCOInstanceSegmentationDataset(root='train', ann_file='/content/drive/MyDrive/Buildings_Instance_Segmentation.v1-raw-images.coco/annotations/instances_train.json', transforms=get_transforms(train=True))
train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True, num_workers=2, collate_fn=collate_fn)

valid_dataset = COCOInstanceSegmentationDataset(root='valid', ann_file='/content/drive/MyDrive/Buildings_Instance_Segmentation.v1-raw-images.coco/annotations/instances_val.json', transforms=get_transforms(train=False))
valid_loader = DataLoader(valid_dataset, batch_size=2, shuffle=False, num_workers=2, collate_fn=collate_fn)

test_dataset = COCOInstanceSegmentationDataset(root='test', ann_file='/content/drive/MyDrive/Buildings_Instance_Segmentation.v1-raw-images.coco/annotations/instances_test.json', transforms=get_transforms(train=False))
test_loader = DataLoader(test_dataset, batch_size=2, shuffle=False, num_workers=2, collate_fn=collate_fn)

# Set up the optimizer and the learning rate scheduler
params = [p for p in model.parameters() if p.requires_grad]
optimizer = torch.optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)
lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.1)

############################################################################

for images, target in train_dataset:
  try:
    images
  except Exception as e:
    print(e)
#на пк проверить каких файлов нет и удалить нахуй

