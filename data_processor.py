import cv2
import os
import math
import pickle
import pandas as pd
import numpy as np
import face_recognition as fr
from sklearn import neighbors
from sklearn.svm import SVC
from ast import literal_eval as le

SHOT_COUNT = 5
MODEL_PATH = os.getcwd()+"/faceData/faceData.csv"
DATA_FILE = os.getcwd()+"/faceData/faceData.pkl"
TRAIN_DIR = os.getcwd()+"/faceData/trained/trainedmodel.clf"
IMAGES = os.getcwd()+"/rawImages/"
CLASSIFIER = 'SVC'

def helper_create_directory():
    try:
        os.mkdir(os.getcwd()+"/faceData/")
    except FileExistsError:
        pass
    try:
        os.mkdir(os.getcwd()+"/faceData/trained/")
    except FileExistsError:
        pass

def create_dataset():
    # check if file already exists
    exists = os.path.exists(DATA_FILE) and os.path.isfile(DATA_FILE)
    oldentries = []
    if exists:
        print(); print("Datafile found.")
        O = pd.read_pickle(DATA_FILE)
        oldentries = set(np.array(O['id']))
        print("Already existing in database: ",oldentries); print()
        
    # loop through the images of every person and find out their encodings
    # also asign proper labels
    features = []
    labels = []
    for person in os.listdir(IMAGES):
        print("[INFO] Processing images for "+person.replace('.', ' '))
        if person in oldentries:
            print(person.replace('.',' ')+" already exists in data.")
            continue
        
        p_dir = IMAGES+"/"+person
        for img in os.listdir(p_dir):
            i_dir = p_dir+"/"+img
            image = fr.load_image_file(i_dir)
            face_bounds = fr.face_locations(image)

            if len(face_bounds) != 1:
                print("Image {} not suitable for training".format(i_dir))
                break

            face_encoding = fr.face_encodings(image, face_bounds)[0]
            features.append(face_encoding)
            labels.append(person)

    # create a pandas dataframe
    labels = labels
    features = features
    d = {'id':labels, 'enc':features}
    P = pd.DataFrame(d)

    # save CSV file
    if exists:
        P.to_csv(MODEL_PATH, mode = 'a', index = False, header = False, line_terminator = '')
        O = pd.read_pickle(DATA_FILE)
        O = O.append(P, ignore_index=True)
        #print(O)
        O.to_pickle(DATA_FILE)
    else:
        P.to_csv(MODEL_PATH, index = False, line_terminator = '')
        P.to_pickle(DATA_FILE)

def train_model(k = None):
    exists = os.path.exists(MODEL_PATH) and os.path.isfile(MODEL_PATH)
    if not exists:
        print("Dataset does not exist")
        exit()

    O = pd.read_pickle(DATA_FILE)
    if k == None:
        k = int(round(math.sqrt(len(O['enc']))))
    
    # create and train classifier
    if CLASSIFIER == 'KNN':
        print("[INFO] Training model: KNN")
        knn = neighbors.KNeighborsClassifier(n_neighbors = k, algorithm = 'ball_tree', weights = 'distance')
        knn.fit(list(O['enc']), O['id'])
    else:
        print("[INFO] Training model: SVC")
        clf = SVC(C=1.0, gamma='scale', kernel='linear', probability = True)
        clf.fit(list(O['enc']), O['id'])
    # saved the trained model
    try:
        with open(TRAIN_DIR, 'wb') as f:
            pickle.dump(clf, f)
        print("Training Successful")
    except:
        print("Some error occured!")

def processdata():
    helper_create_directory()
    create_dataset()
    train_model()
