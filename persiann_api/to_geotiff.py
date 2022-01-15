"Transform .bin.gz into .tiff files from the PERSIANN database."

# data wrangling
import numpy as np

# geo data processing
from osgeo import gdal
from osgeo import osr

# utils
from struct import unpack
import gzip
import shutil


def unpack_gz(input_file, output_file):
    with gzip.open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def bin_to_geotiff(BinaryFile, OutputFile):
    # open binary file
    f = open(BinaryFile, 'rb')
    # set file dimensions
    xs = 1440 # 180 / 0.25 (our resolution for longitude)
    ys = 480 # 60 / 0.25  (our resolution for latitude)
    # set number of bytes in file
    NumbytesFile = xs * ys
    # number of columns in row
    NumElementxRecord = -xs
    # create empty array to put data in
    myarr = []
    # loop trough the binary file row by row
    for PositionByte in range(NumbytesFile,0, NumElementxRecord):
    
            Record = ''
    
            # the dataset starts at 0 degrees, use 720 to convert to -180 degrees
            for c in range (PositionByte-720, PositionByte, 1):
                    f.seek(c * 4)
                    DataElement = unpack('>f', f.read(4))
                    Record = Record  + str("%.2f" % DataElement + ' ')
            
            # 0 - 180 degrees
            for c in range (PositionByte-1440 , PositionByte-720, 1):
                    f.seek(c * 4)
                    DataElement = unpack('>f', f.read(4))
                    Record = Record  + str("%.2f" % DataElement + ' ')
    
            # add data to array
            myarr.append(Record[:-1].split(" "))
    
    # close binary file
    f.close()
    # Array to numpy float
    myarr = np.array(myarr).astype('float')
    # mirror array
    myarr = myarr[::-1]
    # set values some values to non data
    myarr[myarr < 0] = 0
    myarr[np.isnan(myarr)] = 0
    # set coordinates
    originy = -60
    originx  = -180
    pixelsize = 0.25
    transform= (originx, pixelsize, 0.0, originy, 0.0, -pixelsize)
    driver = gdal.GetDriverByName( 'GTiff' )
    # set projection
    target = osr.SpatialReference()
    target.ImportFromEPSG(4326)
    ## write dataset to disk
    outputDataset = driver.Create(OutputFile, xs,ys, 1,gdal.GDT_Float32)
    outputDataset.SetGeoTransform(transform)
    outputDataset.SetProjection(target.ExportToWkt())
    outputDataset.GetRasterBand(1).WriteArray(myarr)
    outputDataset.GetRasterBand(1).SetNoDataValue(0)
    outputDataset = None


def gz_to_geotiff(gzFile:str, GeoTiffFile:str=None):
        binfile = gzFile[:-3]
        unpack_gz(gzFile, binfile)
        if GeoTiffFile is None:
                GeoTiffFile = binfile[:-3] + 'tiff'
        bin_to_geotiff(binfile, GeoTiffFile)

