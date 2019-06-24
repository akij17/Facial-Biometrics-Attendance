# This script will register the faces along with their names
import cv2
import os

SHOT_COUNT = 5

def captureFaceData(name):
    cam = cv2.VideoCapture(0)
    count = 0
    dirName = os.getcwd()+"/faceData/rawImages/"+name
    try:
        os.mkdir(dirName)
    except FileExistsError:
        pass
    while count < SHOT_COUNT:
        r, img = cam.read()
        if r == True:
            cv2.imshow('Press S to save. Press N to take next shot.', img)
            k = cv2.waitKey(0)
            print("Take next shot. Press N key")
            if k == ord('n'):
                cv2.destroyAllWindows()
            elif k == ord('s'):
                cv2.imwrite(dirName+"/"+name+"."+str(count)+".jpg", img)
                count = count + 1
        
print("Begin: Registration Process")
name = input("Please enter your name: ")
print("Instructions: We will now register your face for the biometrics.")
print("A camera window will flash on the screen. Make sure the face is clearly visible.")
print("Take the desired number of shots from different angles (greater than 45 degrees).")
print("Press S to save that shot. Press N to take another shot.")
print("Current shot count is ", SHOT_COUNT)
input("Once ready press Enter...")
captureFaceData(name.strip().replace(' ','.'))
print("Done")
