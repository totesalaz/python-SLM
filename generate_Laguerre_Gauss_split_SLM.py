# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 16:07:20 2016

Filename: generate_Laguerre_Gauss_split_SLM.py

Author:Luis José Salazar-Serrano        
        totesalaz@gmail.com / luis-jose.salazar@icfo.es
        http://opensourcelab.salazarserrano.com
        
Description: 

Program that splits the SLM into two equal regions and in each region generates
a phase mask of a Laguerre Gauss beam with a CHARGE provided by the user. 

The whole image is sent to the second monitor output where the SLM is
connected. The mask generated is also shown in the main monitor in a small window.

To use the program: 

>> python generate_Laguerre_Gauss_SLM.py [list of arguments] where: 

 -c CHARGE sets the CHARGE of the LG beam.
 -w RADIUS use this option to put a circular mask centered in the screen center.
 -g PERIOD add a grating to the LG phase. The period in pixels is specified with the variable PERIOD.

 -s when added the image generated is sent to the SLM
 -m when added, the SLM correction mask provided by the manufacturer is applied to the phase mask.
 -b when added, the image of the phase mask is stored in the bmp file "LG_ch_CHARGE.bmp"

The code requires the library slmpy.py, written by Sébastien Popoff that can be found on the link
http://wavefrontshaping.net/index.php/57-community/tutorials/spatial-lights-modulators-slms/124-how-to-control-a-slm-with-python
             
Usage examples:

>>python LaguerreGauss.py -c 10 -5 (SLM split in two masks | LG +10 | LG -5 |. The image generated is not sent to the SLM)
>>python LaguerreGauss.py -c 10 -5 -b (add -b to save image as LG_ch_10_-5.bmp)
>>python LaguerreGauss.py -c 10 -5 -m -s (image sent to SLM) 

To exit, press 'q' after clicking on the 'phase mask' window.

"""

import argparse
import cv2
import numpy as np
import scipy.misc
import slmpy
import imutils

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-c', '--charge', nargs='+', type=int, default= [10,10])
ap.add_argument("-w", "--window",	help="mask window radius (default = 0)", type=int, default = 0)
ap.add_argument("-g", "--grating", nargs='+', type=int, default= [0,0])

feature_parser = ap.add_mutually_exclusive_group(required=False)
feature_parser.add_argument("-s","--slm", help="send image to SLM", action='store_true')

feature_parser = ap.add_mutually_exclusive_group(required=False)
feature_parser.add_argument("-m","--mask", help="apply correction mask", action='store_true')

feature_parser = ap.add_mutually_exclusive_group(required=False)
feature_parser.add_argument("-b","--bmp", help="save *.bmp file", action='store_true')

args = vars(ap.parse_args())

beamCharge = args["charge"]
saveFlag = args["bmp"]
slmFlag = args["slm"]
correctionFlag = args["mask"]
maskRadius = np.abs(args["window"])
gratingPeriod1 = args["grating"][0]
gratingPeriod2 = args["grating"][1]

beamCharge1 = args["charge"][0]
beamCharge2 = args["charge"][1]

fileStr = 'LG_ch_' + str(beamCharge1) + '_' + str(beamCharge2) + '.bmp'

# change 'correctionMaskFile' according to your correction mask file
correctionMaskFile = 'CAL_LSH0600780_633nm.bmp';

# generate phase mask for LG beam
def generate_LG_Mask(beamCharge):
    
    if beamCharge == 0:
        image = np.zeros([ImgResY, ImgResX])
    else:             
        image = np.angle(np.exp((beamCharge*np.angle(X+Y*1j))*1j))        

    image8bit = normalize_image(image)
    
    return image8bit

def generate_displaced_LG_Mask(beamCharge, gratingPeriod):
    
    # if period = 0 ... show zero phase mask
    if gratingPeriod == 0:
        image = np.zeros([ImgResY, ImgResX])
    # if period > 0 ... shift beam to the RIGHT wrt period = 0
    elif gratingPeriod > 0:             
        image = np.angle(np.exp((2*np.pi*X/gratingPeriod)*1j)+np.exp((beamCharge*np.angle(X+Y*1j))*1j))
    # if period < 0 ... shift beam to the LEFT wrt period = 0
    elif gratingPeriod < 0:             
        image = np.angle(np.exp((2*np.pi*X/gratingPeriod+np.pi)*1j)+np.exp((beamCharge*np.angle(X+Y*1j))*1j))

    image8bit = normalize_image(image)
    
    return image8bit

# normalize image to range [0, 1]    
def normalize_image(image):
    img = cv2.normalize(image, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    image8bit = np.round((2**8-1)*(img)).astype('uint8')
    
    return image8bit

def apply_correction_mask(image):
    
    SLMcorrectionMask = np.zeros((ImgResY, ImgResX), dtype = "uint8")       
    
    # mask exclusive for Hamamatsu SLM S/N LSH0600780    
    SLMbmpMask = cv2.imread(correctionMaskFile)

    SLMbmpMask = cv2.cvtColor(SLMbmpMask, cv2.COLOR_BGR2GRAY)

    rows,cols = SLMbmpMask.shape
    
    SLMcorrectionMask[0:rows, 0:cols] = SLMbmpMask

    return SLMcorrectionMask+image

if slmFlag == True:
    # create the object that handles the SLM array
    slm = slmpy.SLMdisplay(isImageLock = True)

    # retrieve SLM resolution (defined in monitor options)
    ImgResX, ImgResY = slm.getSize()
else:
    
    ImgResX = 792
    ImgResY = 600

ImgCenterX = ImgResX/2
ImgCenterY = ImgResY/2

x = np.linspace(0,ImgResX,ImgResX)
y = np.linspace(0,ImgResY,ImgResY)

# initialize image matrix
X, Y = np.meshgrid(x,y)

X = X - ImgCenterX
Y = Y - ImgCenterY

# generate circular window mask
maskCircle = np.zeros((ImgResY, ImgResX), dtype = "uint8")
cv2.circle(maskCircle, (ImgCenterX, ImgCenterY), maskRadius, 255, -1)
maskCircle = normalize_image(maskCircle)

# generate and apply squared mask to image8bit
windowSize = ImgResX/2
maskWindow = np.zeros((ImgResY, ImgResX), dtype = "uint8")
cv2.rectangle(maskWindow, (ImgCenterX-windowSize/2, ImgCenterY-windowSize/2), (ImgCenterX+windowSize/2, ImgCenterY+windowSize/2), 255, -1)
maskWindow = normalize_image(maskWindow)

if slmFlag != True:
    
    if gratingPeriod1 or gratingPeriod2 != 0:
        
        image8bit1 = generate_displaced_LG_Mask(beamCharge1, gratingPeriod1)
        image8bit2 = generate_displaced_LG_Mask(beamCharge2, gratingPeriod2)
   
    else:
        
        image8bit1 = generate_LG_Mask(beamCharge1)
        image8bit2 = generate_LG_Mask(beamCharge2)
   
    if maskRadius > 0:
        image8bit1 = cv2.bitwise_and(image8bit1, image8bit1 , mask = maskCircle) 
        image8bit2 = cv2.bitwise_and(image8bit2, image8bit2 , mask = maskCircle)            
    else:
        image8bit1 = cv2.bitwise_and(image8bit1, image8bit1 , mask = maskWindow)    
        image8bit2 = cv2.bitwise_and(image8bit2, image8bit2 , mask = maskWindow)       
   
    # translate the image x=100 pixels to the left and y=0 pixels up
    image8bit1 = imutils.translate(image8bit1, -ImgResX/4, 0)
    image8bit2 = imutils.translate(image8bit2, ImgResX/4, 0)                      

    image8bit = cv2.add(image8bit1,image8bit2)
    
    # apply SLM correction mask provided by manufacturer        
    if correctionFlag == True:
        image8bit = apply_correction_mask(image8bit)
            
    cv2.imshow('phase hologram',image8bit)
    cv2.waitKey()
    
    if saveFlag == True:
        scipy.misc.imsave(fileStr, image8bit)
        print "file: " + fileStr + " saved! Press any key to continue."
    
else:    
    
    while True:

        if gratingPeriod1 or gratingPeriod2 != 0:
        
            image8bit1 = generate_displaced_LG_Mask(beamCharge1, gratingPeriod1)
            image8bit2 = generate_displaced_LG_Mask(beamCharge2, gratingPeriod2)
   
        else:
        
            image8bit1 = generate_LG_Mask(beamCharge1)
            image8bit2 = generate_LG_Mask(beamCharge2)
   
        if maskRadius > 0:
            image8bit1 = cv2.bitwise_and(image8bit1, image8bit1 , mask = maskCircle) 
            image8bit2 = cv2.bitwise_and(image8bit2, image8bit2 , mask = maskCircle)            
        else:
            image8bit1 = cv2.bitwise_and(image8bit1, image8bit1 , mask = maskWindow)    
            image8bit2 = cv2.bitwise_and(image8bit2, image8bit2 , mask = maskWindow)       
   
        # translate the image x=100 pixels to the left and y=0 pixels up
        image8bit1 = imutils.translate(image8bit1, -ImgResX/4, 0)
        image8bit2 = imutils.translate(image8bit2, ImgResX/4, 0)                      

        image8bit = cv2.add(image8bit1,image8bit2)
        
        # apply SLM correction mask provided by manufacturer        
        if correctionFlag == True:
           image8bit = apply_correction_mask(image8bit)

        image = cv2.resize(image8bit,(320, 240), interpolation = cv2.INTER_CUBIC)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        cv2.putText(image, "press q to exit...", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)    

        # display image on window
        cv2.imshow('SLM',image)       
    
        # send image to SLM    
        slm.updateArray(image8bit)
    
        # press 'q' to exit   
        key = cv2.waitKey(33)
        if key == ord('q'):
            break
    
    slm.close()
    cv2.destroyAllWindows()
    
    
    
    
