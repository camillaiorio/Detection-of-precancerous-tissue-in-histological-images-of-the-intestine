import random
from typing import List
import matplotlib.pyplot as plt
import roi_utils
import cv2 as cv
import constants
import numpy as np
import os

class ImgDataset:
    """
    Iterable over the images with the corresponding ground truth segmentation.
    The values of the segmentation mask are:
    1 -> for negative regions
    2 -> for positive regions
    """
    def __init__(self,split:str):
        self.train_size=.8
        self.val_size=.1
        self.random_seed=9

        positive_im_roi_dict = roi_utils.imageRoiDict(constants.POSITIVE_ROI_PATH,constants.POSITIVE_IMG_PATH)
        negative_im_roi_dict = roi_utils.imageRoiDict(constants.NEGATIVE_ROI_PATH,constants.NEGATIVE_IMG_PATH)
        
        random.seed(self.random_seed)
        positive = sorted(positive_im_roi_dict.keys())
        negative = sorted(negative_im_roi_dict.keys())
        if split=="train":
            positive = positive[0:round(len(positive)*self.train_size)]
            negative = negative[0:round(len(negative)*self.train_size)]
        elif split=="test":
            positive = positive[round(len(positive)*self.train_size) + round(len(positive)*self.val_size):]
            negative = negative[round(len(negative)*self.train_size) + round(len(negative)*self.val_size):]
        elif split=="val":
            positive = positive[round(len(positive)*self.train_size):round(len(positive)*self.train_size) + round(len(positive)*self.val_size)]
            negative = negative[round(len(negative)*self.train_size):round(len(negative)*self.train_size) + round(len(negative)*self.val_size)]
        else:
            raise ValueError("Unexpected value for argument 'split', accetted values are 'train','test','val'")

        self.samples = positive + negative
        self.im_roi_dict = {**positive_im_roi_dict, **negative_im_roi_dict}
        random.shuffle(self.samples)
        self.idx = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.idx >= len(self.samples):
            raise StopIteration()
        path = self.samples[self.idx]
        img = cv.imread(path)
        img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        label = 0
        if 'positive' in path:
          label = 2
        elif 'negative' in path:
          label = 1
        mask = roi_utils.roi2Mask(self.im_roi_dict[path],img.shape[0],img.shape[1],label)
        self.idx += 1
        return img,mask
    