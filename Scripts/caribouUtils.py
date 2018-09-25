import os
import shutil
import sys
import tempfile
from random import randint
import datetime

import gdal
import numpy
from osgeo import ogr
import osgeo.osr as osr

import caribouConstants as cc
import projUtil as pu


def createBuffer(inputfn, outputBufferfn, minBufferDist, maxBufferDist=None, field_names = [cc.DEV_LAYER_ATTRIBUTE_NAME,]):
    """
        Create a new Layer by buffering the specified Input layer. If only a minBufferDist
        is specified, then all features are specified by this value, If both a Min and Max value are specified, then
        a random buffer distance in that range is applied to each feature.
        Note: Only those attributes that are listed in field_names are retained - all others are discarded.

    @param inputfn: The file name of the shapefile to be buffered
    @param outputBufferfn: The filename of the output file.
    @param minBufferDist: Minimum Buffer distance.
    @param maxBufferDist: Maximum Buffer distance. If specified, then a random buffer distance between minBufferDist and
    maxBufferDist will be calculated for each feature. If not specified, a fixed value of minBufferDist is used for all features.
    @param field_names: A list of the input fields that we want to copy over the buffered output shapefile
    @return:
    """

    inputds = ogr.Open(inputfn)
    if not inputds:
        sys.exit("Unable to open input file '{0}'".format(inputfn))
    inputlyr = inputds.GetLayer()
    inpSRS = inputlyr.GetSpatialRef()

    shpdriver = ogr.GetDriverByName('ESRI Shapefile')
    if os.path.exists(outputBufferfn):
        shpdriver.DeleteDataSource(outputBufferfn)

    if os.path.exists(outputBufferfn):
        sys.exit("Unable to delete old file '{0}".format(outputBufferfn))

    outputBufferds = shpdriver.CreateDataSource(outputBufferfn)
    bufferlyr = outputBufferds.CreateLayer(outputBufferfn, geom_type=ogr.wkbPolygon, srs=inpSRS)

    featureDefn = bufferlyr.GetLayerDefn()

    # Create field definition(s)
    # Add input Layer Fields to the output Layer if defined in field_names arg.
    inLayerDefn = inputlyr.GetLayerDefn()
    copied_fields = []
    for i in range(0, inLayerDefn.GetFieldCount()):
        fieldDefn = inLayerDefn.GetFieldDefn(i)
        fieldName = fieldDefn.GetName()
        if fieldName not in field_names:
            continue
        bufferlyr.CreateField(fieldDefn)
        fieldDefn = None
        copied_fields.append(fieldName)
        print "\tCreated an Attribute '{0}' in buffer shapefile '{1}'".format(fieldName,outputBufferfn)


    for feature in inputlyr:
        ingeom = feature.GetGeometryRef()

        if maxBufferDist is None:
            geomBuffer = ingeom.Buffer(minBufferDist)
        else:
            geomBuffer = ingeom.Buffer(randint(minBufferDist, maxBufferDist))

        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(geomBuffer)
        for name in copied_fields:
            outFeature.SetField(name, feature.GetField(name))

        bufferlyr.CreateFeature(outFeature)
        outFeature = None

    outputBufferds.Destroy()

    # Create a PRJ file for this shapefile
    pu.createPrjFile(outputBufferfn,inpSRS)


def getVectorLayerAttrVal(lon, lat, lyr_in, fieldName):
    """
    Get the attribute value from a Vector layer at the specified location

    :param lon:  The longitude of location of interest
    :param lat:  The latitude of location of interest
    :param lyr_in:  The layer of interest
    :param fieldName: The name of the Attribute field of interest
    :return: A String containing the attribute value, or NO_DATA_VALUE if Vector doesnt contain location

    Note:
        If the latitude/longitude we're going to use is not in the projection
        of the shapefile, then we will get erroneous results.
        The following assumes that the latitude longitude is in WGS84
        This is identified by the number "4326", as in "EPSG:4326"
        We will create a transformation between this and the shapefile's
        projection, whatever it may be

    """

    # geo_ref = lyr_in.GetSpatialRef()

    #DEVNOTE: I cant seem to get this to work properly unless I explicitly specify a SRS of EPSG:3857. Using
    # lyr_in.GetSpatialRef() doesnt seem to cut it.
    geo_ref = ogr.osr.SpatialReference()
    geo_ref.ImportFromEPSG(cc.DEFAULT_SRS)

    point_ref = ogr.osr.SpatialReference()
    point_ref.ImportFromEPSG(4326)
    ctran = ogr.osr.CoordinateTransformation(point_ref, geo_ref)

    [x, y, z] = ctran.TransformPoint(lon, lat)

    # create point geometry
    pt = ogr.Geometry(ogr.wkbPoint)
    pt.SetPoint_2D(0, x, y)
    lyr_in.SetSpatialFilter(pt)

    idx_reg = lyr_in.GetLayerDefn().GetFieldIndex(fieldName)
    if idx_reg == -1:
        sys.exit("Could not find specified attribute '{0}' in Shapefile".format(fieldName))

    # go over all the polygons in the layer see if one include the point
    if lyr_in.GetFeatureCount() == 0:
        # Nothing found, so return NO_DATA_VALUE
        return cc.NO_DATA_VALUE
    elif lyr_in.GetFeatureCount() ==1:
        for feat_in in lyr_in:
            return feat_in.GetField(fieldName)
    else:
        # Loop thru all check in different values. If so, log warning, and return lowest valule. This could result
        # from overlapping buffers.
        found_values = []
        for feat_in in lyr_in:
            val = feat_in.GetField(fieldName)
            if val not in found_values:
                found_values.append(val)

        if len(found_values) > 1:
            print ("Found overlapping polygons with different values for field '{0}':{1}".format(fieldName,str(found_values)))

        # Return the lower value found
        return min(found_values)




def getVectorLayerContains(lon, lat, lyr_in):
    """
    Get a indicating specifying whether the Vector layer contains the specified location

    :param lon:  The longitude of location of interest
    :param lat:  The latitude of location of interest
    :param lyr_in:  The layer of interest
    :return: A Boolean indicating whether the Vector contains the location

    Note:
        If the latitude/longitude we're going to use is not in the projection
        of the shapefile, then we will get erroneous results.
        The following assumes that the latitude longitude is in WGS84
        This is identified by the number "4326", as in "EPSG:4326"
        We will create a transformation between this and the shapefile's
        projection, whatever it may be

    """

    #DEVNOTE: I cant seem to get this to working properly unless I explicitly specify a SRS of EPSG:3857. Using
    # lyr_in.GetSpatialRef() doesnt seem to cut it.
    geo_ref = ogr.osr.SpatialReference()
    geo_ref.ImportFromEPSG(cc.DEFAULT_SRS)

    point_ref = ogr.osr.SpatialReference()
    point_ref.ImportFromEPSG(4326)
    ctran = ogr.osr.CoordinateTransformation(point_ref, geo_ref)

    [x, y, z] = ctran.TransformPoint(lon, lat)

    # create point geometry
    pt = ogr.Geometry(ogr.wkbPoint)
    pt.SetPoint_2D(0, x, y)
    lyr_in.SetSpatialFilter(pt)

    return len(lyr_in)

def getRasterLayerValue(lon, lat, raster):
    """
        Get the Raster cell value for the specified Latitude / Longitude. If the LL outside bounds of the raster, return NO_DATA_VALUE

        Note: see code in http://trac.osgeo.org/gdal/browser/trunk/gdal/swig/python/samples/val_at_coord.py

    """

    # Build Spatial Reference object based on coordinate system, fetched from the
    # opened dataset
    srs = ogr.osr.SpatialReference()
    srs.ImportFromWkt(raster.GetProjection())

    # DEVTODO: Make the SRS code for this function and the getVectorLayerAttrVal the same (?)
    srsLatLong = srs.CloneGeogCS()
    # Convert from (longitude,latitude) to projected coordinates
    ct = ogr.osr.CoordinateTransformation(srsLatLong, srs)
    (X, Y, height) = ct.TransformPoint(lon, lat)

    # Read geotransform matrix and calculate corresponding pixel coordinates
    geomatrix = raster.GetGeoTransform()
    (success, inv_geometrix) = gdal.InvGeoTransform(geomatrix)
    x = int(inv_geometrix[0] + inv_geometrix[1] * X + inv_geometrix[2] * Y)
    y = int(inv_geometrix[3] + inv_geometrix[4] * X + inv_geometrix[5] * Y)

    if x < 0 or x >= raster.RasterXSize or y < 0 or y >= raster.RasterYSize:
        # Passed coordinates are not in dataset extent
        return cc.NO_DATA_VALUE


    # DEVNOTE: TKR - The following line causes an Process Exit issue: "Process finished with exit code -1073741819 (
    # 0xC0000005)". It does not seem to affect the proper execution of the program, but does cause a "messy" exit. I
    # tried to figure out a solution, but unable to. Some discussion of possible like issues at https://trac.osgeo.org/gdal/wiki/PythonGotchas
    res = raster.GetRasterBand(1).ReadAsArray(x, y, 1, 1)
    val = res[0][0]

    # No Data Value is a Float
    noData = raster.GetRasterBand(1).GetNoDataValue()
    if abs(val - noData) <= sys.float_info.epsilon:
        return cc.NO_DATA_VALUE
    else:
        return val


def mergePolyShapefiles(input1Filename, input2Filename, mergedFilename,field_names = [cc.DEV_LAYER_ATTRIBUTE_NAME,]):
    """
    Merge the two input Polygon shapefiles.

    :param input1Filename: The filename of the 1st source shapefile to merge
    :param input2Filename: The filename of the 2nd source shapefile to merge
    :param mergedFilename: The filename of the resultant merged shapefiles
    :param field_names: A list of Layer fields in the source file(s) that we want to retain in the output. All other fields will be discarded.
    :return:

    Notes: The geometry type and SRS of the input files must be equal.  As well, any attributes not listed in field_names will be discarded.
    Attributes must be defined in both input shapefiles.

    """

    input1Ds = ogr.Open(input1Filename)
    if not input1Ds:
        sys.exit("Unable to open input file '{0}'".format(input1Filename))
    input1lyr = input1Ds.GetLayer()
    inp1SRS = input1lyr.GetSpatialRef()

    input2Ds = ogr.Open(input2Filename)
    if not input2Ds:
        sys.exit("Unable to open input file '{0}'".format(input2Filename))

    input2lyr = input2Ds.GetLayer()
    inp2SRS = input2lyr.GetSpatialRef()

    # Check that files have matching SRS, as we're not reprojecting. Use MorphToESRI to overcome weird issues where
    # parameters are same but just in different positions
    inp1SRS.MorphToESRI()
    inp2SRS.MorphToESRI()
    if inp1SRS.ExportToWkt()<> inp2SRS.ExportToWkt():
        print inp1SRS.ExportToWkt()
        print inp2SRS.ExportToWkt()
        sys.exit("The SRS of the input files '{0}' and '{1}' do not match. Merge cannot be completed.".format(
            input1Filename,input2Filename))

    # DEVTODO: Should check for matching geometry types - them we could generalize this function. For now,
    # only support Polygons

    shpdriver = ogr.GetDriverByName('ESRI Shapefile')
    if os.path.exists(mergedFilename):
        shpdriver.DeleteDataSource(mergedFilename)
    if os.path.exists(mergedFilename):
        sys.exit("Unable to delete existing Shapefile '{0}'".format(mergedFilename))

    outputBufferds = shpdriver.CreateDataSource(mergedFilename)
    outputlyr = outputBufferds.CreateLayer(mergedFilename, geom_type=ogr.wkbPolygon, srs=inp1SRS)

    # Add input Layer Fields to the output Layer if its listed in the field_names list
    inLayerDefn = input1lyr.GetLayerDefn()
    for i in range(0, inLayerDefn.GetFieldCount()):
        fieldDefn = inLayerDefn.GetFieldDefn(i)
        fieldName = fieldDefn.GetName()
        if fieldName not in field_names:
            continue
        outputlyr.CreateField(fieldDefn)
        fieldDefn = None
        print "\tCreated an Attribute '{0}' in merged shapefile '{1}'".format(fieldName,mergedFilename)

    # Get the output Layer's Feature Definition
    outLayerDefn = outputlyr.GetLayerDefn()
    inputLayerDefn = input1lyr.GetLayerDefn()

    # Add features to the ouput Layer
    for i in range(0, input1lyr.GetFeatureCount()):
        # Get the input Feature
        inFeature = input1lyr.GetFeature(i)
        outFeature = ogr.Feature(outLayerDefn)

        # Add specified field values from input Layer
        for i in range(0, inputLayerDefn.GetFieldCount()):
            fieldDefn = inputLayerDefn.GetFieldDefn(i)
            fieldName = fieldDefn.GetName()
            if fieldName not in field_names:
                continue

            outFeature.SetField(fieldName, inFeature.GetField(fieldName))

        outputlyr.CreateFeature(outFeature)

    inputLayerDefn = input2lyr.GetLayerDefn()

    for i in range(0, input2lyr.GetFeatureCount()):
        # Get the input Feature
        inFeature = input2lyr.GetFeature(i)

        outFeature = ogr.Feature(outLayerDefn)

        # Add specified field values from input Layer
        for i in range(0, inputLayerDefn.GetFieldCount()):
            fieldDefn = inputLayerDefn.GetFieldDefn(i)
            fieldName = fieldDefn.GetName()
            if fieldName not in field_names:
                continue

            outFeature.SetField(fieldName, inFeature.GetField(fieldName))

        outputlyr.CreateFeature(outFeature)

    outputBufferds.Destroy()
    # Create prj file
    pu.createPrjFile(mergedFilename,inp1SRS)


def makeLocationPtShapefile(config,locationData):
    """
    Create a New Point Shapefile and Add Location points and attribute data
    :param config - The runtime configuration object
    :param locationData - The numpy array containing the location data, including Lat/Lng.        
    """


    # set up the shapefile driver
    driver = ogr.GetDriverByName("ESRI Shapefile")

    num_iterations = config.TotalIterations
    num_years = config.EndYear
    
    for iteration in range(1, num_iterations + 1):
        for year in range(1, num_years + 1):

            shapeFilename = config.getOutputFilePath(cc.COLLAR_VALUES_SHAPEFILE_FILENAME.format(iteration,year))

            # delete the shapefile if it already exists
            if os.path.exists(shapeFilename):
                driver.DeleteDataSource(shapeFilename)
            if os.path.exists(shapeFilename):
                sys.exit("Unable to delete existing Shapefile '{0}'".format(shapeFilename))

            # create the data source
            data_source = driver.CreateDataSource(shapeFilename)

            # create the spatial reference, WGS84
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(4326)

            # create the layer
            layer = data_source.CreateLayer("location", srs, ogr.wkbPoint)

            # Add the fields we're interested in
            # ITERATION_ID,YEAR_ID,JULIAN_DAY,STRATUM_ID,HARVEST_ZONE,LAT, LON,OUT_OF_BOUNDS,DISTANCE
            # DEVNOTE: Shapefiles seem bound to 10 character limit
            layer.CreateField(ogr.FieldDefn("ITER_ID", ogr.OFTInteger))
            layer.CreateField(ogr.FieldDefn("YEAR_ID", ogr.OFTInteger))
            layer.CreateField(ogr.FieldDefn("JULIAN_DAY", ogr.OFTInteger))
            layer.CreateField(ogr.FieldDefn("STRATUM_ID", ogr.OFTInteger))
            layer.CreateField(ogr.FieldDefn("LAT", ogr.OFTReal))
            layer.CreateField(ogr.FieldDefn("LON", ogr.OFTReal))
            layer.CreateField(ogr.FieldDefn("DIST_KM", ogr.OFTReal))
            layer.CreateField(ogr.FieldDefn("REL_ZOI", ogr.OFTString))
            layer.CreateField(ogr.FieldDefn("RAA", ogr.OFTString))

            # Process the text file and add the attributes and features to the shapefile
            for row in locationData:
                
                # Filter by iteration and timestep
                if row['ITERATION_ID'] == iteration:
                    if  row['YEAR_ID'] == year:
                        # create the feature
                        feature = ogr.Feature(layer.GetLayerDefn())
                        # Set the attributes using the values from the delimited text file
                        feature.SetField("ITER_ID", row['ITERATION_ID'])
                        feature.SetField("YEAR_ID", row['YEAR_ID'])
                        feature.SetField("JULIAN_DAY", row['JULIAN_DAY'])
                        feature.SetField("STRATUM_ID", row['STRATUM_ID'])
                        feature.SetField("LAT", row['LAT'])
                        feature.SetField("LON", row['LON'])
                        feature.SetField("DIST_KM", row['DISTANCE'])
                        feature.SetField("REL_ZOI", row['RELATION_TO_ZOI'])
                        feature.SetField("RAA", row['RANGE_ASSESSMENT_AREA'])

                        # create the WKT for the feature using Python string formatting
                        wkt = "POINT(%f %f)" %  (float(row['LON']) , float(row['LAT']))

                        # Create the point from the Well Known Txt
                        point = ogr.CreateGeometryFromWkt(wkt)

                        # Set the feature geometry using the point
                        feature.SetGeometry(point)
                        # Create the feature in the layer (shapefile)
                        layer.CreateFeature(feature)
                        # Destroy the feature to free resources
                        feature.Destroy()

            # Destroy the data source to free resources
            data_source.Destroy()

            print ("\n\tConverted Collar Points Values into Shapefile for Iteration/Year {0}/{1}. Output file:'{2}'".format(iteration, year, shapeFilename))


def createDevIDAttr(shapefileName, defaultVal):
    """
        Create a DEV_ID Attribute field in the specified Vector file, and initialize with the specified Default value

        :param shapefileName - The name of the shapefile to add the DEV_ID Attribute to
        :param defaultVal - The default value to initialise all existing features to
    """

    inputds = ogr.Open(shapefileName,update=True)
    if not inputds:
        sys.exit("Unable to open input file '{0}'".format(shapefileName))

    inputlyr = inputds.GetLayer()

    # Create field definition(s)
    # Add input Layer Fields to the output Layer if defined in field_names arg.
    inLayerDefn = inputlyr.GetLayerDefn()
    if inLayerDefn.GetFieldIndex(cc.DEV_LAYER_ATTRIBUTE_NAME) == -1:
        print("\tCreating an Attribute '{0}' in vector file '{1}'".format(cc.DEV_LAYER_ATTRIBUTE_NAME,shapefileName))

        inputlyr.CreateField(ogr.FieldDefn(cc.DEV_LAYER_ATTRIBUTE_NAME, ogr.OFTInteger))

        for inFeature in inputlyr:
            inFeature.SetField(cc.DEV_LAYER_ATTRIBUTE_NAME,defaultVal)
            inputlyr.SetFeature(inFeature)

        inputds.Destroy()
        print("\tCreated an Attribute '{0}' in vector file '{1}'".format(cc.DEV_LAYER_ATTRIBUTE_NAME,shapefileName))


def reclassifyVeg(vegInpFilename,vegReclassifiedFilename,vegClassRemapFilename ):
    """
    Reclassify the Vegetation Raster using the Remap CSV file.

    :param vegInpFilename - The absolute path of the vegation input file
    :param vegReclassifiedFilename - The absolute filename of the Reclassified Raster file.
    """

    gdalData = gdal.Open(vegInpFilename)
    if gdalData is None:
        sys.exit("Cannot open veg raster file '%s'" % vegInpFilename)

    raster = gdalData.ReadAsArray()
    x = numpy.array(raster)

    # Import the Veg Class Remap CSV
    remap = numpy.genfromtxt(vegClassRemapFilename, delimiter=',', names=True, dtype=None)
    if remap is None:
        sys.exit("Cannot open veg classification remap file '%s'" % vegClassRemapFilename)

    for old_id, new_id in remap:
        temp = numpy.equal(x, old_id)
        numpy.putmask(raster, temp, new_id)


    # we already have the raster with exact parameters that we need
    # so we use CreateCopy() method instead of Create() to save our time
    rasterFormat = "GTiff"
    driver = gdal.GetDriverByName(rasterFormat)
    outData = driver.CreateCopy(vegReclassifiedFilename, gdalData, 0)
    outData.GetRasterBand(1).WriteArray(raster)

    print ("Done Reclassify Veg. Output file:'%s'" % vegReclassifiedFilename)


def calcApproxDist(lon1, lat1, lon2, lat2):
    """
    Calculate the approximate distance between two points, given their Lat/Lon values
    :param lon1: The Longitude of the 1st point
    :param lat1: The Latitude of the 1st point
    :param lon2: The Longitude of the 2nd point
    :param lat2: The Latitude of the 2nd point
    :return:  The distance in metres between the two points.

    Note: This provides an approximate distance, using  law of cosines. A more accurate value could be calculated
    using projections, but beyond the scope of this project.
    """

    import math
    from shapely.geometry import Point

    point1 = Point(lon1,lat1)
    point2 = Point(lon2, lat2)

    return math.acos(math.sin(math.radians(point1.y))*math.sin(math.radians(point2.y))+math.cos(math.radians(
        point1.y))*math.cos(math.radians(point2.y))*math.cos(math.radians(point2.x)-math.radians(point1.x)))*6371


    
def getRelationToZOI(collarData, pointIdx, lyr_in):
    """
     Classify 2 consecutive daily locations as:
        Outside: Outside of ZOI (2 FALSE days)
        Enter: Entering ZOI (1 FALSE and 1 TRUE day)
        Stay: Stay in ZOI (2 TRUE days)
        Leave: Leaving Zone of Influence (1 TRUE and 1 FALSE day)
        Cross: Crossing Zone of Influence (2 FALSE days)
        N/A: 1st point so calculation no relevant

    :param collarData:  An array of collarData point
    :param pointIdx:  The index to the current point of interest
    :param lyr_in:  The Zone of Influence layer
    :return: A String containing a classification value as described above

    """

    geo_ref = ogr.osr.SpatialReference()
    geo_ref.ImportFromEPSG(cc.DEFAULT_SRS)

    point_ref = ogr.osr.SpatialReference()
    point_ref.ImportFromEPSG(4326)
    ctran = ogr.osr.CoordinateTransformation(point_ref, geo_ref)

    # Can't calculate for the 1st point, as no Previous point to reference
    if pointIdx == 1:
        return 'N/A'

    # Check for changing iteration
    current_cd = collarData[pointIdx-1]
    prev_cd = collarData[pointIdx -2]
    if current_cd['ITERATION_ID'] <> prev_cd['ITERATION_ID']:
        return 'N/A'

    # Manufacture Current Pt Geometry
    [x, y, z] = ctran.TransformPoint(current_cd['LON'], current_cd['LAT'])
    current_pt = ogr.Geometry(ogr.wkbPoint)
    current_pt.SetPoint_2D(0, x, y)

    # Manufacture Previous Pt Geometry
    [x, y, z] = ctran.TransformPoint(prev_cd['LON'], prev_cd['LAT'])
    prev_pt = ogr.Geometry(ogr.wkbPoint)
    prev_pt.SetPoint_2D(0, x, y)

    current_in = False
    prev_in = False

    lyr_in.SetSpatialFilter(current_pt)
    current_in =  len(lyr_in) > 0

    lyr_in.SetSpatialFilter(prev_pt)
    prev_in = len(lyr_in) > 0

    if current_in == True and prev_in==True:
        return 'Stay'

    if current_in == True and prev_in==False:
        return 'Enter'

    if current_in ==False and prev_in==True:
        return 'Leave'

    # Determine whether a line between the 2 points crosses a ZOI
    if current_in ==False and prev_in==False:
        ln = ogr.Geometry(ogr.wkbLineString)
        ln.AddPoint_2D(current_pt.GetX(),current_pt.GetY())
        ln.AddPoint_2D(prev_pt.GetX(),prev_pt.GetY())

        lyr_in.SetSpatialFilter(ln)
        if len(lyr_in) > 0:
            return 'Cross'
        else:
            return 'Outside'

    return 'Unknown Case'





def compressVectorPolygons(srcShapeFilename, destShapeFilename= None):
    '''
    Merge the (multi)polygons in the specified file, performing a UnionCascaded operation. This effectively performs
    a spatial merge, combining overlapping polygons into a single polygon. This reduces the size of the shapefile, sometimes
    quite significantly ( Ex: 37M -> 2.6M). Note that no attributes are copied over, as they are "lost" in the merge. Also note
    that if no destination filename is specified, then the source shapefile layer is replaced by the new "merged" layer
    :param srcShapeFilename: The name of the source shapefile containing the polygons/or multipolygons to merge
    :param destShapeFilename: The name of the destination shapefile containing the merged end product. Is not specified, the srcShapefile will be replaced.
    '''

    # print ("MergeVectorPolygons Start:{}".format(str(datetime.datetime.now())))
    if srcShapeFilename == destShapeFilename:
        sys.exit("Source file and Destination file cannot be the same.")

    if destShapeFilename is None:
        tmp_dir = tempfile.mkdtemp()
        tmp_filename = os.path.join(tmp_dir, "temp.shp")
        __mergeVectorPolygons(srcShapeFilename,tmp_filename)
        # Overwrite original shapefile with new merged one
        renameShapefile(tmp_filename,srcShapeFilename)
        # Delete tmp directory
        shutil.rmtree(tmp_dir)

    else:
        __mergeVectorPolygons(srcShapeFilename,destShapeFilename)

    # print ("MergeVectorPolygons Start:{}".format(str(datetime.datetime.now())))


def __mergeVectorPolygons(srcShapeFilename, destShapeFilename):
    '''
    Merge the (multi)polygons in the specified file, performing a UnionCascaded operation. This effectively performs
    a spatial merge, combining overlapping polygons into a single polygon. This reduces the size of the shapefile, sometimes
    quite significantly ( Ex: 37M -> 2.6M). Note that no attributes are copied over, as they are "lost" in the merge. Also note
    that if no destination filename is specified, then the source shapefile layer is replaced by the new "merged" layer
    :param srcShapeFilename: The name of the source shapefile containing the polygons/or multipolygons to merge
    :param destShapeFilename: The name of the destination shapefile contains the merged end product.
    '''

    from osgeo import ogr

    shpdriver = ogr.GetDriverByName('ESRI Shapefile')

    if not os.path.exists(srcShapeFilename):
        sys.exit("Unable to find the specified source Shapefile '{0}'".format(srcShapeFilename))

    deleteShapefile(destShapeFilename)

    srcShape = ogr.Open(srcShapeFilename,True)
    srcLyr = srcShape.GetLayer()

    # Make sure this is a poly or Multipolygon layer, or nothing to do.
    srcLayerDefinition = srcLyr.GetLayerDefn()
    geomType = srcLayerDefinition.GetGeomType()
    if (geomType != ogr.wkbMultiPolygon and geomType != ogr.wkbPolygon):
        sys.exit('This function only applied to shapefiles containing a Polygon geometry type.')

    unionc = ogr.Geometry(ogr.wkbMultiPolygon)
    for feat in xrange(srcLyr.GetFeatureCount()):
        fit = srcLyr.GetFeature(feat)
        geom = fit.GetGeometryRef()
        if geom.GetGeometryType() == ogr.wkbMultiPolygon:
            for i in range(0, geom.GetGeometryCount()):
                g = geom.GetGeometryRef(i)
                unionc.AddGeometry(g)
        else:
            unionc.AddGeometry(geom)

    union = unionc.UnionCascaded()

    outputDs = shpdriver.CreateDataSource(destShapeFilename)
    outputlyr = outputDs.CreateLayer(destShapeFilename, geom_type=ogr.wkbMultiPolygon, srs=srcLyr.GetSpatialRef())
    if outputlyr is None:
        sys.exit("Output Layer creation failed.")

    featureDefn = outputlyr.GetLayerDefn()

    for geom in union:
        # geom_mp = ogr.ForceToMultiPolygon(geom)
        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(geom)

        outputlyr.CreateFeature(outFeature)

    # Create prj file
    pu.createPrjFile(destShapeFilename,srcLyr.GetSpatialRef())

    srcShape.Destroy()


def deleteShapefile(shpFilename):
    '''
    Delete the specified Shapefile
    :param shpFilename: The name of the shapefile we would like to delete
    :return:
    '''
    shpdriver = ogr.GetDriverByName('ESRI Shapefile')

    if os.path.exists(shpFilename):
        shpdriver.DeleteDataSource(shpFilename)
    if os.path.exists(shpFilename):
        sys.exit("Unable to delete existing Shapefile '{0}'".format(shpFilename))


def renameShapefile(srcFilename, destFilename):
    '''
    Rename the specified shapefile
    :param srcFilename:  The name of the shapefile we would like to rename
    :param destFilename:  The new name of the shapefile

    Note: The rename does an OS rename of the files with shp,dbf,shx,prj extensions
    '''

    srcName =  os.path.splitext(srcFilename)[0]
    destName =  os.path.splitext(destFilename)[0]

    for ext in ['.shp','.dbf','.shx','.prj']:
        if os.path.exists(destName +ext):
            os.remove(destName +ext)

        if os.path.exists(srcName +  ext):
            os.rename(srcName +  ext, destName +ext )


if __name__ == '__main__':

    pass
    # DEVNOTE: Test code
    # renameShapefile('d:\\Temp\\buffer.shp', 'd:\\temp\\tom.shp')
    # compressVectorPolygons('d:/Temp/Sc41-It0001_zone_of_influence.shp','d:/Temp/Sc41-It0001_zone_of_influence_dissolved.shp')
    # compressVectorPolygons('D:/ApexRMS/Raster Simulator A131/Sample Landfire Data/Bathurst-Movement-Model_Syncrosim_1/Bathurst-Movement-Model.ssim.output/Scenario-52/Spatial/It0001_harvest_zone.shp')
    # renameShapefile('d:/Temp/Sc41-It0001_zone_of_influence.shp','d:/Temp/Sc41-It0001_zone_of_influence_dissolved.shp')
