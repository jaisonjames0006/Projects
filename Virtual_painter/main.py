import cv2
import numpy as np
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
# cap.set(3,1280)
# cap.set(4,720)


detector = htm.handDetector(detectionCon=0.8)

drawingColor = (0,0,0)

imgcanvas = np.zeros((930,1800,3),np.uint8)

eraserSize = 50
brushSize = 20

while True:

    # step 1 Preprocesssing
    sucess,image = cap.read()
    image = cv2.resize(image,(1800, 930)) #resize
    image = cv2.flip(image,1)  #mirror image


    cv2.rectangle(image,(5,5),(135,918),(238,232,170),cv2.FILLED)
    cv2.circle(image,(70,75),60,(148,0,211),cv2.FILLED)
    cv2.circle(image,(70,205),60,(75,0,130),cv2.FILLED)
    cv2.circle(image,(70,335),60,(255,0,0),cv2.FILLED)
    cv2.circle(image,(70,465),60,(0,255,0),cv2.FILLED)
    cv2.circle(image,(70,595),60,(0,255,255),cv2.FILLED)
    cv2.circle(image,(70,725),60,(255,127,0),cv2.FILLED)
    cv2.circle(image,(70,855),60,(0,0,255),cv2.FILLED)
    cv2.circle(image,(1720,70),65,(255,255,255),cv2.FILLED)
    cv2.putText(image,'ERASER',(1665,80),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),2)
    cv2.putText(image,'V',(60,85),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,0,0),2)
    cv2.putText(image,'I',(60,215),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,0,0),2)
    cv2.putText(image,'B',(60,345),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,0,0),2)
    cv2.putText(image,'G',(60,475),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,0,0),2)
    cv2.putText(image,'Y',(60,605),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,0,0),2)
    cv2.putText(image,'O',(60,735),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,0,0),2)
    cv2.putText(image,'R',(60,865),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),2)
    cv2.rectangle(image,(5,5),(135,918),(0,0,255),2)


    # step 2 find the hand landmarks
    image = detector.findHands(image)
    lmlist = detector.findPosition(image) # find the position of 21 points in the hand

    if len(lmlist) != 0:
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]
        # print(x1,y1) #index finger
        # print(x2,y2) #middle finger position
        

    # step 3 check which finger is up

    fingers = detector.fingersUp()
    # print(fingers)
    
    # step 4 selection mode - two finger is up

    if fingers[1] and fingers[2]:
        
        # print('Selection mode..')
        xp,yp = 0,0

        if x1<80:

            if 15<y1<135:
                # print(x1,y1)
                # print('v selected')
                drawingColor = (148,0,211)

            elif 145<y1<265:
                # print(x1,y1)
                # print('i selected')
                drawingColor = (75,0,130)

            elif 275<y1<395:
                # print(x1,y1)
                # print('b selected')
                drawingColor = (255,0,0)


            elif 405<y1<525:
                # print(x1,y1)
                # print('g selected')
                drawingColor = (0,255,0)


            elif 535<y1<655:
                # print(x1,y1)
                # print('y selected')
                drawingColor = (0,255,255)

            elif 665<y1<785:
                # print(x1,y1)
                # print('o selected')
                drawingColor = (255,127,0)

            elif 795<y1<915:
                # print(x1,y1)
                # print('r selected')
                drawingColor = (0,0,255)


        if 1530<x1<1810 and 10<y1<140:

            # print('Eraser selected')
            drawingColor = (0,0,0)


        cv2.rectangle(image,(x1,y1),(x2,y2),drawingColor,cv2.FILLED)
    

    # step 5 drawing mode - one finger is up

    if fingers[1] and not fingers[2]:

        cv2.circle(image,(x1,y1),15,drawingColor,thickness=-1)

        # print('Drawing Mode')

        if xp == 0 and yp == 0:
            xp = x1
            yp = y1

        if drawingColor ==( 0,0,0):
            cv2.line(image,(xp,yp),(x1,y1),drawingColor,eraserSize)
            cv2.line(imgcanvas,(xp,yp),(x1,y1),drawingColor,eraserSize)

        else:
            cv2.line(image,(xp,yp),(x1,y1),drawingColor,brushSize)
            cv2.line(imgcanvas,(xp,yp),(x1,y1),drawingColor,brushSize)


        xp , yp = x1 , y1

    imgGray = cv2.cvtColor (imgcanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv = cv2.threshold(imgGray,20,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)

    image = cv2.bitwise_and(image,imgInv)
    image  = cv2.bitwise_or(image,imgcanvas)


    image = cv2.addWeighted(image,1,imgcanvas,0.5,0)


    cv2.imshow('VIRTUAL WRITTING BOARD',image)
    if cv2.waitKey(1) & 0xFF ==27:
        break

