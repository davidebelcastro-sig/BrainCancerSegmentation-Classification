## Brain Cancer Segmentation 
> Computer Vision project for the BSc in Computer Science at La Sapienza University of Rome. 

<p float="left">
  <img src="https://i.ibb.co/4KG1w0K/Screenshot-2023-04-29-at-20-53-23.png" width="370" />
  <img src="https://i.ibb.co/PYM7ZLL/Screenshot-2023-04-29-at-20-54-20.png" width="370" /> 
</p>

### Requirements 
Dependecies used for the Segmentation:
- [cv2](https://pypi.org/project/opencv-python/)
- [sklearn](https://pypi.org/project/scikit-learn/)
- [numpy](https://pypi.org/project/numpy/)
- [matplotlib](https://pypi.org/project/matplotlib/)
- [h5py](https://pypi.org/project/h5py/)

Dependecies used for the GUI:
- [flet](https://pypi.org/project/flet/)

You can use the requirements.txt file to install this dependencies with pip:
``` 
pip3 install -r requirements.txt
```

### Dataset
> Dataset was downloaded from Kaggle, download it [here](https://figshare.com/articles/dataset/brain_tumor_dataset/1512427).

The dataset contains 3064 contrast-enhanced T1-MRI performed on 233 patients with 3 different tumor types: meningioma (708), glioma (1426), and pituitary tumor (930).

The dataset is divided into 4 directories containing 766 files each.

Each file is in matlab(.mat) format and contains the following information :
- cjdata.label: 1 for meningioma, 2 for glioma, 3 for pituitary tumor
- cjdata.PID: patient ID
- cjdata.image: image data
- cjdata.tumorBorder
- cjdata.tumorMask: a binary image with 1s indicating tumor region

The last lines of the README.txt file present in the dataset are shown.
This data was used in the following paper: 1. Cheng, Jun, et al. ”Enhanced Performance of Brain Tumor Classification via Tumor Region Augmentation and Partition.” PloS one 10.10 (2015). 2. Cheng, Jun, et al. "Retrieval of Brain Tumors by Adaptive Spatial Pooling and Fisher Vector Representation." PloS one 11.6 (2016). Matlab source codes are available on [github](https://github.com/chengjun583/brainTumorRetrieval).
## Usage
Install the requirements and run the main.py file or run the .sh file.
```
./run.sh
``` 

### Examples
> TODO


## License
> This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for more details.

## Credits
- Brain Cancer Segmentation developed by [Davide Belcastro]().
- GUI developed by [Lucian D. Crainic]().
