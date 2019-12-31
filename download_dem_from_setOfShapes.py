from download_dem import *
import ogr
import  os
import numpy as np
import zipfile
from glob import  glob

shapefilePath = '/Users/sjohnstone/Documents/Research/Projects/IntermountainWest/misc shp/250k_Transect_Quads.shp' #Your shape path here
saveFolder = '/Volumes/DataStorage/DEMData/IMW_DEMs'
nameField = 'QUAD_NAME'

#Use OGR to open shape file
src = ogr.Open(shapefilePath)  # Load in the OGR shapefile object

lyr = src.GetLayer(0)  # Get the top layer from the shapefile

# #test a subset
# featuresToTest = ['Durango', 'Aztec']
# allquads = [ftr.GetField(nameField) for ftr in lyr]
# idcsToTest = []
# for name in featuresToTest:
#     matches = [name == quadname for quadname in allquads]
#     idcsToTest.append(np.where(matches)[0][0])
#
#
# #For each feature in shapefile
# # for i in idcsToTest:
# i = idcsToTest[1]
# #Get feature, and features quad name
# ftr = lyr.GetFeature(i)

for ftr in lyr:
    quadName = ftr.GetField(nameField)

    print('Working on ' + quadName)

    latlon = get_latlonPts_within_feature(ftr)

    #create the path to the directory to save data
    savePath = os.path.join(saveFolder,quadName)

    if not os.path.isdir(savePath):
        #create a folder with the same name as the quad
        os.mkdir(savePath)

    prefix = write_prefix_names(latlon)
    file_path_names = build_file_paths(prefix, kind='.zip')

    retrieve_DEMS_ftp(file_path_names,confirmDownloads=False,saveFolder=savePath)

    #Go through and unzip files
    files = glob( os.path.join(savePath, '*.zip'))
    for file in files:
        newdir = os.path.join(os.path.splitext(file)[0])
        os.mkdir(newdir)

        with zipfile.ZipFile(file,"r") as zip_ref:
            zip_ref.extractall(newdir)

        os.remove(file)
#
src = None