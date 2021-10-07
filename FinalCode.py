#Import the required Packages
import cv2
import numpy as np
import argparse
import pytesseract as tess
import string
import re

#Create Argument Parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type = str,
default = "Bill1.png", help="path to input image")
ap.add_argument("-o1", "--template", type = str,
default = "Template.jpg",help="path to template image")
args = vars(ap.parse_args())

#Read template and input image
image = cv2.imread(args["image"])
template = cv2.imread(args["template"])

#Convert Images to Grayscale
imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# perform template matching
result = cv2.matchTemplate(imageGray, templateGray,cv2.TM_CCOEFF_NORMED)
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

# determine the starting and ending (x, y)-coordinates of the
# bounding box
(startX, startY) = maxLoc
endX = startX + template.shape[1]
endY = startY + template.shape[0]

#Crop the image 
cropped = image[startY:endY, startX:endX]
cv2.imwrite("Cropped.png",cropped)

img = cropped

# resize the image
scale_percent = 200 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
 
# Convert to grayscale    
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Morphological processing
kernel = np.ones((1, 1), np.uint8)
img = cv2.dilate(img, kernel, iterations=1)
img = cv2.erode(img, kernel, iterations=1)

#Apply Pytesseract 
text = tess.image_to_string(img)

#Clean the text and separate out Due Date and amount payable

#Due Date
for line in range(len(text.splitlines())):
    if "Due Date" in text.splitlines()[line] :
        print("Due Date:"+ text.splitlines()[line].replace('Due Date','')) #Print Due Date

#Amount payable
for line in range(len(text.splitlines())):
	if  "Amount Payable" in text.splitlines()[line]:
		amount=line
	if  "Summary" in text.splitlines()[line]:
		summary=line

# Remove Spaces and other Punctuations from string
words = str(text.splitlines()[amount:])
my_punctuation = string.punctuation.replace(".", "")
table = str.maketrans('', '', my_punctuation)
stripped = [w.translate(table) for w in words]
string = ''.join(stripped)


#Remove all other words from string
for line in range(len(re.findall('\d*\.?\d+',string))):
	amount = float(re.findall('\d*\.?\d+',string)[line])

#Print Amount 
print("Amount Payable: "+ str(amount))


