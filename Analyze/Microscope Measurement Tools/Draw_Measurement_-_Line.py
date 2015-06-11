'''Draw Measurement - Line.py
Part of the "Microscope Measurement Tools" scripts
by Demis D. John, Praevium Research Inc., 2015-05-25

Draw a Line & Length of the Line along the currently selected Line ROI.

'''

#print "hello outside!"

## Import some modules:
from ij import IJ, ImagePlus, WindowManager #, gui
from ij.gui import GenericDialog, YesNoCancelDialog

from java.awt import Color as jColor    # for setting color
from java.awt import Font as jFont      # for setting text font

import sys, os




# add the path to this script, so we can find the user-settings
libpth = os.path.split(  os.path.split( sys.path[0] )[0]  )[0]  # split-off the "/jars/lib" part
#print  libpth
libpth = os.path.join(libpth, 'plugins', 'Scripts', 'Analyze', 'Microscope Measurement Tools')
# hard-coded path, underneath the Fiji directory.

try:
    sys.path.index( libpth )    # see if search-path is already added
except ValueError:
    # path wasn't included yet, so add it:
    sys.path.append( libpth )
#sys.path.append('/Applications/Fiji.app/plugins/Scripts/Plugins/uScopeMeas/')
#print sys.path

# microscope settings should be in the file `Microscope_Calibrations_user_settings.py`:
import Microscope_Calibrations_user_settings as sets      # imports settings under `sets.linecolor`, `sets.linethickness` etc.

#print os.path.abspath(sets.__file__)
#print dir(sets)
#print sets.cals


# the run() function is called at the end of this script:
def run():
    '''This is the main function run when the plugin is called.'''
    
    #print dir(IJ)
    ip = IJ.getProcessor()
    
    imp = IJ.getImage()     # get the current Image, which is an ImagePlus object
    #print "imp=", type(imp), imp
    #print dir(imp)
    
    roi = imp.getRoi()  # get the drawn ROI
    #print "roi=", roi
    
    #print roi.getClass()
    
    
    # check ROI type
    if roi==None:
        gd = GenericDialog("Draw Measurement - Line")
        gd.addMessage("Please draw a straight-line first!")
        gd.showDialog()
        return
        #raise Exception(  "Please draw a line ROI first!" )
    if roi.getTypeAsString()  != "Straight Line":
        gd = GenericDialog("Draw Measurement - Line")
        gd.addMessage("Please draw a straight-line first!")
        gd.showDialog()
        return
        #raise Exception(  "Not a Line ROI!  (type="+roi.getTypeAsString()+")"  )
    
    
    
    # set ROI params from settings:
    roi.setStrokeWidth( sets.linethickness )
    roi.setStrokeColor(  jColor(float(sets.linecolor[0]), float(sets.linecolor[1]), float(sets.linecolor[2]), float(sets.linecolor[3]))  )
    
    #roi.drawPixels( ip )   # draw along the ROI - only draws outline unfortunately
    ip.drawRoi(roi)     # draw the ROI on the image
    

    #imp.updateAndDraw()     #update the image
    
    p1 = [  int(roi.x1d),  int(roi.y1d)  ]    # point 1 (x,y)
    p2 = [  int(roi.x2d),  int(roi.y2d)  ]    # point 2
    print "Line Points: p1=", p1, " & p2=", p2
    pm = midpoint(p1, p2)   # get midpoint coord
    
    unit = imp.getCalibration().getUnit().encode('utf8')    # get the unit as UTF-8 (for \mu)
    if unit != 'pixel': unit=unit[1:]  # strip weird char at start
    
    
    # format of measurement text (eg. 3 decimal points):
    lenstr = "%0.3f" % roi.getLength() + " %s" % (unit)  # string to print as length
    print "Line length= %s" % lenstr
    print "x,y=", p2[0], p2[1]
    
    #ip.moveTo(p2[0]-ip.getStringWidth(lenstr), p2[1]);  # move the drawing 'pen'
    if sets.texttoleft:
        x=p2[0]-ip.getStringWidth(lenstr)
    else:
        x = p2[0]
    y=p2[1]
    
    
    # set font
    ip.setFont(   jFont('SansSerif', 0, sets.textsize)   )
    ip.setColor(    jColor(  float(sets.textcolor[0]), float(sets.textcolor[1]), float(sets.textcolor[2]), float(sets.textcolor[3])  )   )
    
    
    if sets.textbackgroundcolor:
        ip.drawString( lenstr, x, y, jColor(  float(sets.textbackgroundcolor[0]), float(sets.textbackgroundcolor[1]), float(sets.textbackgroundcolor[2]), float(sets.textbackgroundcolor[3])  ) )     # write the text w/ BG color
    else:
        ip.drawString( lenstr, x, y )     # write the text
    
    
    imp.updateAndDraw()     #update the image
    
    # to do:
    #   Add dialogue for user to alter draw options?  Or just from settings file?
    
    
    
#end run()
""" java.awt.Font: Font(String name, int style (0=plain?), int size)    """
"""
class ImageProcessor:
    drawString(java.lang.String s, int x, int y)
        Draws a string at the specified location using the current fill/draw value.
    drawString(java.lang.String s, int x, int y, java.awt.Color background)
        Draws a string at the specified location with a filled background.
"""
'''ImageProcessor:
    drawRoi(Roi roi):  Draws the specified ROI on this image using the stroke width, stroke color and fill color defined by roi.setStrokeWidth, roi.setStrokeColor() and roi.setFillColor().
'''



def midpoint( p1, p2 ):
    ''' return the midpoint as [x,y] list.
    Takes two points, also as a pair of [x,y] lists.
    '''
    
    x1 = min( p1[0], p2[0] )
    y1 = min( p1[1], p2[1] )
    x2 = max( p1[0], p2[0] )
    y2 = max( p1[1], p2[1] )
    
    xm = (x2-x1)/2. + x1
    ym = (y2-y1)/2. + y1
    
    return [int(xm), int(ym)]
#end midpoint()




run()       # Run the script function!

