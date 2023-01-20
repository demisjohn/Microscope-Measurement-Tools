'''
Draw_Rectangle_Long_Length.py
by Will Sides 2020-03-04

Contribution to the "Microscope Measurement Tools" scripts
by Demis D. John, Praevium Research Inc., 2015-05-25

Draws the long dimension of a rectangle or rotated rectangle
Draws extension lines defined by short side width of the rectangle
'''

from ij import IJ, ImagePlus, WindowManager 
from ij.gui import GenericDialog

from java.awt import Color as jColor    # for setting color
from java.awt import Font as jFont      # for setting text font

import sys, os

# add the path to this script, so we can find the user-settings
libpth = os.path.split(  os.path.split( sys.path[0] )[0]  )[0]  # split-off the "/jars/lib" part
#print  libpth
libpth = os.path.join(libpth, 'plugins', 'Analyze', 'Microscope Measurement Tools')
# hard-coded path, within the Fiji directory.

try:
    sys.path.index( libpth )    # see if search-path is already added
except ValueError:
    # path wasn't included yet, so add it:
    sys.path.append( libpth )

# Settings should be in the file 'DA_user_settings.py`:
import Microscope_Calibrations_user_settings as sets      # imports settings under `sets.linecolor`, `sets.linethickness` etc.

# the run() function is called at the end of this script:
def run():
    '''This is the main function run when the plugin is called.'''
    
    ip = IJ.getProcessor() #Construct a image processor
    
    imp = IJ.getImage()     # get the current Image, which is an ImagePlus object

    # Warn the user if no calibration has been set
    cal = imp.getCalibration()   
    unit = cal.getUnit().encode('utf8')  # get the unit as UTF-8 (for \mu)
    if len(unit) == 3 : unit=unit[1:] # strip weird char at start of \mu
    if unit=='pixel':
        gd = GenericDialog("No Calibration")
        gd.addMessage("Warning - no calibration set")
        gd.setCancelLabel("Continue anyway")
        gd.setOKLabel("Cancel")
        gd.showDialog()
        if gd.wasOKed():
        	return
    
    # check ROI exists
    roi = imp.getRoi()  # get the drawn ROI
    if roi==None:
        showInvalidROIDialog('Draw a rectangle first!')
        return

    # Check the ROI is a rectangle or rotated rectangle
    roiType=roi.getTypeAsString()
    print ('ROI type: ' + roiType)
    if roiType not in ["Rectangle", "Freehand"]:
        showInvalidROIDialog('Invalid shape - please draw a rectangle')
        return
    
    # Get the x,y, coordinates of the 4 corners of the rectangle
    x=roi.getFloatPolygon().xpoints
    y=roi.getFloatPolygon().ypoints
    
    # Calculate the side lengths
    l0=((x[0]-x[1])**2+(y[0]-y[1])**2)**0.5
    l1=((x[1]-x[2])**2+(y[1]-y[2])**2)**0.5
    l2=((x[2]-x[3])**2+(y[2]-y[3])**2)**0.5
    l3=((x[3]-x[0])**2+(y[3]-y[0])**2)**0.5

    # Rotated rectangles come back as generic 'Freehand' types, so we have to get creative to allow only rectangles (true parallelograms are also valid)
    if (len(x) != 4) or (len(y) != 4) or (abs(l0 - l2) > 0.01) or (abs(l1 - l3) > 0.01):
        showInvalidROIDialog('Invalid shape - please draw a rectangle')
        return

    # Calculate the coordinates in physical units
    calX=[]
    for i in x:
        calX.append(cal.getX(i))
    calY=[]
    for i in y:
        calY.append(cal.getX(i))

    # Test which side is the 'long' side to draw
    if l0 > l1:
        # Define the lines to draw as tuples: (x,y,x',y')
        topLine=(x[1],y[1],x[2],y[2])  # first 'short' side
        bottomLine=(x[3],y[3],x[0],y[0]) # the other 'short' side
        centerLine=((x[1]+x[2])*0.5,(y[1]+y[2])*0.5,(x[3]+x[0])*0.5,(y[3]+y[0])*0.5) # Connecting the 'short' sides through the middle, parallel to the long side
        calLength=((calX[0]-calX[1])**2+(calY[0]-calY[1])**2)**0.5 # length of the 'long' side in physical units
    else: 
        topLine=(x[0],y[0],x[1],y[1])
        bottomLine=(x[2],y[2],x[3],y[3])
        centerLine=((x[0]+x[1])*0.5,(y[0]+y[1])*0.5,(x[2]+x[3])*0.5,(y[2]+y[3])*0.5)
        calLength=((calX[1]-calX[2])**2+(calY[1]-calY[2])**2)**0.5

    # Determine the pixel coordinated to place the text label, in the center of the center-line
    textCenterPoint = ((centerLine[0]+centerLine[2])*0.5,(centerLine[1]+centerLine[3])*0.5)
    
    # format of measurement text:
    lenstr = "%0.1f" % calLength + " %s" % (unit)  # string to print
   
    drawLines( [topLine, bottomLine, centerLine] )
    drawText( lenstr, textCenterPoint )

#end run()

def drawLines( lines ):
    '''
    Draws the given lines on the image according to user settings

    Parameters:
    -----------
    lines : 
        List of lines to draw, each defined as a tuple of pixel coordinates: (x,y,x',y')
    '''    
    
    # microscope settings should be in the file `Microscope_Calibrations_user_settings.py`:
    import Microscope_Calibrations_user_settings as sets      # imports settings under `sets.linecolor`, `sets.linethickness` etc.
    
    ip = IJ.getProcessor()  # Image Processor
    imp = IJ.getImage()     # get the current Image, which is an ImagePlus object

    # Set Line drawing settings
    ip.setLineWidth(  int(sets.linethickness)  )      
    ip.setColor(  jColor(float(sets.linecolor[0]), float(sets.linecolor[1]), float(sets.linecolor[2]), float(sets.linecolor[3]))  )

    # Draw the lines
    for line in lines:
        ip.drawLine( *[int(n) for n in line] )

    imp.updateAndDraw()     #update the image
    
#end annotateHeight()

def drawText( text, xy ):
    '''
    Draw a text string at the specified coordinates & relative position, ensuring text doesn't go over the edge of the image.  

    Parameters:
    -----------
    text : 
        The text to draw
    
    xy : 
        The center (pixel) coordinates of the text
    '''   

    # microscope settings should be in the file `Microscope_Calibrations_user_settings.py`:
    import Microscope_Calibrations_user_settings as sets      # imports settings under `sets.linecolor`, `sets.linethickness` etc.
    
    ip = IJ.getProcessor()  # Image Processor
    imp = IJ.getImage()     # get the current Image, which is an ImagePlus object

    # set font:
    ip.setFont(   jFont('SansSerif', 0, sets.textsize)   )
    ip.setColor(    jColor(  float(sets.textcolor[0]), float(sets.textcolor[1]), float(sets.textcolor[2]), float(sets.textcolor[3])  )   )
    ip.setJustification( 1) # Justification: 0, 1, 2 = left, center, right    

    # get image size and label sizes
    imgw, imgh = ip.getWidth(), ip.getHeight()
    margin = 6      # space in pixels away from edge of image

    # get label size and position
    strw = ip.getStringWidth(text)
    strh = ip.getFontMetrics().getHeight()
    xtext, ytext = xy[0], xy[1] + (strh * 0.5)
 
    # Correct for edge of image
    if   ytext - strh < 0:
        ytext = 0 + strh + margin
    elif   ytext > imgh :
        ytext = imgh - margin
    
    if   (xtext - (strw * 0.5)) < 0:
        xtext = (strw * 0.5) + margin
    elif  (xtext + (strw * 0.5)) > imgw:
        xtext = imgw - (strw * 0.5) - margin
    
    # Draw the text
    if sets.textbackgroundcolor:
        ip.drawString( text, int(xtext), int(ytext), jColor(  float(sets.textbackgroundcolor[0]), float(sets.textbackgroundcolor[1]), float(sets.textbackgroundcolor[2]), float(sets.textbackgroundcolor[3])  ) )     # write the text w/ BG color
    else:
        ip.drawString( text, int(xtext), int(ytext) )     # write the text alone

    imp.updateAndDraw()     #update the image

#end drawText()

def showInvalidROIDialog( message ):
    # Shows the user a pop-up error message
    gd = GenericDialog("ROI Error")
    gd.addMessage(message)
    gd.showDialog()
#end showInvalidROIDialog

run()       # Finally, Run the script function!

