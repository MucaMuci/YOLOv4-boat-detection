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
After we're done with creating them, we just need to upload them from our local storage to google drive. From there we will run:
```
!cp /content/drive/MyDrive/Nadzor_luke/obj.names ./data  
!cp /content/drive/MyDrive/Nadzor_luke/obj.data  ./data
```
### Upload the generate_train.py and generate_test.py script
Now we need to create train.txt and test.txt files as we said. To help you with that, you can run generate_train.py and generate_test.py scripts. But first, we have to transfer them from Google Drive to cloud VM: 
```
!cp /content/drive/MyDrive/Nadzor_luke/generate_test.py ./  
!cp /content/drive/MyDrive/Nadzor_luke/generate_train.py ./
```

### Generate train.txt and test.txt
now we just need to run these two scripts:
```
!python generate_train.py  
!python generate_test.py
```

### Get pretrained weights
This step downloads the weights for the convolutional layers of the YOLOv4 network. By using these weights it helps your custom object detector to be way more accurate and not have to train as long. You don't have to use these weights but trust me it will help your modle converge and be accurate way faster.
```
!wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137  
```
### Start training
With that, everything is ready for training. Now we just need to run it. Uncomment %%capture below if you run into memory issues or your Colab is crashing:  
```
# %%capture
!./darknet detector train /content/darknet/data/obj.data /content/darknet/cfg/yolov4-obj.cfg yolov4.conv.137 -dont_show -map
```
### Training...
This training could take several hours depending on how many iterations you chose in the .cfg file. You will want to let this run as you sleep or go to work for the day, etc. However, Colab Cloud Service kicks you off it's VMs if you are idle for too long (30-90 mins). To avoid this hold (CTRL + SHIFT + i) at the same time to open up the inspector view on your browser. Paste the following code into your console window and hit Enter.  

```javascript
function ClickConnect(){
console.log("Working"); 
document
  .querySelector('#top-toolbar > colab-connect-button')
  .shadowRoot.querySelector('#connect')
  .click() 
}
setInterval(ClickConnect,50000)
```
### Colab crashes
If for some reason you get an error or your Colab goes idle during training, you have not lost your partially trained model and weights! Every 100 iterations a weights file called yolov4-obj_last.weights is saved to /content/drive/MyDrive/Nadzor_luke/backup folder (wherever your backup folder is). This is why we created this folder in our Google drive and not on the cloud VM. If your runtime crashes and your backup folder was in your cloud VM you would lose your weights and your training progress. We can kick off training from our last saved weights file so that we don't have to restart. Just run the following command but with your backup location.
```
!./darknet detector train data/obj.data cfg/yolov4-obj.cfg /content/drive/MyDrive/Nadzor_luke/backup/yolov4-obj_last.weights -dont_show
```
kick off training from where it last saved:
```
!./darknet detector train data/obj.data cfg/yolov4-obj.cfg /content/drive/MyDrive/Nadzor_luke/backup/yolov4-obj_last.weights -dont_show
```
### show chart.png of how custom object detector did with training
After training, you can observe a chart of how your model did throughout the training process by running the below command. It shows a chart of your average loss vs. iterations. For your model to be 'accurate' you should aim for a loss under 2. If you stop training or it crashes during training you can still check accuracy of your model in the next steps.
```
imShow('chart.png')
```
###  Checking the Mean Average Precision (mAP) of Your Model
If you didn't run the training with the '-map- flag added then you can still find out the mAP of your model after training. Run the following command on any of the saved weights from the training to see the mAP value for that specific weight's file. I would suggest to run it on multiple of the saved weights to compare and find the weights with the highest mAP as that is the most accurate one. If you think your final weights file has overfitted then it is important to run these mAP commands to see if one of the previously saved weights is a more accurate model for your classes:
```
!./darknet detector map data/obj.data cfg/yolov4-obj.cfg /content/drive/MyDrive/Nadzor_luke/backup/yolov4-obj_1000.weights
```
### Testing
You now have a custom object detector to make your very own detections. Time to test it out. Need to set our custom cfg to test mode:   
```
%cd cfg
!sed -i 's/batch=64/batch=1/' yolov4-obj.cfg
!sed -i 's/subdivisions=16/subdivisions=1/' yolov4-obj.cfg
%cd ..
```
Run your custom detector. Upload an image to your google drive to test, thresh flag sets accuracy that detection must be in order to show it:
```
!./darknet detector test data/obj.data cfg/yolov4-obj.cfg /content/drive/MyDrive/Nadzor_luke/backup/yolov4-obj_last.weights /mydrive/images/boatTest.jpg -thresh 0.3
imShow('predictions.jpg')
```
