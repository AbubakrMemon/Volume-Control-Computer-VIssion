import cv2
import numpy as np
import time
import handtrackingmodule as htm
import math
import pycaw

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL








wCam , hCam = 640 , 480

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0

detector = htm.HandDetector(detectionCon=0.8)



device = AudioUtilities.GetSpeakers()
interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#print(f"Audio output: {device.FriendlyName}")
#print(f"- Muted: {bool(volume.GetMute())}")
#print(f"- Volume level: {volume.GetMasterVolumeLevel()} dB")
print(f"- Volume range: {volume.GetVolumeRange()[0]} dB - {volume.GetVolumeRange()[1]} dB")
volRange = volume.GetVolumeRange()
minVal = volRange[0]
maxVal = volRange[1]
vol = 0
volB = 300
volP = 100









while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    
    img = detector.findhands(img)
    lmList = detector.findPosition(img)
    #print(lmList)

    if(len(lmList)!=0):
        #print(lmList[4],lmList[8])

        x1,y1 = lmList[4][1], lmList[4][2]
        x2,y2 = lmList[8][1], lmList[8][2]
        cx,cy = (x1+x2)//2 , (y1+y2)//2

        cv2.circle(img,(x1,y1), 6 , (255 ,0, 255),cv2.FILLED)
        cv2.circle(img,(x2,y2), 6 , (255 ,0, 255),cv2.FILLED)
        cv2.line(img , (x1,y1),(x2,y2), (255,0,255), 2)
        cv2.circle(img,(cx,cy), 6 , (255 ,0, 255),cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        #print(length)

        vol = np.interp(length,[20,150],[minVal,maxVal])
        volB = np.interp(length,[20,150],[300,200])
        volP = np.interp(length,[20,150],[0,100])
        volume.SetMasterVolumeLevel(vol, None)
        print(length,vol)



        

        if(length<20):
            cv2.circle(img,(cx,cy), 6 , (0 ,255, 0),cv2.FILLED)


    cv2.rectangle(img,(50,200),(30,300),(0,255,0),3)
    cv2.rectangle(img,(50,int(volB)),(30,300),(0,255,0),cv2.FILLED)
    cv2.putText(img,f'{int(volP)}%',(10,350),cv2.FONT_HERSHEY_PLAIN,3,(200,0,200),2)




    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3 )
    
    cv2.imshow('img',img)


    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

