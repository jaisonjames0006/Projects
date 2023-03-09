import cv2
from pynput.keyboard import Controller
from module import findpostion
import math
from time import sleep

cap = cv2.VideoCapture(0)

keyboard=Controller()

keys=[["1","2","3","4","5","6","7","8","9","0"],
      ["Q","W","E","R","T","Y","U","I","O","P"],
      ["A","S","D","F","G","H","J","K","L",";"],
      ["Z","X","C","V","B","N","M",",",".","/"]]

Textbox=""
Textbox1=""

def draw(img,keylist):
    for key in keylist:
        x,y=key.pos
        w,h=key.size
        cv2.rectangle(img,(key.pos),(x+w,y+h),(50,180,220),cv2.FILLED)
        cv2.putText(img,key.text,(x+10,y+40),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)
    return img

class key():
    def __init__(self,pos,text,size=[60,60]):
        self.pos=pos
        self.text=text
        self.size=size
      
keylist=[]
for i in range(4):
    for j,k in enumerate(keys[i]):
        keylist.append(key([80*j+30,80*i+100],k))   

while True:

     sucess, image = cap.read()
     image = cv2.flip(image,1)
     image = cv2.resize(image, (1740, 920))

     cv2.rectangle(image,(10,10),(1725,450),(76,225,209),3)  
     cv2.rectangle(image,(530,80),(1045,20),(153,153,255),cv2.FILLED)  
    
     
     lmlist=findpostion(image)
     image = draw(image,keylist)
     if len(lmlist)!=0:
        for key in keylist:
            
            x,y=key.pos
            w,h=key.size
            x1,y1=lmlist[8][1],lmlist[8][2]
            x2,y2=lmlist[4][1],lmlist[4][2]
            length = math.hypot(x2-x1,y2-y1)

            if x<x1<x+w and y<y1<y+h:
               
               cv2.rectangle(image,(key.pos),(x+w,y+h),(235,0,0),cv2.FILLED)
               cv2.putText(image,key.text,(x+10,y+40),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)

               if length < 30:
               
                  cv2.rectangle(image,(key.pos),(x+w,y+h),(0,255,0),cv2.FILLED)
                  cv2.putText(image,key.text,(x+10,y+40),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)

                  if len(Textbox)>26:
                      Textbox1 +=key.text
                      keyboard.press(key.text)
                      keyboard.release(key.text)
                  else:
                      Textbox +=key.text
                      keyboard.press(key.text)
                      keyboard.release(key.text)
    
        
     cv2.rectangle(image,(850,100),(1700,400),(180,180,180),cv2.FILLED)
     cv2.putText(image,'Onscreen Keyboard',(550,60),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(255,255,255),3)
     cv2.putText(image,Textbox,(880,150),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)
     cv2.putText(image,Textbox1,(880,200),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)
     sleep(0.05)
     

     cv2.imshow("Onscreen Keyboard", image);
     if cv2.waitKey(1) & 0xFF==27:
         break
     
cap.release()
cv2.destroyAllWindows()