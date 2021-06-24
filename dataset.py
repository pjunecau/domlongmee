from torch.utils.data import DataLoader, Dataset
import numpy as np
import pandas as pd
import cv2
import albumentations as A
from albumentations.pytorch import ToTensorV2
from utils import CFG


class CassavaDataset(Dataset):
    def __init__(self,df, file_path=None, uploaded_image=None, transform=None, uploaded_state=False, demo_state=True):
        self.df = df
        self.file_path= file_path
        self.uploaded_image = uploaded_image
        self.file_names = df['image_id'].values
        self.transform = transform
        self.uploaded_state= uploaded_state
        self.demo= demo_state
        
    def __len__(self):
        return len(self.df)

        
    def __getitem__(self, idx):
        file_name = self.file_names[idx]
        file_path = self.file_path
        if self.demo:
            image = cv2.imread(file_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if self.uploaded_state:
            image = cv2.imdecode(np.fromstring(self.uploaded_image.read(), np.uint8), 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']
        return image



def get_transforms(*, data):
    if data == 'valid':
        return A.Compose([
            A.Resize(CFG.size, CFG.size),
            A.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
            ToTensorV2(),
        ])


labels= ['Cassava Bacterial Blight (CBB)', 'Cassava Brown Streak Disease (CBSD)', 'Cassava Green Mottle (CGM)','Cassava Mosaic Disease (CMD)', 'គ្មានជំងឺ']
classes_map= { 'ប្រភេទជំងឺ': labels}
classes= pd.DataFrame(classes_map)
