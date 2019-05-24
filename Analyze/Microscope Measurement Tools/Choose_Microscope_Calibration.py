''' Choose_Microscope_Calibration.py
Plugin for FIJI, to enable custom scaling for various microscope objectives.

Reads user settings from `Microscope_Calibrations_user_settings.py` 
including user-calibrations and names for various microscope objectives.
This function will popup a menu of all available microscope cals listed in the settings file, and then apply that scaling (and unit) to the image.
User can optionally apply the scaling to all open images, and/or run the "Scale Bar..." command afterwards.

Based off Microscope_Scale.java & Correct_3d_drift.py


v2.2
Demis D. John, Univ. of California Santa Barbara, 2019-04-12
'''

mc_DEBUG = False     # Print debugging info to the console?

## Import some modules:
from ij import IJ, ImagePlus, WindowManager
from ij.gui import GenericDialog, YesNoCancelDialog

import sys, os




# add the path to this script, so we can find the user-settings
libpth = os.path.split(  os.path.split( sys.path[0] )[0]  )[0]  # path to Fiji folder
#print  libpth
libpth = os.path.join(libpth, 'plugins', 'Scripts', 'Analyze', 'Microscope Measurement Tools')


try:
    sys.path.index( libpth )    # see if search-path is already added
except ValueError:
    # path wasn't included yet, so add it:
    sys.path.append( libpth )
#sys.path.append('/Applications/Fiji.app/plugins/Scripts/Plugins/Demis/')
#print sys.path

# microscope settings should be in the file `Microscope_Calibrations_user_settings.py`:
import Microscope_Calibrations_user_settings as cal      # imports `names`, `cals`, `units` under namespace `cal.names` etc.




# the run() function is called at the end of this script:
def run():
    '''This is the main function run when the plugin is called.'''
    
    #print cal.names, cal.cals, cal.units
    
    
    imp = IJ.getImage()     # get the current Image as ImagePlus object

    # Show "Choose Calibration" dialog:
    CalIdx, SetGlobalScale, AddScaleBar = uScopeCalDialog(cal)
    
    if CalIdx == None: return       # User cancelled - exit
    
    newcal = imp.getCalibration().copy()   # make a copy of current calibration object
    
    if isinstance( cal.names[CalIdx], str ):
        '''It's just a regular calibration setting'''
        calName = cal.names[CalIdx]
        if mc_DEBUG: print("Calibration is Regular String/text")
        newPixelPerUnit = float( cal.cals[CalIdx] )
        newUnit = cal.units[CalIdx]
        newAspect = float( cal.aspect_ratio[CalIdx] )
        
        newPixelWidth = 1. / newPixelPerUnit
        newPixelHeight = newPixelWidth * newAspect
    else:
        ''' Assume we'll be loading a custom function/class '''
        if mc_DEBUG: print("Calibration is a custom function.")
        # call the class' `classObj.cal( ImagePlusObject )` function to get the scale value:
        try:
            calObject = cal.names[CalIdx]
            calName = calObject.name
            newPixelPerUnit = calObject.cal( imp )
        except AttributeError:
            raise ValueError('This calibration Name value is invalid, please check your Settings.py file!/n/tFor Calibration Number %i, got: `'%(CalIdx) + str(cal.names[CalIdx]) + '`. Expected a String or a Class instance with ".cal()" method, but got type ' + str( type(cal.names[CalIdx]) ) + ' with no ".cal()" method.' )
        #end try
        
        newUnit = calObject.unit
        newAspect = calObject.aspect_ratio
        
        newPixelWidth = 1. / newPixelPerUnit
        newPixelHeight = newPixelWidth * newAspect
    #end if(cal.name is a string or function)
    print "Chose `", calName, "` : ", newPixelPerUnit, " px/", newUnit
        
    #end if CalIdx

    # the following translated from "Microscope_Scale.java":
    newcal.setUnit(  newUnit  )
    newcal.pixelWidth =  newPixelWidth
    newcal.pixelHeight = newPixelHeight    

    
    if SetGlobalScale:
        '''Apply to all images'''
        imp.setGlobalCalibration(newcal)
        winlist = WindowManager.getIDList();
        #print "winlist=", winlist
        if (winlist==None):  return # exit if no images open
        for win in winlist:
            #(int i=0; i<list.length; i++) {
            nextimp = WindowManager.getImage(win);
            #print 'win=', win, '\tnextimp=', nextimp
            if (nextimp != None):   nextimp.getWindow().repaint()
    else:
        imp.setGlobalCalibration(None)
        imp.setCalibration( newcal )    # set the new calibration
        imp.getWindow().repaint()     # refresh the image?
    
    if AddScaleBar:
        IJ.run("Scale Bar...")  # run Scale Bar plugin
#end run()




def uScopeCalDialog(cal):
    ''' Pop up a dialog asking user to choose from the calibration names etc.
    
    CalIdx, SetGlobalScale, AddScaleBar = uScopeCalDialog(cal)
    
    `cal` should be the object containing `names`, `cals`, `units` attributes
    as set in the "user_settings.py" file.
    
    `CalIdx` is the list index to the chosen calibration.  
        Eg., if the options were 
            ['5x', '10x', '20x']
        and the user chose '10x', then 
            CalIdx = 1
        Returns `None` if the user cancelled the dialog.
    
    `SetGlobalScale` is a boolean (True/False) from a checkbox option, if the user wants this calibration set 'globally' to all open images.
    
    `AddScaleBar` is also a boolean (True/False), for a checkbox option, if user would like to run "Scale Bar..." afterwards.
    '''
    
    # The following inspired heavily by Correct_3D_drift.py:
    
    #print "uScopeCalDialog():"
    #print cal.names, [str(x) for x in cal.cals]
    
    gd = GenericDialog("Microscope Calibrations")
    gd.addMessage("Choose the calibration to load:")
    
    
    # generate text to display in list:
    # Radio Buttons:
    CalStr = []
    CalType_IsFunc = []
    
    
    for ii, name in enumerate(cal.names):
        if mc_DEBUG: print( "item #%i: name=" % (ii), name, "\n\t type=", type(name)  )
        if isinstance(name, basestring):
            '''It's just a regular calibration setting'''
            CalStr.append(  name + "      (%s"%cal.cals[ii] + " pixels/%s)"%cal.units[ii]  )
        else:
            ''' Assume we'll be loading a custom function/class '''
            CalStr.append(  name.name  )    # get the name from the Class' .name attribute
        #end if(str)
    #end for(cal.names)

    
    '''if > 20 cals, use dropdown list, otherwise use radio buttons'''
    if len(cal.names) > 20:
        Radio=False
        # Drop-Down list:
        gd.addChoice("     Calibration:", CalStr, CalStr[0]   )   # default = 1st (#0)
    
    else:
        Radio=True
        gd.addRadioButtonGroup("     Calibration:", CalStr, len(CalStr), 1, CalStr[0])
        #addRadioButtonGroup(label, [String items],  rows,  columns,  String:defaultItem)
    #end if(cal>20)
    
    gd.addCheckbox("Apply Scale to all open images?", False)
    gd.addCheckbox("Add Scale Bar to this image?", False)
    gd.addMessage("These calibrations can be altered by editing the file: \nFiji.app/plugins/Scripts/Plugins/Analyze/...\n\tMicroscope Measurement Tools/...\n\tMicroscope_Calibrations_user_settings.py")
    
    gd.showDialog()
    
    
    if gd.wasCanceled():
        return  None, None, None  # return None's if user cancels
    
    if Radio:
        ChosenCal = gd.getNextRadioButton()
        # Find the index to the chosen radio button w/ [list].index():
        CalIdx = CalStr.index(  ChosenCal )
    else:
        ChosenCal = gd.getNextChoiceIndex()
        CalIdx = ChosenCal  # the index to the choice
    
    SetGlobalScale = gd.getNextBoolean()
    AddScaleBar = gd.getNextBoolean()
    
    
    
    #if mc_DEBUG: print( ChosenCal,CalIdx, SetGlobalScale )
    #if mc_DEBUG: print( "end uScopeCalDialog()." )
    return CalIdx, SetGlobalScale, AddScaleBar
#end uScopeCalDialog()


run()       # Run the script function!


