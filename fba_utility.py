import pandas as pd
import os

DATA_FILE = os.getcwd()+"/faceData/datafile.pkl"
ATTENDANCE_DIR = os.getcwd()+"/attendance/"

def generate_excel_file():
    if not os.path.exists(DATA_FILE) and os.path.isfile(DATA_FILE):
        raise ValueError("Data File not found")
        return
    P = pd.read_pickle(DATA_FILE)
    try:
        os.mkdir(ATTENDANCE_DIR)
    except FileExistsError:
        pass
    ind = str(P.index[0]).split(' ')[0]
    P.to_csv(ATTENDANCE_DIR+str(ind)+".csv")
