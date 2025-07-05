import cv2
import mediapipe as mp
import time 


class HandDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxhands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mphand = mp.solutions.hands

        self.hands = self.mphand.Hands(
                static_image_mode=self.mode,
                max_num_hands=self.maxhands,
                min_detection_confidence=self.detectionCon,
                min_tracking_confidence=self.trackCon
                )


        self.mpDraw = mp.solutions.drawing_utils

    def findhands(self,img,draw=True):

        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

        #print(result.multi_hand_landmarks)

        if self.result.multi_hand_landmarks:
            for handLMS in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLMS,self.mphand.HAND_CONNECTIONS)
        return img
    
    def findPosition(self,img,handNo=0,draw=True):

                lmList = []

                if self.result.multi_hand_landmarks:
                    myhand = self.result.multi_hand_landmarks[handNo]
            
                    for id, lm in enumerate(myhand.landmark):
                        #print(id,lm)
                        h, w, c, = img.shape
                        cx,cy = int(lm.x*w),int(lm.y*h)
                        lmList.append([id,cx,cy])
                        # if draw:
                        #     cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)

                return lmList

    






def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 90)
    detector = HandDetector()
    

    while True:
        success,img = cap.read()
        img = cv2.flip(img,1)
        img = detector.findhands(img)
        lmList = detector.findPosition(img)
        if(len(lmList)!=0):
            print(lmList[4])
        

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3 )


        cv2.imshow("Video",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

     
    cap.release()
    cv2.destroyAllWindows()


if __name__== '__main__':
    main()