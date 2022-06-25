# YOLOv4-boat-detection
CNN made with YOLOv4 used for localizing and classifying boats in pictures and videos.

## Process

### clone darknet repo
`!git clone https://github.com/AlexeyAB/darknet`

### change makefile to have GPU and OPENCV enabled
`%cd darknet  
!sed -i 's/OPENCV=0/OPENCV=1/' Makefile  
!sed -i 's/GPU=0/GPU=1/' Makefile  
!sed -i 's/CUDNN=0/CUDNN=1/' Makefile  
!sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile`

### verify CUDA
`!/usr/local/cuda/bin/nvcc --version`

### make darknet (builds darknet so that you can then use the darknet executable file to run or train object detectors)
`!make`

### Import google drive
`from google.colab import drive
drive.mount('/content/drive')`

### Copy data from drive into darknet directory
`!cp -r /content/drive/MyDrive/Nadzor_luke/images/obj /content/darknet/data
!cp -r /content/drive/MyDrive/Nadzor_luke/images/test /content/darknet/data`

### download cfg to google drive and change its name
`!cp cfg/yolov4-custom.cfg /content/drive/MyDrive/Nadzor_luke/yolov4-obj.cfg`

### Change config file

### upload the custom .cfg back to cloud VM from Google Drive
`!cp /content/drive/MyDrive/Nadzor_luke/yolov4-obj.cfg ./cfg`

### upload the obj.names and obj.data files to cloud VM from Google Drive
`!cp /content/drive/MyDrive/Nadzor_luke/obj.names ./data
!cp /content/drive/MyDrive/Nadzor_luke/obj.data  ./data`

### upload the generate_train.py and generate_test.py script to cloud VM from Google Drive
`!cp /content/drive/MyDrive/Nadzor_luke/generate_test.py ./
!cp /content/drive/MyDrive/Nadzor_luke/generate_train.py ./`

### Something awesome
`!python generate_train.py
!python generate_test.py`

### Start training
`!wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137
!./darknet detector train /content/darknet/data/obj.data /content/darknet/cfg/yolov4-obj.cfg yolov4.conv.137 -dont_show -map`
