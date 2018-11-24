import cv2
import numpy as np
from collections import Counter
import csv


print("Data will be added to the data.csv file after each image is run.")
print("")
imgName = input("enter image name followed by extension type:")

image = cv2.imread(imgName)
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
th2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,3,-2)

(th, contours, hierarchy) = cv2.findContours(th2,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
length_contours = len(contours)


delContours = []
for i in range(0,length_contours,2):
    delContours.append(i)

for i in sorted(delContours,reverse = True):
    del contours[i]


shapes = [] #for storing shapes
color = [] #for storing colors
colored_shapes = [] #for appending elements of shapes,size and color as one element in it.
size = [] #for storing sizes



numContours = int(len(contours))
font = cv2.FONT_HERSHEY_SIMPLEX




for i in range(0,numContours):#loop for finding shape and size of the shapes.
    cnt = contours[i]

    area = cv2.contourArea(cnt)

    M = cv2.moments(cnt)
    Cx = int(M["m10"]/M["m00"])
    Cy = int(M["m01"]/M["m00"])

    epsilon = 0.04*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)
    topmost = list(cnt[cnt[:,:,1].argmin()][0]) # to find topmost vertices  of a contour.
    
    if len(approx) >= 8: #for a circle.
        cv2.putText(image,"CIRCLE",(topmost[0]+30,topmost[1]-10),font,0.35,(0,0,0),1)
        shapes.append("CIRCLE")
        
        if area >= 8625.0:
            size.append("LARGE")
        elif area <= 2356.5:
            size.append("SMALL")

        else:
            size.append("MEDIUM")
        

    elif len(approx) == 4:#for a square or a rectangle
        (x,y,w,h) = cv2.boundingRect(approx)
            
        if (float(w/h) == 1):
            cv2.putText(image,"SQUARE",(topmost[0]+30,topmost[1]+10),font,0.35,(0,0,0),1)
            shapes.append("SQUARE")

            if area >= 11023:
                size.append("LARGE")
            elif area <= 3023:
                size.append("SMALL")
            else:
                size.append("MEDIUM")
            
        else:
            cv2.putText(image,"RECTANGLE",(topmost[0]+40,topmost[1]-10),font,0.35,(0,0,0),1)
            shapes.append("RECTANGLE")

            if area >= 21523.0:
                size.append("LARGE")
            elif area <= 4123.0:
                size.append("SMALL")
            else:
                size.append("MEDIUM")
            
                
                

    elif len(approx) == 3 or len(approx)/2 == 3: #for a triangle
        cv2.putText(image,"TRIANGLE",(topmost[0]+20,topmost[1]),font,0.35,(0,0,0),1)
        shapes.append("TRIANGLE")

        if area >= 5871.5:
            size.append("LARGE")
        elif area <= 1692.0:
            size.append("SMALL")

        else:
            size.append("MEDIUM")
            
    cv2.drawContours(image,cnt,-1,(0,0,0),1) # for drawing contours along the shape


for j in range(0,numContours): #loop for finding out the colour for each shape
    cnt = contours[j]

    M = cv2.moments(cnt)
    Cx = int(M["m10"]/M["m00"])
    Cy = int(M["m01"]/M["m00"])

    epsilon = 0.04*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)
    topmost = list(cnt[cnt[:,:,1].argmin()][0]) #to find topmost vertice of each contour
    pixel = image[topmost[1]+2,topmost[0]]

    if(pixel[0]==255 and pixel[1]==0 and pixel[2]==0):
        cv2.putText(image,"BLUE",(topmost[0],topmost[1]-10),font,0.35,(0,0,0),1)
        color.append("BLUE")

    elif(pixel[0]==0 and pixel[1]==255 and pixel[2]==0):
        cv2.putText(image,"GREEN",(topmost[0],topmost[1]-10),font,0.35,(0,0,0),1)
        color.append("GREEN")

    
    elif(pixel[0]==0 and pixel[1]==0 and pixel[2]==255):
        cv2.putText(image,"RED",(topmost[0],topmost[1]-10),font,0.35,(0,0,0),1)
        color.append("RED")

    elif(pixel[0]==0 and pixel[1]==255 and pixel[2]==255):
        cv2.putText(image,"YELLOW",(topmost[0],topmost[1]-10),font,0.35,(0,0,0),1)
        color.append("YELLOW")


    else:
        cv2.putText(image,"ORANGE",(topmost[0],topmost[1]-10),font,0.35,(0,0,0),1)
        color.append("ORANGE")

l = len(shapes)
if l > 0:# to check if the image contains any object if it doesn't the script doesn't return anything
    
    for i in range(0,l): #appending all the elements of color,size and shape
        string  =color[i]+ "-"+ shapes[i]+"-" +size[i]+"-"
        colored_shapes.append(string)

    new_list = [] #list for storing the string along with count
    output_list = [] #list of lists for storing the output
    temp = [] #temporary list for storing the values temporarily


    c = Counter(colored_shapes) #keeps track of how many times the similar value was added in the list
    for key,value in c.items():
        valueStr = str(value)
        new_list.append(key + valueStr)


    for each in new_list: #making a list of lists
        temp.append(each)
        output_list.append(temp)
        temp = []

    output_list.insert(0,imgName)
    new_list.insert(0,imgName)


    #writing the lists
    with  open("data.csv","a") as file:
        writer = csv.writer(file,delimiter = ',',lineterminator = '\n')
        writer.writerow(new_list)
    file.close()


    if imgName == "test1.png":
        cv2.imwrite("output1.png",image)

    if imgName == "test2.png":
        cv2.imwrite("output2.png",image)

    if imgName == "test3.png":
        cv2.imwrite("output3.png",image)

    if imgName == "test4.png":
        cv2.imwrite("output4.png",image)

        
            
    cv2.imshow("image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



    
