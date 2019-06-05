# Microscope-Measurement-Tools
Microscope Measurement plugin for [FIJI](http://fiji.sc).

This set of [FIJI](http://fiji.sc) plugins provides a quick way to save distance/length calibrations for various microscopes/objectives in a simple text file, and then draw calibrated distances onto your images.

You can then choose any of your prior calibrations to be applied to an open image (or all open images), as so: 

![Choose Calibration window][MMT-Choose-Cal-Pic]


The "Draw Measurement" plugin then allows you to draw a line with the calibrated measurement length, as so: 

![Annotation with Line][MMT-Annot-Line-Pic]


# Installation
Download and install the [scientific image analysis program FIJI](http://fiji.sc).

Download the most recent [Microscope Tools Release from Github](https://github.com/demisjohn/Microscope-Measurement-Tools/releases).  
For the *UCSB Fork*, [download the forked repo](https://github.com/demisjohn/Microscope-Measurement-Tools-UCSB/archive/master.zip).

View the [Instructions PDF on Github](https://github.com/demisjohn/Microscope-Measurement-Tools/blob/master/Microscope%20Meas.%20-%20Calibration%20instructions.pdf) for the Installation & Calibration procedure.

# Usage
Three files are included, which will show up in your FIJI "Analyze" menu:

+ **Choose_Microscope_Calibration.py**
  + *Opens the "Choose Calibration" window, for setting the measurement scale to a preconfigured value.*
+ **Draw_Measurement_-_Line.py**
  + *Converts a Line ROI into a drawn annotation with the measurement length indicated.*
+ **Microscope_Calibrations_user_settings.py**
  + *User-editable Settings file that contains your pre-configured scale calibrations, along with settings for drawing annotations (background/text color etc.)*
  + Please see the Instructions PDF for detailed instructions on setting up your settings file with Calibrations.
  
[MMT-Choose-Cal-Pic]: http://fiji.sc/_images/c/cd/Microscope_Meas_Tools_-_Choose_Calibration_01.png
[MMT-Annot-Line-Pic]: http://fiji.sc/_images/f/f4/Microscope_Meas_Tools_-_Draw_Meas_Line.png

## Custom Calibration Functions
A custom function can be added to the list of available calibrations (as opposed to a static scale value).  A sub-folder is included showing an example of how to do this. The example is for a JEOL SEM (scanning electron microscope), and the example function will determine the scale of the SEM image by parsing an accompanying text file.

See the files in the sub-folder "*MScopeCals - custom function example*" for more info, and move both of the `*.py` files into the main *Microscope Measurement Tools* folder to see how they can be used.  An example SEM image and TXT file from a JEOM 7600F SEM are included.

# Contact

Feel free to add Issues/Feature Requests, or even better, Fork the `git` repository and submit your own updates (see this [how-to](http://kbroman.org/github_tutorial/pages/fork.html))!

June 2019, Demis D. John
