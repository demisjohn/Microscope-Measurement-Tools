'''
	FIJI Plugin
Additional Function for Choose_Microscope_Calibration.py
Demis D. John, Univ. of California Santa Barbara, 2019

This file adds functions for JEOL SEM images files, to automatically load the scale calbration from the accompanying *.txt file.
Find accompying *.txt file with same name/locaiton as the image file, parse out the pixel-to-unitlength info, and apply the scale automatically.
Designed against a JEOL 7600F SEM with the followig TXT file version info:
$CM_FORMAT      JEOL-SEM
$CM_VERSION     1.0

The class will be accessed by  `Choose_Microscope_Calibration.py`.
The class must have methods named as follows:
    MyClass() - class constructor, which defines MyClass.name attribute:
    MyClass.name - a string that shows up in the available calibrations list.
    MyClass.cal() - returns the Pixel-Per-Unit calibration (numeric)
    MyClass.unit - a string that is the measurement unit, eg. "cm" or "nm" etc.
    MyClass.aspect - numeric value of pixel aspect ratio, eg. 1.0

After you edit this file, be sure to delete the corresponding *.pyclass file and restart Fiji for the changes to take effect.
'''


"""
################################
   JEOL SEM AutoCal from *.txt
################################


"""

jeol_DEBUG = False     # Send debugging info to the log file?


class JEOL_SEM_CalFromTxt(object):
    '''    Class with functions for automatic calibration of image scale.
    
    JEOL_SEM_CalFromTxt() : (Constructor)
        Only sets the `name` to be used in the Calibrations list.
    
    JEOL_SEM_CalFromTxt.name : string
        The name that shows up in the Calibrations list.
    
    JEOL_SEM_CalFromTxt.cal(  ImagePlus_Object ) :
        Takes in the ImagePlusObject being analyzed.
        Returns the pixel-per-unit numeric value, using a custom function.
        Sets the following internal attributes:
            self.pixel_per_unit (unused)
            self.unit
            self.aspect_ratio
    
    JEOL_SEM_CalFromTxt.unit : string
        String indicating the unit used in the pixel-per-unit returned by `self.cal()`.  The string will be used by annotations and set internally in ImageJ's "Set Scale" etc.  Should be the short abbreviation of the unit name.
        Examples: "mm", "cm", "um" (will be converted to greek `mu` by ImageJ)
    
    JEOL_SEM_CalFromTxt.aspect_ratio
        Numeric aspect ratio (width/height) of the pixel-per-unit, typically 1.0.
    
    '''
    
    def __init__(self):
        ''' See `help(JEOL_SEM_CalFromTxt)` for help on this constructor.'''
        self.name =     "JEOL SEM: AutoCal from *.txt"
    #end __init__()
    

    def cal( self, imp ):
        '''
        Takes in the ImagePlusObject being analyzed.
        Returns the pixel-per-unit numeric value.
        For JEOL SEM image files, this is done by locating the accompying *.txt text-file and parsign it to find the image scale values.
        Sets the following internal attributes:
            self.unit
            self.aspect_ratio
        '''
        
        import re   # RegEx matching, for parsing text file
        import os.path  # file-path manipulation functions
        
        filepath =    imp.getOriginalFileInfo().directory  +  os.path.sep  +  imp.getOriginalFileInfo().fileName
        if jeol_DEBUG: 
            print( "imp=", imp )
            print( "ImagePath=", filepath )
        
        txtpath = os.path.splitext( filepath )[0] + ".txt"
        if jeol_DEBUG: print "txtpath = ", txtpath
        if not os.path.isfile(txtpath): raise IOError("Text File not found at: \n\t" + txtpath)
        
        # set up regex search groups:
        re_bar = re.compile( r'\$\$SM_MICRON_BAR (\d*)'  ) # captures the digits in "$$SM_MICRON_BAR 90" to a group
        re_barmark = re.compile( r'\$\$SM_MICRON_MARKER (\d*)([a-zA-Z]*)')  # captures the decimals and units in "$$SM_MICRON_MARKER 100nm" to separate groups
    
    
        # try to load the .txt file:
        BarLength_px = None
        BarLength_dist = None
        BarLength_unit = None
    
        txtfile = open(txtpath, 'r')
        try:
            while True:
                txtline = txtfile.readline()  # grab one line of text
                if len(txtline) == 0:
                    # end of file, exit the loop
                    break
                #end(if end-of-file)
            
            
                # search for strings/values:
                match1 = re_bar.search( txtline )
                if match1:
                    BarLength_px = float( match1.group(1)  )  # this is pixel width of the scale bar
                    if jeol_DEBUG: print 'Scale Bar Pixel Length found:', match1.groups(), ' --> ', BarLength_px    
                #end if(match1)
            
            
                match2 = re_barmark.search( txtline )
                if match2:
                    BarLength_dist = float( match2.group(1)  )  # this is physical width of the scale bar
                    BarLength_unit = str( match2.group(2)  )
                    if jeol_DEBUG: print 'Scale Bar Distance Length found:', match2.groups(), ' --> ', BarLength_dist, BarLength_unit
                #end if(match2)
            
            #end while(file-reading)

        except IOError:
            raise IOError("Could not load text file that accompanies this image file.  Expected the text file to have the same filename as the image, except with '.txt' extension.  Expected file to be here:\n\t" + txtpath )
    
        finally:
            # make sure python closes the file no matter what
            txtfile.close()
        #end try(txtfile)
        
        self.pixel_per_unit = (BarLength_px/BarLength_dist)
        self.unit = BarLength_unit
        self.aspect_ratio = 1.0
        
        # return pixel-per-unit
        return self.pixel_per_unit
    #end cal()
#end class(JEOL_SEM_CalFromTxt)












'''
---------------------------------------------------------
Warn user if they run this file as a stand-alone plugin.
'''

def run():
    ''' If someone tries to run this file by itself, warn them of their error.  Unfortunately, since I was too lazy to make Microscope_Calibrations a full plugin (rather than a script), this accompanying settings file will show up in the Scripts menu.'''
    from ij.gui import GenericDialog
    
    gd = GenericDialog("Microscope_Calibrations_user_settings.py")
    gd.addMessage("This file is only for adding functionality to the plugin 'Microscope Measurement Tools'.\nNothing is done when this settings file is run by itself."  )
    
    gd.showDialog()
#end run()

if __name__ == '__main__':
    run()   # run the above function if the user called this file!


