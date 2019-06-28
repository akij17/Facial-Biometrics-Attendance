# Main script for the Facial Biometrics Attendance system
import tkinter
import register_face
import data_processor
import recognize_face
import fba_utility

HEIGHT = 200
WIDTH = 450

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.canvas = tkinter.Canvas(self.window, width = WIDTH, height = HEIGHT)
        self.canvas.pack()

        self.heading = tkinter.Label(self.canvas, text = "Select one of the options below:", font = 8)
        self.heading.place(anchor='nw', relx = 0.2)

        self.beginbutton = tkinter.Button(self.canvas, text = "Start Attendance Mode", bg = 'lightgray', command = self.attendance)
        self.beginbutton.place(anchor='nw', relx = 0.025, rely = 0.15, relwidth = 0.95)

        self.registerbutton = tkinter.Button(self.canvas, text = "Register Face", bg = 'lightgray', command = self.register)
        self.registerbutton.place(anchor='nw', relx = 0.025, rely = 0.4, relwidth = 0.95)
        
        self.processbutton = tkinter.Button(self.canvas, text = "Process Face Data", bg = 'lightgray', command = self.process)
        self.processbutton.place(anchor='nw', relx = 0.025, rely = 0.55, relwidth = 0.95)

        self.generatebutton = tkinter.Button(self.canvas, text = "Generate Excel File", bg = 'lightgray', command = self.generate_excel)
        self.generatebutton.place(anchor='nw', relx = 0.025, rely = 0.7, relwidth = 0.95)

        window.mainloop()

    def register(self):
        register_face.register(0)

    def process(self):
        data_processor.processdata()

    def attendance(self):
        recognize_face.begin()

    def generate_excel(self):
        fba_utility.generate_excel_file()

    def __del__(self):
        print("Shutting down")
        exit()

App(tkinter.Tk(), "Facial Biometrics Attendance")
