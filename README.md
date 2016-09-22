# python-SLM
Set of routines in Python used to control a Spatial Light Modulator. It is assumed that the SLM is connected to a secondary monitor.

**Important!!!** The code requires the following modules installed:
* opencv
* numpy
* wxPython 
* slmpy (file that can be downloaded from [Sébastien's POPOFF](http://wavefrontshaping.net/index.php/57-community/tutorials/spatial-lights-modulators-slms/124-how-to-control-a-slm-with-python)) page.

## Files

File | Description
------------ | -------------
generate_Laguerre_Gauss_SLM.py | File that generates a phase mask for a LG beam and displays it on a SLM

## Files description
### generate_Laguerre_Gauss_SLM.py
The file generates a phase mask for a LG beam with a charge specified by the user. The mask can be saved as a bmp file, displayed on the main monitor, or can be sent to the SLM.

#### How to use it
To use the function, just write `python generate_Laguerre_Gauss_SLM.py [options]`, where the options are the following:

* -c CHARGE sets the **CHARGE** of the LG beam.
* -w RADIUS use this option to put a circular mask centered in the screen center with radius **RADIUS**.
* -g PERIOD add a grating to the LG phase. The period in pixels is specified with the variable **PERIOD**.
* -s when added the image generated is sent to the SLM (by default the phase mask is not sent to the SLM).
* -m when added, the SLM correction mask provided by the manufacturer is applied to the phase mask.
* -b when added, the image of the phase mask is stored in the bmp file "LG_ch_CHARGE.bmp", where **CHARGE** is specified with the option -c.

The correction mask file has to be stored in the same folder as the python file. To change the mask name, just change the line 133 (change **mask_750nm.bmp**) according to your file.

To exit, press 'q' after clicking on the 'phase mask' window.

#### Usage examples

* Use `python generate_Laguerre_Gauss_SLM.py -c 10`, to generate a phase mask (LG beam charge +10) that is shown only in the main screen.
* To save the image in a bmp file, use `python generate_Laguerre_Gauss_SLM.py -c 10 -b`. The file will be saved as **LG_ch_10.bmp**.
* To generate and send to the SLM a phase mask for a LG beam with charge -5, use `python generate_Laguerre_Gauss_SLM.py -c -5 -m -s`. Notice that the option **-m** specifies to use the correction mask provided by the manufacturer.





