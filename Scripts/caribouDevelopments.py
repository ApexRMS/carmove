import glob
import os

import operator

from datetime import datetime
from osgeo import ogr
from random import *
import sys
from shapely.geometry import LineString
from shapely.wkt import loads

import projUtil
import caribouConstants as cc


from caribouUtils import createBuffer, mergePolyShapefiles, compressVectorPolygons, createDevIDAttr


def createDevelopments(config):

    initDevFiles(config)

    for iterId in range(config.MinimumIteration, config.MaximumIteration + 1):

        if config.NumNewDev <> 0:
            print("\rCreating New Development Layers. Processing Iteration {0}".format(iterId))
            createProjectedDevPoints(config,iterId)

            createProjectedRoads(config,iterId)

            createProjectedDevBufPtsLayer(config,iterId)

        createZOIDevelopment(config,iterId)

        createMergedHarvestZone(config,iterId)

        # If no devs, then only do this once, as all generated layers will be identical.
        if config.NumNewDev ==0:
            break


###############################################################################################

def initDevFiles(config):
    """
    Clean and Initialize the files that are normally produced by running the methods included in createDevelopments.
    @type config Config
    :return:
    """

    print("\rInitializing Development files...")

    # Delete all the files in the Working directory
    files = glob.glob( os.path.join(config.WorkingDirectory,"*") )
    for f in files:
        try:
            if os.path.isfile(f):
                os.remove(f)
        except OSError as e:
            sys.exit(e)

    # Make sure the Working Directory exists
    if not os.path.isdir(config.WorkingDirectory):
        os.makedirs(config.WorkingDirectory)

    # Make sure the Output Directory exists
    if not os.path.isdir(config.OutputDirectory):
        os.makedirs(config.OutputDirectory)


    # Let reproject all our user input Vector files into a common SRS, so we don't get projection issue when processing

    # Climate
    climateFilename = config.ClimateShapefile
    workClimateFilename = config.getWorkingFilePath(cc.WORKING_CLIMATE_FILENAME)
    projUtil.reprojectShapefile(climateFilename,workClimateFilename,cc.DEFAULT_SRS)

    # Existing Development
    devFilename = config.ExistingDevShapefile
    if devFilename !="":
        workDevFilename = config.getWorkingFilePath(cc.WORKING_EXISTING_DEV_FILENAME)
        projUtil.reprojectShapefile(devFilename,workDevFilename,cc.DEFAULT_SRS)

        # Make sure Dev related vector files has a DEV_ID field - create if not, and set to default
        createDevIDAttr(workDevFilename,config.DefaultDevID)

    # Existing Harvest Zone
    hzFilename = config.HarvestZoneShapeFile
    workHzFilename = config.getWorkingFilePath(cc.WORKING_EXISTING_HARVEST_ZONE_FILENAME)
    projUtil.reprojectShapefile(hzFilename,workHzFilename,cc.DEFAULT_SRS)
    # Make sure Dev related vector files has a DEV_ID field - create if not, and set to default
    createDevIDAttr(workHzFilename, config.DefaultDevID)

    # Existing Road - optional unless Projected
    roadLineFilename = config.ExistingRoadsShapeFile
    if roadLineFilename !="":
        workRdLineFilename = config.getWorkingFilePath(cc.WORKING_EXISTING_ROAD_LINE_FILENAME)
        projUtil.reprojectShapefile(roadLineFilename,workRdLineFilename,cc.DEFAULT_SRS)

        # Generate a polygon layer from the road line, using a 1m buffer
        workRdPolyFilename = config.getWorkingFilePath(cc.WORKING_EXISTING_ROAD_POLY_FILENAME)
        createBuffer(workRdLineFilename,workRdPolyFilename,1)

        # Make sure Dev related vector files has a DEV_ID field - create if not, and set to default
        createDevIDAttr(workRdPolyFilename,config.DefaultDevID)

    # Range Assessment Area - optional unless Projected
    raaFilename = config.RangeAssessmentShapeFile
    if raaFilename != "":
        workRaaFilename = config.getWorkingFilePath(cc.WORKING_RANGE_ASSESSMENT_AREA_FILENAME)
        projUtil.reprojectShapefile(raaFilename, workRaaFilename, cc.DEFAULT_SRS)


def createProjectedDevPoints(config,iterationId,verbose=False):
    """
        Generate a list of random points for Projected Developments

        Parameters:
        :type config Config
        :type iterationId: int - The ID of the iteration we're currently processing
        :type verbose:bool - Set to True for verbose runtime messages

        Notes:
        Buffer the existing development layer by 25km and 50km.  New development points should be x times
        more likely to be selected in the 50K contour and y times more likely in the 25k contour. X and y can be user
        inputs. A point selected within the 25km buffer would be automatically kept, a point selected within the 50km
        buffer would have an x/y probability of being kept and a point selected outside the 50km buffer would have a 1/y
        probability of being kept.  This is not perfect but Don thought it would be a good start as new developments hope
        to take advantage of the existing road network and also tend to aggregate around the mineral deposits that are
        already reflected by existing developments.

    """

    shpdriver = ogr.GetDriverByName('ESRI Shapefile')

    # Support no development shapefile specified, as this is one of the applicable modelling scenarios
    if config.ExistingDevShapefile == "":
        return
    else:
        devFilename = config.getWorkingFilePath(cc.WORKING_EXISTING_DEV_FILENAME)

        devDs = ogr.Open(devFilename)
        devLyr = devDs.GetLayer()
        if devLyr is None:
            sys.exit("Unable to open Existing Development layer {0}".format(devFilename))

        devSRS = devLyr.GetSpatialRef()
        minX, maxX, minY, maxY = devLyr.GetExtent()

        # Create 2 development buffers with specified radius.
        dev25Filename = config.getWorkingFilePath(cc.DEVELOPMENT_NEAR_RADIUS_FILENAME)
        dev50Filename = config.getWorkingFilePath(cc.DEVELOPMENT_FAR_RADIUS_FILENAME)
        # Only bother doing this for iteration 1 ( the 1st time)
        if iterationId ==1:
            createBuffer(devFilename, dev25Filename, config.NearRadiusFromExistingDev * 1000)
            createBuffer(devFilename, dev50Filename, config.FarRadiusFromExistingDev * 1000)

        dev25Ds = ogr.Open(dev25Filename)
        dev25Lyr = dev25Ds.GetLayer()
        if dev25Lyr is None:
            sys.exit("Unable to open Buffered Development layer {0}".format(dev25Filename))

        dev50Ds = ogr.Open(dev50Filename)
        dev50Lyr = dev50Ds.GetLayer()
        if dev50Lyr is None:
            sys.exit("Unable to open Buffered Development layer {0}".format(dev50Filename))


        newDevPtsFilename = cc.NEW_DEV_POINTS_FILENAME.format(iterationId)
        newDevPtsFilename = config.getWorkingFilePath(newDevPtsFilename)

        pointDs = shpdriver.CreateDataSource(newDevPtsFilename)
        # Create a new point layer, using same SRS as Dev layer
        pointLyr = pointDs.CreateLayer(newDevPtsFilename, geom_type=ogr.wkbPoint, srs=devSRS)

        i = 0
        while i < config.NumNewDev:

            # create point geometry
            point = ogr.Geometry(ogr.wkbPoint)
            point.SetPoint(0, minX + (maxX - minX) * random(), minY + (maxY - minY) * random())

            # See if it intersects with the Development Layer
            devLyr.SetSpatialFilter(point)
            if len(devLyr):
                if verbose:
                    print "Point fell within Dev layer, so discarded"
                continue


            # See if it intersects with the Near Raduis Development buffer Layer
            dev25Lyr.SetSpatialFilter(point)
            if len(dev25Lyr):
                if verbose:
                    print "Creating Point because it fell within Near Radius dev buffer"

            else:
                # See if it intersects with the Far Radius Development buffer  Layer
                dev50Lyr.SetSpatialFilter(point)
                if len(dev50Lyr):
                    chance = random()
                    probSuccess = config.RelProbOutsideNearRadius
                    if probSuccess > chance:
                        if verbose:
                            print (
                                "Creating Point because it fell within Far radius dev buffer and probabilistically "
                                "occurred ({0} / {1})".format(chance, probSuccess))
                    else:
                        if verbose:
                            print (
                                "Not creating Point because it fell within Far radius dev buffer but probabilistically "
                                "did "
                                "not "
                                "occur ({"
                                "0}/{1})".format(chance, probSuccess))
                        continue
                else:
                    # Outside the Far radius development buffer
                    # So the probability of creating this point is 1/y
                    chance = random()
                    probSuccess = config.RelProbOutsideFarRadius
                    if probSuccess > chance:
                        if verbose:
                            print (
                                "Creating Point because it fell outside 50km dev buffer and probabilistically occured ({0} "
                                "/ {"
                                "1})".format(chance, probSuccess))
                    else:
                        if verbose:
                            print (
                                "Not creating Point because it fell outside 50km dev buffer but probabilistically did not "
                                "occur ({"
                                "0}/{1})".format(chance, probSuccess))
                        continue


            # Create the feature and set values
            featureDefn = pointLyr.GetLayerDefn()
            outFeature = ogr.Feature(featureDefn)
            outFeature.SetGeometry(point)

            pointLyr.CreateFeature(outFeature)

            i += 1

        devDs = None
        pointDs.Destroy()

        # Add a DEV_ID attribute field to the newly created shapefile
        createDevIDAttr(newDevPtsFilename,config.DefaultDevID)
        print "Created New Projected Development Points Layer {0}".format(newDevPtsFilename)


def createProjectedRoads(config,iterationId):
    """
    :type config: Config
    :type iterationId: int

    Join new developments to existing road network
     	a) for all new developments (centroids or original points) find nearest point on any existing road
     	b) rank all new developments from nearest to farthest from an existing road
     	c) for the new development that is nearest to existing roads, create a new euclidean line segment to connect
 	   that development to the road (this new line segment is now also considered an existing road).
 	    d) repeat a, b & c until all new developments are connected to the road network
    """

    shpdriver = ogr.GetDriverByName('ESRI Shapefile')


    # a) for all new developments (centroids or original points) find nearest point on any existing road
    devPointsFilename = cc.NEW_DEV_POINTS_FILENAME.format(iterationId)
    devPointsFilename = config.getWorkingFilePath(devPointsFilename)

    newPtDs = ogr.Open(devPointsFilename)
    if newPtDs is None:
        sys.exit("Unable to open New Development Points file {0}".format(devPointsFilename))

    newPtLyr = newPtDs.GetLayer()
    if newPtLyr is None:
        sys.exit("Unable to open  New Development Points layer {0}".format(devPointsFilename))

    roadLineFilename = config.getWorkingFilePath(cc.WORKING_EXISTING_ROAD_LINE_FILENAME)
    roadLnDs = ogr.Open(roadLineFilename)
    if roadLnDs is None:
        sys.exit("Unable to open Road Line file {0}".format(roadLineFilename))

    roadLineLyr = roadLnDs.GetLayer()
    if roadLineLyr is None:
        sys.exit("Unable to open Road Line layer {0}".format(roadLineFilename))

    roadLineSrs = roadLineLyr.GetSpatialRef()

    newRoadsLineFilename = cc.NEW_ROADS_LINE_FILENAME.format(iterationId)
    newRoadsLineFilename = config.getWorkingFilePath(newRoadsLineFilename)
    newRoadsDs = shpdriver.CreateDataSource(newRoadsLineFilename)
    newRoadsLyr = newRoadsDs.CreateLayer(newRoadsLineFilename, geom_type=ogr.wkbLineString, srs=roadLineSrs)

    # Copy over all the existing road segments
    for roadIdx in range(0, roadLineLyr.GetFeatureCount()):
        road = roadLineLyr.GetFeature(roadIdx)
        newRoadsLyr.CreateFeature(road)

    pointsToProcess = range(0, newPtLyr.GetFeatureCount())

    while len(pointsToProcess) > 0:
        # Loop thru the remaining points and fetch distance to nearest line
        minDists = {}
        for ptIdx in pointsToProcess:
            pt = newPtLyr.GetFeature(ptIdx)
            # Load Shapely point
            point = loads(pt.GetGeometryRef().ExportToWkt())
            # print point

            minDist = sys.float_info.max
            minDistRoadIdx = 0
            # print("Road segments count:{0}".format(newRoadsLyr.GetFeatureCount()))
            for roadIdx in range(0, newRoadsLyr.GetFeatureCount()):
                road = newRoadsLyr.GetFeature(roadIdx)
                line = loads(road.GetGeometryRef().ExportToWkt())
                distance = point.distance(line)
                if distance < minDist:
                    minDist = distance
                    minDistRoadIdx = roadIdx
                    # print("Distance {0}".format(distance))

            minDists[ptIdx] = [minDist, minDistRoadIdx]
            roadLineLyr.ResetReading()


        # Which point was the closest to existing roads ?
        minPoint = sorted(minDists.items(), key=operator.itemgetter(1))[0]
        minPointIdx = minPoint[0]
        dist, roadIdx = minPoint[1]


        # for ptIdx in range(0,newPtLyr.GetFeatureCount()):
        pt = newPtLyr.GetFeature(minPointIdx)
        point = loads(pt.GetGeometryRef().ExportToWkt())

        roadFeat = newRoadsLyr.GetFeature(roadIdx)
        road = loads(roadFeat.GetGeometryRef().ExportToWkt())
        roadIntersectionPt = road.interpolate(road.project(point))

        # Now create new Lines from Dev Point to Road Intersection
        # http://stackoverflow.com/questions/24415806/coordinate-of-the-closest-point-on-a-line
        newRoad = LineString([(point.x, point.y), (roadIntersectionPt.x, roadIntersectionPt.y)])

        featureDefn = newRoadsLyr.GetLayerDefn()
        outFeature = ogr.Feature(featureDefn)

        g = ogr.CreateGeometryFromWkb(newRoad.wkb)
        outFeature.SetGeometry(g)
        # outFeature.SetField(fieldName, fieldValue)
        newRoadsLyr.CreateFeature(outFeature)

        # Remove processed point from list
        pointsToProcess.remove(minPointIdx)

        # DEVNOTE: TKR - The above code could be more efficient, if it just calculated distance to new line segments,
        # and updated the point/distance/sgement list if applicable. That way we'd only have to process against the
        # existing segment once, and then against the new segments ( much shorter list) for each pass.

    # Close the datasource to save before using below in createBuffer
    newRoadsDs.Destroy()
    print("Created New Roads Line Layer {0}".format(newRoadsLineFilename))

    # Add a DEV_ID attribute field to the newly created shapefile
    createDevIDAttr(newRoadsLineFilename, config.DefaultDevID)

    newRoadsPolyFilename = config.getWorkingFilePath(cc.NEW_ROADS_POLY_FILENAME.format(iterationId))
    createBuffer(newRoadsLineFilename,newRoadsPolyFilename,1 )
    print("Created New Roads Poly (1M) Layer {0}".format(newRoadsPolyFilename))


def createProjectedDevBufPtsLayer(config,iterId):
    """
        Create New Projected Developments Buffered Points Layers - create buffer for new Dev points that is a random
        integer between MIN_DEV_SIZE and MAX_DEV_SIZE

    :type config: Config The iteration ID
    :type iterId: int The iteration ID
    :return:
    """

    # create buffer for new Dev points that is a random integer between MIN_DEV_SIZE and MAX_DEV_SIZE
    inpFilename = cc.NEW_DEV_POINTS_FILENAME.format(iterId)
    inpFilename = config.getWorkingFilePath(inpFilename)
    newDevPtBufFilename = cc.NEW_DEV_POINTS_BUFFERED_FILENAME.format(iterId)
    newDevPtBufFilename = config.getWorkingFilePath(newDevPtBufFilename)
    createBuffer(inpFilename, newDevPtBufFilename, config.MinimumNewDevRadius, config.MaximumNewDevRadius)
    print("Created Projected Development Points Buffered Layer {0}".format(newDevPtBufFilename))



def createMergedHarvestZone(config,iterId):
    """
       Create a new Harvest Zone layer based on the existing base Harvest Zone (composed of Communities, Waterbodies,
       Rivers) + Existing Development + Projected Development we generated

    :type config: Config
    :param iterId: The iteration Id of the Harvest Zone layer we are generating
    :return:

    Note:
        Existing "Harvest Zone" Development Layer created by:
        Buffer infrastructure ( non-Roads, etc) - 5 km
        Buffer navigable water by 2 km & clipped by community 50 km buffer
            bathhurst_rivers_clippedByCommunities
            bathhurst_waterbodies_clippedByCommunities
        Buffer communities by 15 km
            bathhust_placenmame_buffer15

    """

    print("Creating Harvest Zone...")

    if config.HarvestZoneShapeFile == "":
        print("\tNo Harvest Zone file specified")
        return

    shpdriver = ogr.GetDriverByName('ESRI Shapefile')

    existingHZFilename = config.getWorkingFilePath(cc.WORKING_EXISTING_HARVEST_ZONE_FILENAME)
    newHZFilename = config.getWorkingFilePath(cc.NEW_HARVEST_ZONE_FILENAME.format(iterId))
    mergedHZFilename = config.getWorkingFilePath(cc.MERGED_HARVEST_ZONE_FILENAME.format(iterId))
    mergedRoadsDevFilename = config.getWorkingFilePath(cc.MERGED_ROADS_DEV_FILENAME.format(iterId))
    existingDevFilename = config.getWorkingFilePath(cc.WORKING_EXISTING_DEV_FILENAME.format(iterId))


    if config.ExistingDevShapefile == "":

        print "\tNo Development layer specified, so copy existing Harvest Zone"
        hzDs = ogr.Open(existingHZFilename)
        shpdriver.CopyDataSource(hzDs,mergedHZFilename)
        return

    if config.NumNewDev == 0:
        # No new Projected. So we need to merge the existing Dev and the existing Roads ( if specified)
        existingDevFilename = config.getWorkingFilePath(cc.WORKING_EXISTING_DEV_FILENAME.format(iterId))
        existingRoadsPolyFilename = config.getWorkingFilePath(cc.WORKING_EXISTING_ROAD_POLY_FILENAME.format(iterId))
        if os.path.exists(existingRoadsPolyFilename):
            mergePolyShapefiles(existingDevFilename, existingRoadsPolyFilename, mergedRoadsDevFilename)
        else:
            hzDs = ogr.Open(existingDevFilename)
            shpdriver.CopyDataSource(hzDs, mergedRoadsDevFilename)

    else:
        # Merge the new Dev and the new Roads
        mergedNewDevFilename = config.getWorkingFilePath(cc.NEW_DEVELOPMENT_FILENAME.format(iterId))
        newRdPolyFilename = config.getWorkingFilePath(cc.NEW_ROADS_POLY_FILENAME.format(iterId))
        newDevPtBufFilename = config.getWorkingFilePath(cc.NEW_DEV_POINTS_BUFFERED_FILENAME.format(iterId))
        mergePolyShapefiles(newDevPtBufFilename, newRdPolyFilename, mergedNewDevFilename)

        # Merge with existing Dev
        mergePolyShapefiles(mergedNewDevFilename, existingDevFilename, mergedRoadsDevFilename)

    if config.OODevAndRoads:
        # copy & deflate
        destinationFilename = os.path.join(config.OutputDirectory,os.path.basename(mergedRoadsDevFilename))
        # Note that this operation merges spatially but throws away the attributes
        compressVectorPolygons(mergedRoadsDevFilename, destinationFilename)
        print "\tCreated flattened Dev & Roads Layer '{0}'".format(destinationFilename)

    # Buffer the merged Development layer by HARVEST_ZONE_INFRASTRUCTURE_BUFFER_SIZE_M.
    # New file is newHZFilename
    createBuffer(mergedRoadsDevFilename, newHZFilename,config.HarvestZoneBufferWidthRoadsAndDev)

    # Now merge newHZFilename with existing Harvest Zone
    mergePolyShapefiles(existingHZFilename, newHZFilename, mergedHZFilename)

    print "\tCreated Merged Harvest Zone layer '{0}'".format(mergedHZFilename)

    if config.OOHarvestZone:
        # copy & deflate
        destinationFilename = os.path.join(config.OutputDirectory,os.path.basename(mergedHZFilename))
        # Note that this operation merges spatially but throws away the attributes
        compressVectorPolygons(mergedHZFilename, destinationFilename)
        print "\tCreated flattened Harvest Development Layer '{0}'".format(destinationFilename)

def createZOIDevelopment(config,iterId):
    """
       Create a new Zone of Influence (ZOI) Development layer based on the existing Development layer and the new
        Development layer we generated based on Projected dev

    :type config: Config
    :param iterId: The iteration Id of the Harvest Zone layer we are generating
    :return:


    """


    if config.ExistingDevShapefile == "":
        return

    print("Creating Zone of Influence...")

    shpdriver = ogr.GetDriverByName('ESRI Shapefile')

    # Merge the existing Development Layer with the new Development layer
    existingDevFilename = config.getWorkingFilePath(cc.WORKING_EXISTING_DEV_FILENAME)
    newDevFilename = config.getWorkingFilePath(cc.NEW_DEV_POINTS_BUFFERED_FILENAME.format(iterId))
    newRoadsLineFilename = config.getWorkingFilePath(cc.NEW_ROADS_LINE_FILENAME.format(iterId))
    mergedDevFilename = config.getWorkingFilePath(cc.MERGED_DEV_FILENAME.format(iterId))
    zoiDevFilename = config.getWorkingFilePath(cc.ZOI_DEV_FILENAME.format(iterId))


    if config.NumNewDev<>0:

        # Merge the existing Dev with the new Projected Dev.
        mergePolyShapefiles(existingDevFilename, newDevFilename, mergedDevFilename)

    else:
        # Copy the existing Dev .
        shpdriver.CopyDataSource(ogr.Open(existingDevFilename), mergedDevFilename)

        # Copy the existing Roads .
        existingRoads = config.getWorkingFilePath(cc.WORKING_EXISTING_ROAD_LINE_FILENAME)
        if os.path.exists(existingRoads):
            shpdriver.CopyDataSource(ogr.Open(existingRoads),newRoadsLineFilename)


    zoiFilename = config.getWorkingFilePath(cc.ZOI_FILENAME.format(iterId))

    # buffer the Roads, if they were specified
    if os.path.exists(newRoadsLineFilename):
        zoiRoadsFilename = config.getWorkingFilePath(cc.ZOI_ROADS_FILENAME.format(iterId))
        createBuffer(newRoadsLineFilename, zoiRoadsFilename, config.ZOIBufferWidthRoads)

        # buffer the Devs
        createBuffer(mergedDevFilename, zoiDevFilename, config.ZOIBufferWidthDev)

        # Combine for the complete picture
        mergePolyShapefiles(zoiDevFilename, zoiRoadsFilename, zoiFilename)

    else:
        # Just buffer the Devs to get final ZOI
        createBuffer(mergedDevFilename, zoiFilename, config.ZOIBufferWidthDev)

    print "\tCreated ZOI Development Layer '{0}'".format(zoiFilename)

    # Copy to output directory for mapping, if required
    if config.OOZOI:
        # copy & deflate - ONLY for Output
        # Note that this operation merges spatially but throws away the attributes
        destinationFilename = os.path.join(config.OutputDirectory,os.path.basename(zoiFilename))
        compressVectorPolygons(zoiFilename, destinationFilename)
        print "\tCreated flattened ZOI Development Layer '{0}'".format(destinationFilename)

        


