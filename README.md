# Microscope-Measurement-Tools
Microscope Measurement plugin for FIJI

This set of plugins provides a quick way to save measurement calibrations for various microscopes/objectives in a simple text file.

You can then choose any of your prior calibrations to be applied to an open image (or all open images), as so: 

![Choose Calibration window][MMT-Choose-Cal-Pic]


The "Draw Measurement" plugin then allows you to annotate a line ROI with the calibrated measurement length, as so: 

![Annotation with Line][MMT-Annot-Line-Pic]


Three files are included:

* Choose_Microscope_Calibration.py
..* Opens the "Choose Calibration" window, for setting the measurement scale to a reconfigured value.
* Draw_Measurement_-_Line.py
..* Converts a Line ROI into a drawn annotation with the measurement length indicated.
* Microscope_Calibrations_user_settings.py
..* Settings file that contains your pre-configured scale calibrations, along with settings for drawing annotations (background/text color etc.)



[MMT-Choose-Cal-Pic]: http://fiji.sc/_images/c/cd/Microscope_Meas_Tools_-_Choose_Calibration_01.png
[MMT-Annot-Line-Pic]: http://fiji.sc/_images/f/f4/Microscope_Meas_Tools_-_Draw_Meas_Line.png
