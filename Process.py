#!/usr/bin/env python
# coding: utf-8


import cv2
import numpy as np
import json
import matplotlib.pyplot as plt
import os
import sys

try:
    jsonFile = sys.argv[1]
except:
    print("\nError: Specify name of JSON File containing annotations.\n")
    exit(0)
currentWorkingDirectory = os.getcwd()

#Generate Binary Masks from Coordinates
#for file in os.listdir('/Users/lbassett/Documents/Projects/geoint/planes2/'):
if not os.path.exists(os.path.join(currentWorkingDirectory, 'binaryMasks/')):
   os.mkdir(os.path.join(currentWorkingDirectory, 'binaryMasks/'))  
    
if not os.path.exists(os.path.join(currentWorkingDirectory,'boundingBoxCroppedImages/')):
    os.mkdir(os.path.join(currentWorkingDirectory,'boundingBoxCroppedImages/'))
    
if not os.path.exists(os.path.join(currentWorkingDirectory,'boundingBoxJSON/')):
    os.mkdir(os.path.join(currentWorkingDirectory,'boundingBoxJSON/'))
    
binaryMaskDir = os.path.join(currentWorkingDirectory, 'binaryMasks/')
boundingBoxImageDir = os.path.join(currentWorkingDirectory,'boundingBoxCroppedImages/')
boundingBoxJsonDir = os.path.join(currentWorkingDirectory,'boundingBoxJSON/')

with open(jsonFile) as file:
    annotations = json.load(file)
    
    for key in annotations:
        #im = np.zeros(img,dtype=np.uint8)
        regions = annotations[key]['regions']
        #print(annotations[key]['filename'],"\n")
        img = np.shape(cv2.imread(os.path.join(currentWorkingDirectory, annotations[key]['filename'])))
        im = np.zeros(img,dtype=np.uint8)
        for regions in regions: 
            x_Cords = np.array(annotations[key]['regions'][regions]["shape_attributes"]["all_points_x"])
            y_Cords = np.array(annotations[key]['regions'][regions]["shape_attributes"]["all_points_y"])
            # Coords = np.meshgrid(x_Cords, y_Cords)
            #print((img),"\n\n\n")
            #newArray = zip(x_Cords,y_Cords)
            pts = np.stack((x_Cords, y_Cords), axis=-1)
                #print(newArray)
            pts = np.int32(pts)
            #im = np.zeros(img,dtype=np.uint8)
            #print(pts) 
            #color = c.to_rgba('black')
            #print("X: ", x_Cords, "\n\nY:  ", y_Cords,"\n" )
            cv2.fillPoly(im, [pts], (255,255,255))
        plt.imshow(im)
        fileN = annotations[key]['filename']

        cv2.imwrite(os.path.join(binaryMaskDir,fileN) ,im)       

with open(jsonFile) as file:
    annotations = json.load(file)
    
    for key in annotations:
        regions = annotations[key]['regions']
        for region in regions:
            #print(annotations[key]['filename'],"\n")
            image = cv2.imread(binaryMaskDir + annotations[key]['filename'])
            original = image.copy()
            gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            # Find contours, obtain bounding box, extract and save ROI
            ROI_number = 0
            cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            
            file = annotations[key]['filename']
            
            with open(boundingBoxJsonDir + annotations[key]['filename']+"_BoundingBoxes.json", "w") as jsonfile:
                json.dump(file,jsonfile)
         
            Bounding = []
            for c in cnts:
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
                ROI = original[y:y+h, x:x+w]
                cv2.imwrite(boundingBoxImageDir + annotations[key]['filename']+ "_ROI_{}.png".format(ROI_number), ROI)
                Box = [x,y,x+w,y+h]
                Bounding.append(Box)
                ROI_number += 1
            filetype = {
                "object_type":"plane",
                "bounding_boxes": Bounding
            }
            with open(boundingBoxJsonDir + annotations[key]['filename']+"_BoundingBoxes.json", "a") as jsonfile:
                json.dump(filetype, jsonfile)
                
            
            
            #cv2.imshow('image', image)
            #new json file
            #name of picture
            #every image generated by the c in cnts loop
           


