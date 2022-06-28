import cv2
import time
import numpy as np

#To save the output in a file output.avi
fourcc = cv2.VideoWriter_fourcc(*"XVID")
output_file = cv2.VideoWriter("output.avi",fourcc,20.0,(640,480))

#starting the webcam
cap = cv2.VideoCapture(0)

#Allowing the webcam to start by making the code sleep for 2 seconds
time.sleep(2)
bg = 0
#Capturing background for 60 frames
for i in range(60):
    ret,bg = cap.read()
#Flipping the background
bg = np.flip(bg,axis = 1)

#reading the captured frame until the camera is open
while(cap.isOpened()):
    ret,img = cap.read()
    if not ret:
        break
    #Flipping hte image for consistency
    img = np.flip(img,axis = 1)
    #Converting the color from BGR  to HSV
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #grenerating mask to detect red color
    lower_red = np.array([0,120,50])
    upper_red = np.array([10,255,255])
    mask_1 = cv2.inRange(hsv,lower_red,upper_red)
    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask_2 = cv2.inRange(hsv,lower_red,upper_red)
    mask_1 = mask_1+mask_2
    #open andd expand the image wher there is mask_1
    mask_1 = cv2.morphologyEx(mask_1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask_1 = cv2.morphologyEx(mask_1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))
    #Selecthing only the part that does not have mask_1 and saving in mask_2
    mask_2 = cv2.bitwise_not(mask_1)
    #Keeping only the part of the images without red color
    res_1 = cv2.bitwise_and(img,img,mask = mask_2)
    #Keeping only the part of the images with red color
    res_2 = cv2.bitwise_and(bg,bg,mask = mask_1)
    #Genrating the final output by merging res_1 and res_2
    final_output = cv2.addWeighted(res_1,1,res_2,1,0)
    output_file.write(final_output)
    #Displaying the output to the user
    cv2.imshow("Magic",final_output)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()    