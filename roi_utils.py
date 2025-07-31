import cv2 as cv
from read_roi import read_roi
import numpy as np
import os
from typing import List,Dict,Union
import re

def imageRoiDict(roifolder:str, imfloder:str) -> Dict[str,List[str]]:
    d:Dict[str,List[str]] = {}
    impaths = os.listdir(imfloder)
    for p in os.listdir(roifolder):
        m = re.match(r"^([0-9]+_corpus_BLI_[0-9])+_[0-9]+\.roi",p)
        if m:
            imname = m.group(1) + ".JPG"
            if imname in impaths:
                impath = os.path.join(imfloder,imname)
                roipath = os.path.join(roifolder,p)
                if impath not in d:
                    d[impath] = [roipath]
                else:
                    d[impath].append(roipath)
    return d

def roi2Mask(roifiles:List[str], heigth:int, width:int, labels: Union[List[int],int,str] = "group")->np.ndarray:
    mask = np.zeros((heigth,width,1),dtype = "uint8")
    for i,f in enumerate(roifiles):
        
        roi = read_roi.read_roi_file(f)
        fname = os.path.split(f)[1]
        fname_noext = os.path.splitext(fname)[0]
        #print(roi)
        #print(f)
        color = None
        if type(labels) == list:
            color = labels[i]
        elif type(labels) == int:
            color = labels
        elif type(labels) == str and labels == "group":
            #if 'group' not in roi[fname_noext]: 
              #print('error', fname_noext)
              #continue
            color = roi[fname_noext]["group"]
        else:
            raise ValueError("Unexpected value for parameter labels: \
                it shoud be list of int or int or 'group'")
      
        if roi[fname_noext]["type"] == "rectangle":
            left = roi[fname_noext]["left"]
            top = roi[fname_noext]["top"]
            width = roi[fname_noext]["width"]
            height = roi[fname_noext]["height"]
            cv.rectangle(mask,
                (left,top),
                (left+width,top+height),
                color=color,
                thickness=-1)

        elif roi[fname_noext]["type"] == "freehand":
            x = roi[fname_noext]["x"]
            y = roi[fname_noext]["y"]
            pts = np.array([[xx,yy] for xx,yy in zip(x,y)],np.int32)
            pts = pts.reshape((-1,1,2))
            cv.fillPoly(mask,[pts],color=color)
        
        elif roi[fname_noext]["type"] == "oval":
            left = roi[fname_noext]["left"]
            top = roi[fname_noext]["top"]
            width = roi[fname_noext]["width"]
            height = roi[fname_noext]["height"]
            center = (left + width//2, top + height//2)
            axes = (width//2, height//2)
            cv.ellipse(mask,
                center, 
                axes, 
                angle=0, 
                startAngle=0, endAngle=360, 
                color=color, thickness=-1)

        else:
            raise ValueError(f"Unknown roi type: {roi[fname_noext]['type']}")
    return mask

