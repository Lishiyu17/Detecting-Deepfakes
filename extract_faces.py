"""
Generate frames from videos obtained from a directory.
Extract faces from those frames
"""
# Program To Read video
# and Extract Frames
# from imutils.video import VideoStream
# import argparse
# import imutils
# import time
import numpy as np
import cv2


# Function to extract frames
def frame_capture(path):
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe('deploy.prototxt.txt', 'res10_300x300_ssd_iter_140000.caffemodel')
    # Path to video file
    vidObj = cv2.VideoCapture(path)

    # Used as counter variable
    count = 0

    # checks whether frames were extracted
    success = 1

    while success:
        # vidObj object calls read
        # function extract frames
        success, image = vidObj.read()
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                                     (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()
        for i in range(0, detections.shape[2]):

            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence < 0.7:  # HYPER_PARAMETER
                continue

            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            frame = image[startY:endY, startX:endX]
            # Saves the frames  with frame-count
            cv2.imwrite("Face_images\\image%d.jpg" % count, frame)

            count += 1


# Driver Code
if __name__ == '__main__':
    # Calling the function
    frame_capture("a.mp4")