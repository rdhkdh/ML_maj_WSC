import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# volume.GetMute() ==> 'true' if comp id muted 
# volume.GetVolumeRange() ==> range is (-65.25,0.0,0.03125)
# volume.GetMasterVolumeLevel() ==> gives current value of volume in terms of the above range -65.25 to 0.0
# volume.SetMasterVolumeLevel(-20.0, None) ==> sets to desired volume

mp_drawing = mp.solutions.drawing_utils
#mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

vid = cv2.VideoCapture(0) # opens camera

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

 while vid.isOpened():
    success, img = vid.read() #to keep refreshing the image captured by camera
    if not success:
        print("Ignoring empty camera frame.")
        continue

    imgRGB= cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #cv2 uses BGR but mediapipe uses RGB, so we have to convert
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks) = 'None' when no hand on the screen. Else gives the coordinates of the hand.

    if results.multi_hand_landmarks: # if hand is found
        for hand_no in results.multi_hand_landmarks: # iterate over all hands found in frame
            mp_drawing.draw_landmarks(img, hand_no, mp_hands.HAND_CONNECTIONS)
            lmkList = [] #list of landmarks
            for id, lm in enumerate(hand_no.landmark): 
                #print(id, lm) # prints coord of each of the 21 landmarks on the hand
                h,w,c= img.shape # height,width,channel of image
                px,py = int(lm.x*w) , int(lm.y*h) # converting coord to pixels
                #print(id,px,py)
                lmkList.append([id,px,py])
            #print(lmkList)

            if lmkList: # obtaining x and y coordinates of landmark 4 and 8
                x1,y1= lmkList[4][1], lmkList[4][2] # thumb
                x2,y2= lmkList[8][1], lmkList[8][2] # index finger
            cv2.circle(img, (x1,y1), 10, (0,255,0),2) #  image, center coord, radius, color(BGR), thickness
            cv2.circle(img, (x2,y2), 10, (0,255,0),2) 
            cv2.line(img, (x1,y1), (x2,y2), (255,0,0),2) # a blue line btw them
            length = math.hypot(x2-x1,y2-y1)
            #print(length)
            vol_range = volume.GetVolumeRange() #returns tuple
            min_vol = vol_range[0] # doing this because we don't want to hardcode it
            max_vol= vol_range[1]
            # converting length to a value in volume range
            vol = np.interp(length, [0,300],[min_vol,max_vol]) # interpolation- length, range of length, range to be converted to.
            volume_bar = np.interp(length, [0,300], [400,150] ) #interpolation to coord of rectangle
            volume_percentage= np.interp(length, [0,300], [0,100])
            volume.SetMasterVolumeLevel(vol, None)
            # displaying volume bar and volume percentage
            cv2.rectangle(img, (50,150), (85,400), (0,255,0), 2)
            cv2.rectangle(img, (50,int(volume_bar)), (85,400), (0,255,0), cv2.FILLED)
            cv2.putText(img, str(int(volume_percentage)), (40,450), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,255), 3)

    cv2.imshow("Image", img) # show video
    k = cv2.waitKey(1) # delay of 1ms to be able to actually see the video
    if k==27: # ASCII value for ESC key. Press ESC key to exit program.
        break   
vid.release() # releasing memory occupied
