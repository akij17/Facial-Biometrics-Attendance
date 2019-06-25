import tkinter
from tkinter import messagebox
import cv2
import PIL
import os
from time import sleep
from PIL import Image
from PIL import ImageTk

SHOT_COUNT = 5
DIRNAME = os.getcwd()+"/rawImages/"

class FaceCam:
    def __init__(self, video_source = 0):
        # open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open the camera")

        # get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            r, img = self.vid.read()
            if r:
                return (r, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            else:
                return (r, None)
        else:
            return False, None

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
        self.cnt = 0
        self.name = ""

        # open video source
        self.vid = FaceCam(video_source)

        # label text
        self.heading = tkinter.Label(window, text = "Capture atleast {} pictures of your face.".format(SHOT_COUNT), font = 22)
        self.heading.pack()

        # id entry
        self.nameframe = tkinter.Frame(window)
        self.nameframe.pack()
        self.idlabel = tkinter.Label(self.nameframe, text = "ID/Name: ", font = 12)
        self.idlabel.grid(row = 0, column = 0)
        self.identry = tkinter.Entry(self.nameframe, font = 12)
        self.identry.grid(row = 0, column = 1)
        self.count = tkinter.Label(window, text = "Count = {}".format(self.cnt))
        self.count.pack()
        

        # create a canvas
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # button to capture the shot
        self.buttonframe = tkinter.Frame(window)
        self.buttonframe.pack()
        self.capture = tkinter.Button(self.buttonframe, text = "Capture", command = self.shot,
                                      bg = "lightgray", font = 12, padx = 50)
        self.capture.grid(row = 0, column = 0)
        self.reset = tkinter.Button(self.buttonframe, text = "Reset", command = self.reset,
                                    bg = "lightgray", font = 12, padx = 5)
        self.reset.grid(row = 0, column = 1)

        # call update after every delay
        self.delay = 5
        self.update()

        self.window.mainloop()

    def helper_create_directory(self, name):
        # first check for outer directory
        try:
            os.mkdir(DIRNAME)
        except FileExistsError:
            pass
        # check for inner directory
        try:
            os.mkdir(DIRNAME+"/"+name+"/")
        except FileExistsError:
            pass            

    def shot(self):
        if self.identry.get().strip() == "":
            print("Please Enter ID/Name")
            messagebox.showinfo("Error!", "Must enter ID/Name")
            return
        self.name = self.identry.get().strip().replace(' ', '.')
        directory = DIRNAME +"/"+ self.name + "/"
        self.helper_create_directory(self.name)
        r, img = self.vid.get_frame()
        if r:            
            print("Captured")
            self.identry.config(state = 'disabled')
            self.count.config(text = "Count = {}".format(self.cnt+1))
            saveDir = directory+self.name+"."+str(self.cnt)+".jpg"
            cv2.imwrite(saveDir, img)
            self.cnt += 1
        else:
            raise ValueError("Camera not working")
            return

    def reset(self):
        self.identry.config(state = 'normal')
        self.identry.delete(0, len(self.identry.get()))
        self.cnt = 0
        self.count.config(text = "Count = {}".format(0))

    def update(self):
        # retrieve frame from video source
        r, frame = self.vid.get_frame()
        if r:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.update)

# create tkinter window and pass it to the App
def register(video_source = 0):
    App(tkinter.Toplevel(), "Register Face", video_source)
