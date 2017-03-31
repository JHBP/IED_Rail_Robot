# import the necessary packages
from __future__ import print_function
import argparse
import time
import cv2
#import costom package
from iedgoprostream import IEDGUI
camera = 0#'http://10.5.5.9:8080/live/amba.m3u8'
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True, help="path to output directory to store snapshots")
args = vars(ap.parse_args())

# initialize the video stream
print("[INFO] preparing camera...")
cvv = cv2.VideoCapture(camera)#
cvv.set(6,40)#set fps to 40
time.sleep(2.0)
ied = IEDGUI(cvv,args["output"])
ied.root.mainloop()
print("safe exit")
