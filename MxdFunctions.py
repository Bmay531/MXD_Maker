#-------------------------------------------------------------------------------
# Name:         Mxd Functions
# Purpose:      Functions for Extending 1 DDP.mxd to many
#               Function to calculate field from s1 to s2 based on unit number
#               Function to modify SQL query within label class settings in an DDP Mxd
#               Function alter layer data source settings in an DDP Mxd
#               Function to set locator frame coordinates
#               Function to export a DDP Mxd to PDF
#
# Author:      BMay
#
#-------------------------------------------------------------------------------
# Import Modules
import arcpy, os
from arcpy import env
arcpy.env.overwriteOutput = True

# Test Variables
gdb = "C:\\AC\\Projects\\2017TaxMaps\\source\\AC_Cadastral.gdb"
ws = "C:\\AC\\Projects\\2017TaxMaps\\build"


Ln = "AC_Splits2016"
uname = "Allegan_Twp"
unum = "02"
unumx = "01"
fld = "ExtraText1"
LayerKey = "Index"
string = "_Index"
fc1 = "AC_Splits2016"
fds1 = "AC_Merge"
Calcfld = "InUnit"
s1 = "Y"
s2 = "N"
#mxda = arcpy.mapping.MapDocument("C:\\AC\\Projects\\2017TaxMaps\\build\\01.mxd")
OutPath = "C:\\AC\\Projects\\2017TaxMaps\\buildTest\\TESTp1"

################################################################################
# Define Functions
################################################################################
#Function to calculate field from s1 to s2 based on unit number
################################################################################
def TogTF(gdb,fds1,fc1,Calcfld,unum,s1,s2):
    exp = '''U_Calc(!ExtraText1!)'''
    CB = "def U_Calc(Input):\n\tif Input == '''" + unum + "''':\n\t\tOutput = '''"+ s1 +"'''\n\t\treturn Output\n\telse:\n\t\tOutput = '''" + s2 + "'''\n\t\treturn Output"
    arcpy.env.workspace = gdb
    fds1 = arcpy.ListDatasets(fds1)[0]
    print fds1
    fc1 = arcpy.ListFeatureClasses(fc1,"",fds1)[0]
    print fc1
    arcpy.CalculateField_management(fc1,Calcfld,exp,"PYTHON_9.3",CB)
    pass
if __name__ == '__main__':
    TogTF(gdb,Lx,Calcfld,unum,s1,s2)
################################################################################
# Function to alter layer data source settings in an DDP Mxd
################################################################################
def replaceD_Source(mxd,LayerKey,gdb,uname,string):
    UxString = uname + string
    layer = arcpy.mapping.ListLayers(mxd,LayerKey)
    print layer
    for lyr in layer:
        lyr.replaceDataSource(gdb, "",UxString,False)
    return mxd
    pass
if __name__ == '__main__':
    replaceD_Source(mxd,LayerKey,gdb,uname,string)
################################################################################
# Function to set locator frame coordinates
#   Note: The mxd locator frame must be set to automatic for this to work.
################################################################################
def MxdLocExtent(mxd, xMinVal, yMinVal, xMaxVal, yMaxVal):
    #ddp = mxd.dataDrivenPages
    DfLocator = arcpy.mapping.ListDataFrames(mxd,"")[2]
    print DfLocator
    newExtent = DfLocator.extent
    #print newExtent
    #newExtent = "12743225.06 433126.85 12775281.51 465361.67"

    newExtent.XMin = xMinVal
    newExtent.YMin = yMinVal
    newExtent.XMax = xMaxVal
    newExtent.YMax = yMaxVal
    DfLocator.extent = newExtent
    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()
    return mxd
    pass
if __name__ == '__main__':
    MxdLocExtent(mxd, xMinVal, yMinVal, xMaxVal, yMaxVal)
################################################################################
# Function to export a DDP Mxd to PDF
################################################################################
def MxdExport(mxd, OutPath):
    ddp = mxd.dataDrivenPages
    for pageNum in range(1, ddp.pageCount + 1):
        print "Looping"
        ddp.currentPageID = pageNum
        print "pageNum: \n"
        print pageNum
        ##ddp = mxd.dataDrivenPages
        pageID = ddp.pageRow.HOTLINK
        print "pageID: \n"
        print pageID

        OPath =os.path.join(OutPath,pageID)

        #Special handling of first page
        if pageNum == 1:
            Frame = arcpy.mapping.ListLayoutElements(mxd)[7]
            #DynTxt = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "ParcelPre")[0]
            DfList = arcpy.mapping.ListDataFrames(mxd,"")
            #print DynTxt.text
            #print DfList
            #DfLocator = DfList[2]
            DfLogo = DfList[1]
            #lyrList1 = arcpy.mapping.ListLayers(mxd,"",DfLocator)
            lyrList2 = arcpy.mapping.ListLayers(mxd,"",DfLogo)
            #for lyr in lyrList1:
                #Locator = lyr
                #Locator.visible = False
            for lyr in lyrList2:
                Logo = lyr
                Logo.visible = True

            #DynTxt.visible = False
            arcpy.mapping.ExportToPDF(mxd, OPath)
            #DynTxt.visible = True
            print "Index Printed"
            #Locator.visible = True
            Logo.visible = False
        else:
            pass
            arcpy.mapping.ExportToPDF(mxd, OPath)
            print "page : " + pageID + " printed"
    return mxd
    pass
if __name__ == '__main__':
    MxdExport(mxd,OutPath)


