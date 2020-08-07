# BinaryMasksAndBoundingBoxes
Takes JSON file with annotations and .png files and generates binary masks and bounding boxes for use in Machine Learning.

open cv must be installed 

This can be accomplished with the following command: 

pip install opencv-python


Preconditions:
This python file, the .png files to annotate, and a json file. 

Post conditions:
-a folder containing the binary mask .png files
-a folder containing json files with coordinates for the bounding boxes
-a folder containing the bounded .png files 

Note: If there is any part of one polygon which overlaps the another polygon, the bounding box will contain both polygons. 

To compile

python Process.py <jsonfile> 
