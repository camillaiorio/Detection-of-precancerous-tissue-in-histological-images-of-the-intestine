# Detection-of-precancerous-tissue-in-histological-images-of-the-intestine
This project focuses on the classification of intestinal histological images into two categories: positive (regions affected by metaplasia) and negative (healthy tissue). 
The classification pipeline includes image preprocessing, segmentation mask generation from ROI files, and preparation of training, validation, 
and test datasets using the ImgDataset class.
Each image is paired with a segmentation mask where pixel values indicate:
* 1 – negative region (healthy)
* 2 – positive region (precancerous tissue)
* 0 – region of no interest

The segmentation masks are generated using annotation files (.roi) and the roi_utils module.
**Dataset note**
⚠️ The dataset used in this project is not publicly available. It is a private dataset provided by Professor Napoli and cannot be shared or redistributed. Any attempt to reproduce the results will require access to equivalent private histological image data.
