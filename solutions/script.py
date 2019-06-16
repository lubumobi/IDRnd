#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os

from IDRnD.utils import Train, seed_everything
from IDRnD.augmentations import ToMellSpec, PadOrClip, ToTensor
from IDRnD.dataset import Test_Dataset
from IDRnD.resnet import resnet34

import pandas as pd
import numpy as np
import librosa
import torch
from torch.utils.data import DataLoader
from torchvision.transforms import transforms

seed_everything(0)


# In[2]:


dataset_dir = "."

eval_protocol_path = "protocol_test.txt"
eval_protocol = pd.read_csv(eval_protocol_path, sep=" ", header=None)
eval_protocol.columns = ['path', 'key']
eval_protocol['score'] = 0.0
#eval_protocol['path'] = eval_protocol['path'].apply(lambda x: os.path.join(dataset_dir, x))


# In[2]:


post_transform = transforms.Compose([
    ToMellSpec(n_mels=128),
    librosa.power_to_db,
    PadOrClip(150),
    ToTensor(),
])


# ### predict

# In[3]:



# In[4]:


hm = Train()

test_dataset = Test_Dataset(np.array(eval_protocol["path"]), post_transform)
#test_dataset = Test_Dataset(X[:300], post_transform)

test_loader = DataLoader(test_dataset, batch_size=50, shuffle=False)

model = resnet34(num_classes=1).cuda()

#model.load_state_dict(torch.load('models/simple_old_conv.pt'))
#model_dst = torch.nn.DataParallel(model, device_ids=[0, 1]).cuda()
#torch.save(model_dst.module.state_dict(),  'models/kaggle2_nonparallel.pt')
model.eval()
model.load_state_dict(torch.load('models/kaggle2_nonparallel.pt'))
pred = hm.predict_on_test(test_loader, model)


# In[7]:


eval_protocol["score"] = pred.values
eval_protocol[['path', 'score']].to_csv('answers.csv', index=None)