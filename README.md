# python-SLM
Set of routines in Python used to control a Spatial Light Modulator

file: generate_Laguerre_Gauss_SLM.py

USAGE EXAMPLES
python generate_Laguerre_Gauss_SLM.py -c 10 (image generated is not sent to the SLM)
python generate_Laguerre_Gauss_SLM.py -c 10 -b (add -b to save image as LG_ch_10.bmp)
python generate_Laguerre_Gauss_SLM.py -c -5 -m -s (LG beam charge -5, use correction mask and image sent to SLM) 

To exit, press 'q' after clicking on the 'phase mask' window.

 *** List of options available ***

 -c CHARGE sets the CHARGE of the LG beam.
 
 -w RADIUS use this option to put a circular mask centered in the screen center.
 
 -g PERIOD add a grating to the LG phase. The period in pixels is specified with the variable PERIOD.

 -s when added the image generated is sent to the SLM.
 
 -m when added, the SLM correction mask provided by the manufacturer is applied to the phase mask.
 
 -b when added, the image of the phase mask is stored in the bmp file "LG_ch_CHARGE.bmp"


