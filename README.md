# Brain Cancer Segmentation 
> Computer Vision project for the course "AI Lab: Computer Vision and NLP (2022/2023)" at La Sapienza University of Rome. This project is part of the thesis "Brain Tumor Segmentation and Classification using Deep Learning" by Davide Belcastro.

https://user-images.githubusercontent.com/32139751/235325224-0c578cff-b594-4bff-a8f3-2afa922e5cfd.mov

## Requirements 
Dependecies used for the Segmentation:
- [cv2](https://pypi.org/project/opencv-python/)
- [sklearn](https://pypi.org/project/scikit-learn/)
- [numpy](https://pypi.org/project/numpy/)
- [matplotlib](https://pypi.org/project/matplotlib/)
- [h5py](https://pypi.org/project/h5py/)

Dependecies used for the GUI:
- [flet](https://pypi.org/project/flet/)

Activate a virtual environment:
```
python3 -m venv env
``` 

Before you can start installing packages in your virtual environment you'll need to activate it:
``` 
source env/bin/activate
``` 

You can use the requirements.txt file to install packages with pip:
``` 
pip3 install -r requirements.txt
```

## Dataset
>Two datasets were used:


The first dataset was downloaded from Kaggle, download it [here](https://www.kaggle.com/datasets/sartajbhuvaji/brain-tumor-classification-mri).
This contains 3264 files so divided, there are two directories: "Testing" and "Training", each directory contains other 4 directories: glioma, pituitary, meningioma, no-tumor.
The format of the images is ".jpg".


The second dataset was downloaded from Figshare, download it [here](https://figshare.com/articles/dataset/brain_tumor_dataset/1512427).
This directory contains 3064 contrast-enhanced T1-MRI performed on 233 patients with 3 different tumor types: meningioma (708), glioma (1426), and pituitary tumor (930).

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
### Brain tumor segmentation
GUI will open and you can select the image you want to segment (by clicking on the "Upload File" button) and then click on the "Start Segment" button to start the segmentation process. 

Once the segmentation is done, the GUI will show the original image (on the left) adn the segmented image (on the right). You can also see some stats about the segmentation process in the 2 columns under the images, the probability of the image to a Tumor and the area of the tumor (both in percentage).

Some documentation about what the buttons do:
- **Upload File**: Upload the image you want to segment. You can choose either a .mat file or an image file (.jpg, .png, .jpeg).
- **Start Segment**: Start the segmentation process (You need to upload a file first).
- **Save Output Image**: Save the output image from the segmentation process in a selected directory.
- **Clean**: Clean the directory that stores all the images (use it only if you want to delete all the images in the directory).

### Segmentation filters
After the segmentation process is done you can save the output image from the segmentation process and then apply some filters to it. We can select an image from the segmentation process (otherwise the filters will not work) and then select the filters we want to apply to the image (An explanation of what each filter does will be shown at the end) and then click on the "Generate Image" button to generate the image with the filters selected. The GUI will show the generated image on the right.

What each filter does:
- **Increment/Decrement Light** : Increase or decrease the amount of light inside the segmentation.
- **Color inside segmentation** : Color inside the segmentation.
- **Get only tumor** : Get only the segmented tumor from the image.
- **Without segmentation** : Get the image without the segmentation.

Some documentation about what the buttons do:
- **Upload Image**: Upload the image you want to apply the filters to. You can choose only an image file (.jpg, .png, .jpeg).
- **Generate Image**: Generate the image with the filter selected (You need to upload an image first and select an option for all the filters).
- **Save Output Image**: Save the generated image in a selected directory.
- **Clean**: Clean the directory that stores all the images (use it only if you want to delete all the images in the directory).

> **Warning**
> If there are any bugs or errors in the GUI, please contact us.

## Examples
> **Note**
> In this page we selected a .mat file that contains the image we want to segment and we clicked on the "Start Segment" button. The GUI will show the original image on the left and the segmented image on the right. Also we can see some stats that have been generated by the segmentation process under the 2 images. There is also a "Save output Image" button that will save the output image from the segmented in a selected directory, meanwhile the Clean button is used only for cleaning the directory that stores all the images (use it only if you want to delete all the images in the directory).

<img src="https://i.ibb.co/4KG1w0K/Screenshot-2023-04-29-at-20-53-23.png">

> **Note**
> In this page we selected the output image from the segmentation process and we selected the "Color inside segmentation" filter to see the segmentation in color. After the the "Generate Image" button is clicked the GUI will show the original image modified with the filter selected on the right. There is also a "Save output Image" button that will save the output image from the filter in a selected directory, meanwhile the Clean button is used only for cleaning the directory that stores all the images (use it only if you want to delete all the images in the directory).

<img src="https://i.ibb.co/PYM7ZLL/Screenshot-2023-04-29-at-20-54-20.png">

## License
> This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for more details.

## Credits
- Brain Cancer Segmentation developed by [Davide Belcastro](https://github.com/davidebelcastro-sig).
- GUI developed by [Lucian D. Crainic](https://github.com/LucianCrainic).
