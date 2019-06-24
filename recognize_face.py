import cv2
import os
import math
import pandas as pd
import numpy as np
from sklearn import neighbors

TRAIN_DIR = os.getcwd()+"/faceData/trained/trainedmodel.clf"

print("=> Menu: ")
print("1. Mark Attendance")
