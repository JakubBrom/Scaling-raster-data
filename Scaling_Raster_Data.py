##Raster=group
##Input_raster=raster
##Use_mask=boolean False
##Mask=raster
##Output_raster=output raster

#-------------------------------------------------------------------------------
# Scaling Raster Data
#
# Author: Jakub Brom, University of South Bohemia in Ceske Budejovice,
#		  Faculty of Agriculture 
# Date: 2017-11-24
# Description: Scaling Raster Data is a Python script providing raster
#				scaling according to standard deviation. It is possible
#				scale data under mask.
#
# License: Copyright (C) 2017, Jakub Brom
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------


import gdal
import sys, os
import numpy as np
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException


def readGeo(rast):
	"""
	Function readGeo reads raster and mask files and makes Numpy array with
	the data restricted by the mask.
	Inputs:
	- rast - raster in GDAL readable format
	- mask - raster mask in GDAL readable format. Data should be 8bit integer,
	         typicaly 0 (nodata) and 1 (data). 	
	"""
	
	# raster processing
	ds = gdal.Open(rast)
	gtransf = ds.GetGeoTransform()
	prj = ds.GetProjection() 
	try:
		rast_in = gdal.Dataset.ReadAsArray(ds).astype(np.float32)
		ds = None
	except:
		raise GeoAlgorithmExecutionException('Error reading raster data. File might be too big.')
	
	return rast_in, gtransf, prj


def scalingRaster(rast_in, rast_mask = None):

	# mask processing
	if rast_mask != None:
		dsm = gdal.Open(rast_mask)
		try:
			array_mask = gdal.Dataset.ReadAsArray(dsm).astype(np.int8)
		except:
			raise GeoAlgorithmExecutionException('Error reading raster data. File might be too big.')
		dsm = None
		mask_bool = np.ma.make_mask(array_mask)              # transformation of the mask in to the boolean
	else:
		pass
	
	# statistika
	try:
		if rast_mask != None:
			rast_masked = rast_in[mask_bool]
			rast_sd = np.std(rast_masked, ddof = 1)
			rast_mean = np.mean(rast_masked)
			rast_out = (rast_in - rast_mean)/rast_sd * array_mask
		else:
			rast_sd = np.std(rast_in, ddof = 1)
			rast_mean = np.mean(rast_in)
			rast_out = (rast_in - rast_mean)/rast_sd
	except:
		raise GeoAlgorithmExecutionException('Error statistics calculation.')
		
	return rast_out
	
def outRast(rast_out, gtransf, prj, outFile):                         # prevede interpolovanou vrstvu do GTiff podle souradneho systemu z rastru
	driver = gdal.GetDriverByName("Gtiff")                                                         	# format vystupu
	ds = driver.Create(outFile, rast_out.shape[1],rast_out.shape[0], 1, gdal.GDT_Float32)    									# vytvoreni vystupu
	ds.SetProjection(prj)
	ds.SetGeoTransform(gtransf)
	ds.GetRasterBand(1).WriteArray(rast_out)                                                          # vytvoreni vrstvy vystupu
	ds = None


#-----------------------------------------------------------------------
# Processing of the Scaling Raster Data 
rast_mask = Mask

if Use_mask == False:
    rast_mask = None

rast_in, gtransf, prj = readGeo(Input_raster)
rast_out = scalingRaster(rast_in, rast_mask)
out_file = Output_raster
path_to_folder, in_filename = os.path.split(out_file)
shortname, ext = os.path.splitext(in_filename)
outRast(rast_out, gtransf, prj, out_file)




