# YOLOv4-boat-detection
We used YOLOv4 for localizing and classifying boats in pictures and videos. Training was done on GoogleColab. There are two main parts of this project.
1. Collecting data
2. Configuring and training YOLOv4 model  

## Collecting data
YOLOv4 requires labeled pictures in .jpg format. We used VLC media player to extract frames (pictures) from videos. To label those images we used LabelImg.

## Configuring and training YOLOv4 model
### Clone darknet repo
First thing we need to do is clone the AlexeyAB's darknet repo from github:
```
!git clone https://github.com/AlexeyAB/darknet
```
### Change makefile
We changed the makefile to have GPU and OPENCV enabled:
```
%cd darknet    
!sed -i 's/OPENCV=0/OPENCV=1/' Makefile    
!sed -i 's/GPU=0/GPU=1/' Makefile    
!sed -i 's/CUDNN=0/CUDNN=1/' Makefile  
!sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile
```
### Verify CUDA
Simple verification that CUDA is enabled:
```
!/usr/local/cuda/bin/nvcc --version
```

### Make darknet
We run makefile commands to build darknet so that we can then use the darknet executable file to run or train object detectors:
```
!make
```

### Import google drive
You'll store all your data (obj and test folders with pictures and .txt files) on google drive. To be able to easily work with our custom data, we will eventually move it in darknet directory. Firstly, we must import our google drive:
```
from google.colab import drive  
drive.mount('/content/drive')
```

### Copy data from drive into darknet directory
Now we copy all folders from our drive into the darknet/data folder:
```
!cp -r /content/drive/MyDrive/Nadzor_luke/images/obj /content/darknet/data  
!cp -r /content/drive/MyDrive/Nadzor_luke/images/test /content/darknet/data  
```
### Download config file
Now we have to start with YOLOv4 configuration. Firstly, download cfg file to google drive and change its name:
```
!cp cfg/yolov4-custom.cfg /content/drive/MyDrive/Nadzor_luke/yolov4-obj.cfg
```
### Change config file
Open it locally in visual studio code, or any text editor. We have to change few parameters based on our data:  
  
#### Training batch and subdivisions  
For optimal results set batch size to 64 and subdivision on 16 (32 if needed).
  
#### Width and height
It has to be any multiple of 32. **416 is standard**, but you can sometimes improve results by making value larger like 608, but it will slow down the training.

#### Max_batches
In our case, we set max_batches to 18000. It is defined as *number_of_classes* * *2000* with exception for projects with one or two classes, where *max_batches = 6000* is standard.

#### Steps
In our case, we set steps to 14400 and 16200. Usually it is defined as **steps=0.8 * *Max_batches*,0.9 * *Max_batches***

![image](https://user-images.githubusercontent.com/92891601/175809318-84587f10-9404-4277-9d05-cccb25c6b16d.png)

#### Filters
Filters is defined as (*number_of_classes +5*) * *3*. So in our case, filters was set to (9+5) * 3 = 42. We will use this in the next step.

#### YOLO layers
There are three YOLO layers defined near the bottom of the config file. Last two things we need to do are:
1. Change number of classes in each of YOLO layers (In our case *classes = 9*).  
2. Change number of filters in first Convolutional layer before each YOLO layer.  

![image](https://user-images.githubusercontent.com/92891601/175809590-20766bfa-0b1d-42b3-99ae-419815dc5a89.png)


#### Random
If you run into memory issues or find the training taking a super long time. In the last yolo layer in the cfg, change one line from random = 1 to random = 0 to speed up training but slightly reduce accuracy of model. **It will also help save memory** if you run into any memory issues.

### Upload config file
After changing all the necessary data in config file, upload it back to google drive. From there we have to transfer it back to cloud VM:
```
!cp /content/drive/MyDrive/Nadzor_luke/yolov4-obj.cfg ./cfg
```
### Create obj.names
Create a new file within a code or text editor called obj.names where you will have one class name per line in the same order as your classes.txt from the dataset generation step. **You do not want to have spaces in your class name**.

![image](https://user-images.githubusercontent.com/92891601/175810060-2bd4077b-6074-4fc6-b4ce-7257bf12e51e.png)

### Create obj.data
Create a new file within a code or text editor called obj.data where you will have paths to folders necessary for training. Don't worry about train.txt and test.txt files, we'll create them next. This backup path is where we will save the weights to of our model throughout training. Create a backup folder in your google drive and put its correct path in this file.  
![image](https://user-images.githubusercontent.com/92891601/175810113-94797b7b-c4ad-4f8f-968e-a995160f05d7.png)

### Upload the obj.names and obj.data
After we're done with creating them, we just need to upload them first from our local storage to google drive, from where we will run:
```
!cp /content/drive/MyDrive/Nadzor_luke/obj.names ./data  
!cp /content/drive/MyDrive/Nadzor_luke/obj.data  ./data
```
### upload the generate_train.py and generate_test.py script to cloud VM from Google Drive
```
!cp /content/drive/MyDrive/Nadzor_luke/generate_test.py ./  
!cp /content/drive/MyDrive/Nadzor_luke/generate_train.py ./
```

### Generate train.txt and test.txt
```
!python generate_train.py  
!python generate_test.py
```

### Start training
```
!wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137  
!./darknet detector train /content/darknet/data/obj.data /content/darknet/cfg/yolov4-obj.cfg yolov4.conv.137 -dont_show -map
```
