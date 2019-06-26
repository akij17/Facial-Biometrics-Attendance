import cv2
import tkinter
import os
import math
import pandas as pd
import numpy as np
import face_recognition as fr
from sklearn import neighbors
from PIL import Image
from PIL import ImageTk

TRAIN_DIR = os.getcwd()+"/faceData/trained/trainedmodel.clf"
HAARCASSCADE = os.getcwd()+"/"+"haarcascade_frontalface.xml"
CAMERA_LATENCY = 5

class FaceCam:
    def __init__(self, video_source = 0):
        self.vid = cv2.VideoCapture(0)
        if not self.vid.isOpened():
            raise ValueError("Unable to open the camera")
        
        self.fd = cv2.CascadeClassifier(HAARCASSCADE)

        # get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
    def get_frame(self):
        if self.vid.isOpened():
            r, img = self.vid.read()
            if r:
                g_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                o_img = img.copy()
                f = self.fd.detectMultiScale(g_img)
                try:
                    (x, y, w, h) = f[0]
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)
                    return (r, cv2.cvtColor(img, cv2.COLOR_BGR2RGB), o_img, True)
                except IndexError:
                    pass
                except:
                    pass
                return (r, cv2.cvtColor(img, cv2.COLOR_BGR2RGB), o_img, False)
            else:
                return (r, None, None, False)
        else:
            return (False, None, None, False)
        
    def __del__(self):
        if self.vid.isOpened():
            cv2.destroyAllWindows()
            self.vid.release()
            exit()
        self.window.mainloop()

class App:
    def __init__(self, window, window_title, video_source = 0):
        self.window = window
        self.window.title(window_title)

        self.vid = FaceCam(video_source)

        self.heading = tkinter.Label(self.window, text = "Green check represents attendance marked.", font = 22)
        self.heading.pack()

        self.canvas = tkinter.Canvas(self.window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        self.delay = CAMERA_LATENCY
        self.update()

        self.window.mainloop()

    def update(self):
        r, frame, o_img, clickable = self.vid.get_frame()
        if r:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            if clickable:
                ## Todo

        self.window.after(self.delay, self.update)
        
App(tkinter.Tk(), "Attendance")
