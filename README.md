# video-watermark
Add watermark to video sample with python

## Description
This is a sample python app that adds a watermark(png) to a video(mp4) file. It places the watermak on the bottom righ corner of the video. The inputs folder contains the sample watermak and video file and the output folder will contain the generated video file with embedded watermark. The watermark fade-in affect is set is set to 0.12 (0.0 - 1.0). If watermark size is greater than 1/4 of the video frame size we'll decrease watermark size by half recursively.


## Getting started
Install libraries
```sh
pip install opencv-python
```
  
Run python main.py file
```sh
python main.py
```
