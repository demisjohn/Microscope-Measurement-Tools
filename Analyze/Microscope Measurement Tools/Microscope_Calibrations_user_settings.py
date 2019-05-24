'''
	FIJI Plugin - Microscope Measurement Tools
        Configuration for Choose_Microscope_Calibration.py & Draw_Measurement_-_Line.py
        Demis D. John, University of California Santa Barbara, Nanofabrication Facility, 2019
        https://www.nanotech.ucsb.edu

Make sure the lists `names`, `cals`, `units` and `aspect_ratio` all have the same number of items!

After you edit this file, be sure to delete the corresponding *.pyclass file and restart Fiji for the settings to take effect.


All of these lists are regular Python Lists, so define them however you prefer to define pythonic lists.  You can define them in-line like normal:
    x = [ 'one', 'two',  'three' ]
or in a vertical fashion:
    x = [
            'one',      # you can even comment on each line of the list
            'two',
            'three'
        ]
or even do python math on the lists, such as repeating an item with `*`, or using "list comprehensions".
'''


"""
################################
   Microscope Image settings
################################

Microscope scaling/pixel-size calibration settings.
"""

# The names of the microscope calibrations (shows up as the radio button/drop-down names):
names = [
        'FluoroScope 5x', 
        'FluoroScope 20x', 
        'FluoroScope 50x', 
        'FluoroScope 100x', 
        'FluoroScope 150x',
        'Olympus DUV 100x',
        ]


# The 'pixel-per-unit' obtained from the "Set Scale..." dialog, for each named calibration above:
cals = [
        0.9058,     # FluoroScope 5x to 150x
        1.81,  
        4.525,  
        9.0667,  
        13.5333,
        54.6875,    # Olympus DUV
        ]
#   This is just 1/pixel_width, in case you were wondering.


# length-units for each calibration:
#units = ['um','um','um','um','um']
# for identical units for all cals, can use the following line instead (uncomment):
units = ['um'    for x in cals]    # list-comprehension with constant `um`


# Aspect Ratio for each calibration (default should be 1.0 )
#   Ratio is defined as so: pixelHeight = pixelWidth * AspectRatio
# The following sets the aspect ratio to 1 for all calibrations:
aspect_ratio =  [ 1.0    for x in cals ]   # list-comprehension with constant `1`
# Uncomment the following line to use custom aspect ratios:
#aspect_ratio = [1, 1, 1, 1, 1]





"""
################################
       Draw Line settings
################################

Settings for the script "Draw Measurement - Line

Colors are specified as:
    [R, G, B, transparency] values, from 0->1.0.  
    Leave last value as 1 for completely opaque.  
    Eg. opaque red would be [1,0,0, 1]
    and half-transparent blue would be [0,0,1, 0.5]
    opaque black is [0,0,0, 1]
    opaque white is [1,1,1, 1]
"""

linethickness = 5.0     # in pixels
linecolor = [ 0, 0.7, 0,   1.0]     
textsize = 30           # text height in pixels, I think
textcolor =     [ 0, 0.8, 0,   1.0]
textbackgroundcolor = [ 0, 0, 0,   0.6]       # background color behind text.
#textbackgroundcolor = None      # set to None for no background - uncomment this line
texttoleft = True      # put text on left or right side of last point?










'''
---------------------------------------------------------
Warn user if they erroneously run this file as a stand-alone plugin.
'''

def run():
    ''' If someone tries to run this file by itself, warn them of their error.  Unfortunately, since I was too lazy to make Microscope_Calibrations a full plugin (rather than a script), this accompanying settings file will show up in the Scripts menu.'''
    from ij.gui import GenericDialog
    
    gd = GenericDialog("Microscope_Calibrations_user_settings.py")
    gd.addMessage("This file is only for setting the microscope calibrations and settings for the plugins 'Microscope Measurement Tools'.\nNothing is done when this settings file is run by itself.\nPlease open this file in a text editor instead, to edit the calibrations.\n  \n"  +  \
    "The file should reside in a path like the following\n"  +  \
    "Fiji.app/plugins/Scripts/Analyze/Microscope Measurement Tools/Microscope_Calibrations_user_settings.py\n  "  +  "\n" +  \
    "Changes to the settings file are not automatically picked up by Fiji.  The workaround is to\n  1) Quit Fiji.\n  2) Delete the '$py.class' file 'Microscope_Calibrations_user_settings$py.class'\n  3) Open Fiji.  Make sure the new settings show up in 'Choose Microscope Calibration'."  )
    
    gd.showDialog()
#end run()

if __name__ == '__main__':
    run()   # run the above function if the user called this file!

