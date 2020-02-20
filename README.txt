 ### Information for use of AddTextToDXF ### 

@author Hans-Christian Ringstad

This script was made to be used in the Bachelor Thesis Manulab spring 2020,
it will put a logo image and a text on a dxf-file template. Files used in  
this program needs to be put in the same folder as the program. For the    
source code Python 3.8.1 was used.

 ### Files needed to run the program ###
info.csv: Contains information for the program to add text and logo image.
	  This csv-file uses ";" as separator and the program will only 
	  read the info in the last row.
	  This file will need to contain these fields;
	# Name of field # Datatype # Comment
	finalFileName   : String   : Name of the dxf file that will be created
	templateName    : String   : Name of the template to be used as background
	logoFileName    : String   : Name of the logo PNG-file
	xInsertPointLogo: float    : x-coordinate of the insert point of logo, the insertion point will be at the bottom right
	yInsertPointLogo: float    : y-coordinate of the insert point of logo, the insertion point will be at the bottom right
	xPixelSize      : int      : x length in pixels
	yPixelSize      : int      : y length in pixels
	xSizeInmm       : float    : x length in millimeter
	ySizeInmm       : float    : y length in millimeter
	rotationLogo    : float    : Rotation of logo
	textToInsert    : String   : Text to insert on the dxf file        
	textStyle       : String   : Text style
	xInsertPointText: float    : x-coordinate of the insert point of text, the insertion point will be at the top center
	yInsertPointText: float    : y-coordinate of the insert point of text, the insertion point will be at the top center
	rotationText    : float    : Rotation of text
	alignmentText   : int      : Alignement for the text, see doc for more info: https://ezdxf.mozman.at/docs/dxfentities/mtext.html#ezdxf.entities.MText.dxf.attachment_point
	textWidth       : float    : Width of text fields, does not cut ind ividual words
	textHeight      : float    : Height of text
	#               #          #

templateName.dxf: The file containing the dxf template to be used by the 
		  program, the name of the file is to be decided in 
		  info.csv

logoFileName.png: The file containing the the png of the logo in use to be 
	          used by the program, the name of the file is to be 
		  decided in info.csv

 ### Files created by the program ###
status.csv: Contains information on status of the program. This csv-file
	    uses ";" as seperator and the program will write the status at 
	    the bottom row read the info in the last row.
	    This file will contain these fields;
	# Name of field # Datatype # Comment
	working		: boolean  : True when active, false if inactive
	done		: boolean  : True when the dxf file was created succesfully
	error		: boolean  : True when an error has occured
	#		#	   #

finalFileName.dxf: The final dxf file created by the specifications in 
		   info.csv,the name of the file is to be decided in info.csv

errLog.txt: All expected errors will be printed to this file with an error
	    messege of what has caused it.