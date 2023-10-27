# This projects adds a watermark to a video file
# The watermark is a png file with transparency
# The watermark is added to the bottom right corner of the video
# If the watermark is greater than 1/4 of the video frame size, we'll decrease watermak size accordingly

import cv2
import os
import sys
import logging

from helper import resize_watermark

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# Constants
input_folder = "inputs"
output_folder = "outputs"
video_file_name = "video.mp4"
watermark_file_name = "watermark.png"
watermark_beta = 0.12   # Watermark fade in effect (0.0 - 1.0)

# Get the video file name and watermark file name from the command line if not provided, use default
if len(sys.argv) == 2:
    video_file = sys.argv[1]
elif len(sys.argv) >= 3:
    video_file = sys.argv[1]
    watermark_file = sys.argv[2]

# Set file paths
video_file_path = os.path.join(input_folder, video_file_name)
watermark_file_path = os.path.join(input_folder, watermark_file_name)
output_video_file_path = os.path.join(output_folder, f'watermarked_{video_file_name}')

# Check if the video file exists
if not os.path.isfile(video_file_path):
    logging.error("Video file does not exist")
    exit()

# Check if the watermark file exists
if not os.path.isfile(watermark_file_path):
    logging.error("Watermark file does not exist")
    exit()

# Create the output folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Clear the output folder if it is not empty
for file in os.listdir(output_folder):
    file_path = os.path.join(output_folder, file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        logging.error(e)

# Read the video and watermark files
video = cv2.VideoCapture(os.path.join(input_folder, video_file_name))
watermark = cv2.imread(os.path.join(input_folder, watermark_file_name), cv2.IMREAD_UNCHANGED)

# Get the video width and height
video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Get video fps
video_fps = video.get(cv2.CAP_PROP_FPS)

# Display video info and watermark info in the log
logging.info(f'Video size: {video_height}x{video_width}')
logging.info(f'Video fps: {video_fps}')
logging.info(f'Video number of frames: {int(video.get(cv2.CAP_PROP_FRAME_COUNT))}')
logging.info(f'Watermark size: {watermark.shape[0]}x{watermark.shape[1]}')

# If watermark is greater than 1/4 of the video frame size we'll decrease watermark size by half recursively
watermark = resize_watermark(watermark, video_height, video_width)

# Ger resized watermark width and height
watermark_height = watermark.shape[0]
watermark_width = watermark.shape[1]

# Define the position to place the watermark (in this case, bottom right)
position = (video_width - watermark_width - 10, video_height - watermark_height - 10)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_file_path, fourcc, video_fps, (video_width, video_height))

# Start video processing
logging.info('Video processing started')
while True:
    # Read the next frame
    ret, frame = video.read()

    # Check if there is a next frame
    if not ret:
        # Display video processing complete
        logging.info('Video processing complete')
        break

    # Get the region of interest (ROI) in the frame for placing the watermark
    roi = frame[position[1]:position[1] + watermark_height, position[0]:position[0] + watermark_width]

    # Create a mask and inverse mask of the watermark
    watermark_mask = watermark[:, :, 1]
    watermark_mask_inv = cv2.bitwise_not(watermark_mask)

    # Extract the watermark region from the frame
    frame_roi = cv2.bitwise_and(roi, roi, mask=watermark_mask_inv)

    # Extract the watermark from the watermark image
    watermark_roi = cv2.bitwise_and(watermark[:, :, :3], watermark[:, :, :3], mask=watermark_mask)

    # Add the watermark to the frame
    # frame_roi = cv2.add(frame_roi, watermark_roi)
    frame_roi = cv2.addWeighted(frame_roi, 1, watermark_roi, watermark_beta, 0, frame_roi)

    # Place the frame with the watermark back into the original frame
    frame[position[1]:position[1] + watermark_height, position[0]:position[0] + watermark_width] = frame_roi

    # # Display the frame with the watermark
    cv2.imshow('Video with watermark', frame)

    # Write the frame with the watermark to the output video file
    out.write(frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video objects and destroy all windows
video.release()
out.release()
cv2.destroyAllWindows()