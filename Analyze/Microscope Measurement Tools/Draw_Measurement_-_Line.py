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
libpth = os.path.join(libpth, 'plugins', 'Analyze', 'Microscope Measurement Tools')
# hard-coded path, within the Fiji directory.

try:
    sys.path.index( libpth )    # see if search-path is already added
except ValueError:
    # path wasn't included yet, so add it:
    sys.path.append( libpth )
#sys.path.append('/Applications/Fiji.app/plugins/Scripts/Analyze/Microscope Measurement Tools/')
#print sys.path

# microscope settings should be in the file `Microscope_Calibrations_user_settings.py`:
import Microscope_Calibrations_user_settings as sets      # imports settings under `sets.linecolor`, `sets.linethickness` etc.

#print os.path.abspath(sets.__file__)
#print dir(sets)
#print sets.cals    # see what calibrations have been set


# the run() function is called at the end of this script:
def run():
    '''This is the main function run when the plugin is called.'''
    
    #print dir(IJ)
    ip = IJ.getProcessor()
    
    imp = IJ.getImage()     # get the current Image, which is an ImagePlus object
    #print "imp=", type(imp), imp
    #print dir(imp)
    
    roi = imp.getRoi()  # get the drawn ROI
    #print "roi=", roi, roi.getClass()
    
    
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
    
    
    
    
    p1 = [  int(roi.x1d),  int(roi.y1d)  ]    # point 1 (x,y)
    p2 = [  int(roi.x2d),  int(roi.y2d)  ]    # point 2
    print "DrawMeas(): Line Points: p1=", p1, " & p2=", p2
    pm = midpoint(p1, p2)   # get midpoint coord
    
    
    # set ROI params from settings:
    ''' Using new method - used ip.drawLine instead of roi.draw, since roi.draw didn't always apply the line thickness.  Would be best to use the ROI method, in case other types of ROI's could be annotated.
    
    roi.setStrokeWidth( sets.linethickness )
    roi.setStrokeColor(  jColor(float(sets.linecolor[0]), float(sets.linecolor[1]), float(sets.linecolor[2]), float(sets.linecolor[3]))  )
    
    #roi.drawPixels( ip )   # draw along the ROI - only draws outline unfortunately
    ip.drawRoi(roi)     # draw the ROI on the image
    '''
    
    ip.setLineWidth(  int(sets.linethickness)  )      
    ip.setColor(  jColor(float(sets.linecolor[0]), float(sets.linecolor[1]), float(sets.linecolor[2]), float(sets.linecolor[3]))  )
    
    #ip.draw(roi)   # changed to ip.drawLine()
    ip.drawLine( int(roi.x1d),  int(roi.y1d), int(roi.x2d),  int(roi.y2d)  )

    
    
    
    '''Draw text annotation'''
    unit = imp.getCalibration().getUnit().encode('utf-8')    # get the unit as UTF-8 (for \mu)
    if len(unit) == 3 : unit=unit[1:] # strip weird char at start of \mu
    print "Draw_Meas(): Unit (raw) = `", unit,"`", type(unit),


    # format of measurement text (eg. 3 decimal points):
    lenstr = "%0.3f" % roi.getLength() + " %s" % (unit)  # string to print as length
    print "DrawMeas(): Line length= %s" % lenstr
    #print "x,y=", p2[0], p2[1]
    
    '''determine position of text from line coords, eg "bottom right" or "top left" etc.   '''
    # y-coord:
    if p2[1] > p1[1]:
        posstr = 'bottom'
    else:
        posstr = 'top'
    
    # x-coord:
    if p2[0] > p1[0]:
        posstr += ' right'
    else:
        posstr += ' left'
    
    
    drawText( lenstr, p2[0], p2[1], position=posstr  )
    
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



def drawText( text, x, y, position='bottom right' ):
    '''Draw a text string at the specified coordinates & relative position, ensuring text doesn't go over the edge of the image.
    
    Parameters:
    -----------
    text : string
        The text string to write on the image.
    
    x, y : int
        The coordinates at which to draw the text.
    
    position : { 'bottom right', 'top right', 'top left', 'bottom left' }, case-insensitive, optional
        Where to draw the text, with respect to the coordinates given.
        Synonyms for 'bottom right' are 'br'.  This is the default.
        Synonyms for 'top right' are 'tr'.
        Synonyms for 'bottom left' are 'bl'.
        Synonyms for 'top left' are 'tl'.
    '''
    print "drawText(): original (x,y)=(%i,%i)"%( x, y )
    
    
    # microscope settings should be in the file `Microscope_Calibrations_user_settings.py`:
    import Microscope_Calibrations_user_settings as sets      # imports settings under `sets.linecolor`, `sets.linethickness` etc.
    
    ip = IJ.getProcessor()  # Image Processor
    imp = IJ.getImage()     # get the current Image, which is an ImagePlus object
    
    
    '''Acquire arguments'''
    position = position.strip().lower()
    if position == 'bottom right' or position == 'br':
        pos = 'br'
    elif position == 'bottom left' or position == 'bl':
        pos = 'bl'
    elif position == 'top left' or position == 'tl':
        pos = 'tl'
    elif position == 'top right' or position == 'tr':
        pos = 'tr'
    else:
        raise ValueError( 'drawText(): Invalid `position` argument: "%s".'%(position) )
    
    
    
    
    '''Setup text annotation'''
    # set font:
    ip.setFont(   jFont('SansSerif', 0, sets.textsize)   )
    ip.setColor(    jColor(  float(sets.textcolor[0]), float(sets.textcolor[1]), float(sets.textcolor[2]), float(sets.textcolor[3])  )   )
    
    
    
    
    '''determine text position'''
    margin = 6      # space in pixels away from edge of image
    spacer = 4      # space in pixels to add between point & text
    strw = ip.getStringWidth(text)
    strh = ip.getFontMetrics().getHeight()
    imgw = ip.getWidth()
    imgh = ip.getHeight()
    
    '''
    print "strw =", strw
    print "strh =", strh
    print "imgw =", imgw
    print "imgh =", imgh
    '''
    
    
    # set coords (x,y) based on `position` argument
    ''' By default, text is horizontally centered at point (x), and vertically above the point (y).  We then modify these default coords.  '''

    if pos[0] == 'b':
        y = y + spacer + strh   # moves down 
    elif pos[0] == 't':
        y = y - spacer
    
    if pos[1] == 'r':
        x = x + spacer     # moves right
    elif pos[1] == 'l':
        x = x - spacer - int(strw)
    
    print "drawText(): %s "%(pos) + "(x,y)=(%i,%i)"%( x, y )
    
    '''Correct for edge of image'''
    if   y - strh < 0:
        y = 0 + strh + margin
    elif   y > imgh :
        y = imgh - margin
    
    if   (x) < 0:
        x = 0 + margin
    elif  (x + strw) > imgw:
        x = imgw - strw - margin
    
    print "drawText(): final (x,y)=(%i,%i)"%( x, y )
    
    
    if sets.textbackgroundcolor:
        ip.drawString( text, x, y, jColor(  float(sets.textbackgroundcolor[0]), float(sets.textbackgroundcolor[1]), float(sets.textbackgroundcolor[2]), float(sets.textbackgroundcolor[3])  ) )     # write the text w/ BG color
    else:
        ip.drawString( text, x, y )     # write the text alone

    imp.updateAndDraw()     #update the image
#end drawText()



run()       # Finally, Run the script function!

