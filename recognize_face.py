import cv2
import tkinter
import os
import math
import statistics as stats
import pickle
import pandas as pd
import numpy as np
import datetime as dt
import face_recognition as fr
from sklearn import neighbors
from PIL import Image
from PIL import ImageTk

TRAIN_DIR = os.getcwd()+"/faceData/trained/trainedmodel.clf"
HAARCASSCADE = os.getcwd()+"/"+"haarcascade_frontalface.xml"
DATA_FILE = os.getcwd()+"/faceData/datafile.pkl"
CAMERA_LATENCY = 10
ACCURACY = 10
WIDTH = 0 
HEIGHT = 0

class FaceCam:
    def __init__(self, video_source = 0):
        self.vid = cv2.VideoCapture(0)
        if not self.vid.isOpened():
            raise ValueError("Unable to open the camera")
        
        self.fd = cv2.CascadeClassifier(HAARCASSCADE)

        # get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        WIDTH = self.width
        HEIGHT = self.height
        
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
                    return (r, cv2.cvtColor(img, cv2.COLOR_BGR2RGB), o_img, True, (x, y))
                except IndexError:
                    pass
                except:
                    pass
                return (r, cv2.cvtColor(img, cv2.COLOR_BGR2RGB), o_img, False, (None, None))
            else:
                return (r, None, None, False, (None, None))
        else:
            return (False, None, None, False, (None, None))
        
    def __del__(self):
        if self.vid.isOpened():
            cv2.destroyAllWindows()
            self.vid.release()
            exit()
        
class App:
    def __init__(self, window, window_title, video_source = 0):
        self.window = window
        self.window.title(window_title)
        self.dataexists = self.helper_data_exists()
        self.tick = cv2.imread('green_tick.png')

        self.vid = FaceCam(video_source)
        self.name_data = []

        self.heading = tkinter.Label(self.window, text = "Green check represents attendance marked.", font = 22)
        self.heading.pack()

        self.canvas = tkinter.Canvas(self.window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        self.process = True

        self.delay = CAMERA_LATENCY
        self.update()

        self.window.mainloop()
        
    def helper_data_exists(self):
        if os.path.exists(DATA_FILE) and os.path.isfile(DATA_FILE):
            return True
        return False
    
    def load_model(self):
        # load the model
        clf = None
        try:
            pickle_in = open(TRAIN_DIR, 'rb')
            clf = pickle.load(pickle_in)
            return clf
        except:
            raise ValueError("Trained data not found!")
            exit()
                
    def run_recognize(self, model, img):
        if self.process:
            self.process = not self.process
            face_bounds = fr.face_locations(img)        
            if not len(face_bounds) == 1:
                return
            try:
                face_encoding = fr.face_encodings(img, face_bounds)[0]
                res = model.predict([face_encoding])
                return res
            except:
                pass
        else:
            self.process = not self.process
    

    def update(self):
        r, frame, o_img, clickable, (fx, fy) = self.vid.get_frame()
        if r:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            x_off = fx
            y_off = fy
            if clickable:
                ## Todo
                P = None
                todays_date = dt.datetime.now().date()
                if not self.dataexists:
                    index = pd.date_range(todays_date, periods=30, freq='D')
                    P = pd.DataFrame(index=index)
                else:
                    P = pd.read_pickle(DATA_FILE)
                model = self.load_model()
                name = self.run_recognize(model, o_img)
                if not name is None:
                    self.name_data.append(name[0])
                if len(self.name_data) > ACCURACY:
                    name = stats.mode(self.name_data)
                    name = name.replace('.', ' ')
                    print("[INFO] Marking attendance for {} on data {}".format(name, todays_date))
                    self.name_data = []
                    if not name in P.columns:
                        P[name] = 'A'
                    if P[name][todays_date] is 'A':
                        P[name][todays_date] = str(dt.datetime.now().time()).split('.')[0]
                        P.to_pickle(DATA_FILE)
                        try:
                            frame[x_off:x_off+len(self.tick), x_off:x_off+len(self.tick)] = self.tick
                        except:
                            pass
                    else:
                        try:
                            frame[y_off:y_off+len(self.tick), x_off:x_off+len(self.tick)] = self.tick
                        except:
                            pass
                    self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
                    self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
                    
        self.window.after(self.delay, self.update)


def begin():        
    App(tkinter.Toplevel(), "Attendance")
