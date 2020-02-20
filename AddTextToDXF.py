'''
 ### Information for use of AddTextToDXF ###

@author Hans-Christian Ringstad

This script was made to be used in the Bachelor Thesis Manulab spring 2020, it will put a logo image and a text on a
dxf-file template. Files used in this program needs to be put in the same folder as the program. For the source code
Python 3.8.1 was used.

 ### Files needed to run the program ###
info.csv: Contains information for the program to add text and logo image. This csv-file uses ";" as separator and the
          program will only read the info in the last row.
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
	alignmentText   : int      : Alignement for the text*
	textWidth       : float    : Width of text fields, does not cut ind ividual words
	textHeight      : float    : Height of text
	#               #          #
*See doc for more info: https://ezdxf.mozman.at/docs/dxfentities/mtext.html#ezdxf.entities.MText.dxf.attachment_point

templateName.dxf: The file containing the dxf template to be used by the program, the name of the file is to be decided
                  in info.csv

logoFileName.png: The file containing the the png of the logo in use to be used by the program, the name of the file is
                  to be decided in info.csv

 ### Files created by the program ###
status.csv: Contains information on status of the program. This csv-file uses ";" as separator and the program will
            write the status at the bottom row read the info in the last row.
	    This file will contain these fields;
	# Name of field # Datatype # Comment
	working		    : boolean  : True when active, false if inactive
	done		    : boolean  : True when the dxf file was created succesfully
	error		    : boolean  : True when an error has occured
	#               #   	   #

finalFileName.dxf: The final dxf file created by the specifications in info.csv,the name of the file is to be decided in
                   info.csv

errLog.txt: All expected errors will be printed to this file with an error message of what has caused it.
'''
import datetime
import sys
import ezdxf
import os
import csv
import time

'''
Error log
'''


def errLog(errType, errMsg, stopProg, updateStatus):
    with open("errLog.txt", "a") as text_file:
        __ = text_file.write(str(datetime.datetime.now()) + "  |  " + str(errType) + ": " + errMsg + "\n")
    if updateStatus:
        __ = updateStatus(_statusFileName, False, False, True)
    if stopProg:
        sys.exit()
    return True


'''
 Write to status.csv
'''


def updateStatus(statusFileName, working, done, error):
    returnVal = False
    attempts = 0
    maxAttempts = 50
    while (not returnVal) & (attempts < maxAttempts):
        try:
            with open(statusFileName, 'w', newline='') as csvfile:
                sep = ';'
                statusWriter = csv.writer(csvfile, delimiter=sep, quotechar=' ', quoting=csv.QUOTE_MINIMAL)
                statusWriter.writerow(['sep=' + sep])
                statusWriter.writerow(['working', 'done', 'error'])
                statusWriter.writerow([working, done, error])
                returnVal = True
        except PermissionError:
            errType = str(PermissionError)
            returnVal = False
            attempts = attempts + 1
            __ = errLog(errType, " has occured at " + statusFileName + '. Attempt ' + str(attempts), False, False)
            time.sleep(_permWaitTime)
    if not returnVal:
        __ = errLog(errType, " has occured at " + statusFileName + ". Force-stops program after " + str(attempts)
                       + " attempts.", True, False)
    return returnVal


'''
 Removes file from system
'''


def removeFile(fileName):
    returnVal = False
    attempts = 0
    maxAttempts = 50
    while (not returnVal) & (attempts < maxAttempts):
        try:
            returnVal = True
            os.remove(fileName)
        except FileNotFoundError:
            returnVal = True
            errType = str(FileNotFoundError)
            __ = errLog(errType, " File " + fileName + " was not found when trying to delete it.", False, False)
            pass
        except PermissionError:
            returnVal = False
            errType = str(PermissionError)
            __ = errLog(errType,
                        " File " + fileName + " is in use when trying to delete it. Close all programs using it", True,
                        True)
    if not returnVal:
        __ = errLog(errType, " has occured at " + _statusFileName + ". Force-stops program after " + str(attempts)
                    + " attempts.", True, False)
    return returnVal


'''
Get a dxf file
'''


def getDXF(dxfFileName):
    try:
        temp = ezdxf.readfile(dxfFileName)
    except FileNotFoundError:
        __ = errLog(str(FileNotFoundError), " has occured. " + dxfFileName + " were not found", True, True)
    except PermissionError:
        __ = errLog(str(PermissionError), " has occured. Please close all program using " + dxfFileName
               + " before continuing ", True, True)
    return temp


'''
 Setup
'''
_permWaitTime = 0.1
_errType = "No Error"
_statusFileName = 'status.csv'
_infoFileName = "info.csv"
'''
 Update status
'''
status = updateStatus(_statusFileName, True, False, False)
'''
 Read info.csv
'''
with open('info.csv') as csvfile:
    _infoReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in _infoReader:
        _info = row
_info = ', '.join(_info)
_info = _info.replace(',', '')
_info = _info.split(";")
'''
 Deletes the dxf file before saving the new file, also ignores exception FileNotFoundError if file does not exist
'''
_dxfFileName = str(_info[0])  # finalFileName
removeFile(_dxfFileName)
'''
 Get template from file and create the modelspace to add design
'''
_dxfTemplateFileName = str(_info[1])  # templateName
_doc = getDXF(_dxfTemplateFileName)
_msp = _doc.modelspace()
'''
 Add NTNU Manulab logo
'''
_logoFileName = str(_info[2])  # logoFileName
_xInsert = float(_info[3])  # xInsertPointLogo
_yInsert = float(_info[4])  # yInsertPointLogo
_xPixel = int(float(_info[5]))  # xPixelSize
_yPixel = int(float(_info[6]))  # yPixelSize
_xSize = float(_info[7])  # xSizeInmm
_ySize = float(_info[8])  # ySizeInmm
_rotLogo = float(_info[9])  # rotationLogo

_my_image_def = _doc.add_image_def(filename=_logoFileName, size_in_pixel=(_xPixel, _yPixel))
_image = _msp.add_image(image_def=_my_image_def, insert=(_xInsert, _yInsert), size_in_units=(_xSize, _ySize),
                        rotation=_rotLogo)
'''
 Add name text from input
'''
_textFileName = str(_info[10])  # textToInsert
_textStyle = str(_info[11])  # textStyle

_xLoc = float(_info[12])  # xInsertPointText
_yLoc = float(_info[13])  # yInsertPointText
_rotation = float(_info[14])  # rotationText
_alignment = int(float(_info[15]))  # alignmentText
_textWidth = float(_info[16])  # textWidth
_textHeight = float(_info[17])  # textHeight
_strNameLen = int(float(_info[18]))  # strNameLen

_strName = _textFileName.replace('\n', ' ')
_strName = _strName[:_strNameLen]

_mtext = _msp.add_mtext(_strName, dxfattribs={'style': _textStyle}).set_location((_xLoc, _yLoc), _rotation, _alignment)
_mtext.dxf.width = _textWidth
_mtext.dxf.char_height = _textHeight
'''
 Save the new file
'''
_doc.saveas(_dxfFileName)
status = updateStatus(_statusFileName, False, True, False)