# Description
The python class `data.ImgDataset` implements an iterator over the images and their corresponding segmentation mask.
Instantiate the class specifying the split, one of `test | train | val`. The iterator initializes the random seed 
so that the results are reproducible. The the values of the segmentation mask are:
- 1 : negative region (not affected by metaplasia)
- 2 : positive region (affeted by metaplasia)
- 0 : region of no interest

# Instructions
- Install read_roi from source: `$ pip install ./read-roi/`
- Update the paths in `constants.py`

# Dependencies
- matplotlib==3.7.0
- opencv==4.6.0
- numpy==1.23.5