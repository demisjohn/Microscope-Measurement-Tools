# Microscope-Measurement-Tools
Microscope Measurement plugin for [FIJI](http://fiji.sc).

This set of [FIJI](http://fiji.sc) plugins provides a quick way to save distance/length calibrations for various microscopes/objectives in a simple text file, and then draw calibrated distances onto your images.

You can then choose any of your prior calibrations to be applied to an open image (or all open images), as so: 

![Choose Calibration window][MMT-Choose-Cal-Pic]


The "Draw Measurement" plugin then allows you to draw a line with the calibrated measurement length, as so: 

![Annotation with Line][MMT-Annot-Line-Pic]


## Installation
Download the most recent [Release from Github](https://github.com/demisjohn/Microscope-Measurement-Tools/releases).

View the [Instructions PDF on Github](https://github.com/demisjohn/Microscope-Measurement-Tools/blob/master/Microscope%20Meas.%20-%20Calibration%20instructions.pdf) for the Installation & Calibration procedure.

Three files are included:

+ **Choose_Microscope_Calibration.py**
  + *Opens the "Choose Calibration" window, for setting the measurement scale to a preconfigured value.*
+ **Draw_Measurement_-_Line.py**
  + *Converts a Line ROI into a drawn annotation with the measurement length indicated.*
+ **Microscope_Calibrations_user_settings.py**
  + *User-editable Settings file that contains your pre-configured scale calibrations, along with settings for drawing annotations (background/text color etc.)*
  + Please see the Instructions PDF for detailed instructions on setting up your settings file with Calibrations.


[MMT-Choose-Cal-Pic]: http://fiji.sc/_images/c/cd/Microscope_Meas_Tools_-_Choose_Calibration_01.png
[MMT-Annot-Line-Pic]: http://fiji.sc/_images/f/f4/Microscope_Meas_Tools_-_Draw_Meas_Line.png

#### Contact

Feel free to add Issues/feature requests, or even better, Fork the `git` repository and submit your own updates (see this [how-to](http://kbroman.org/github_tutorial/pages/fork.html))!

Jan. 2016, Demis D. John
