import cv2

# ############################ Helper Functions ############################
def resize_watermark(watermark, video_height, video_width):
    # If watermark is greater than 1/4 of the video frame size we'll decrease watermark size by half
    # Do this recursively until the watermark is less than 1/4 of the video frame size
    if watermark.shape[0] > video_height / 4 or watermark.shape[1] > video_width / 4:
        watermark = cv2.resize(watermark, (int(watermark.shape[1] / 2), int(watermark.shape[0] / 2)))
        watermark = resize_watermark(watermark, video_height, video_width)
    
    return watermark
# ############################ Helper Functions ############################