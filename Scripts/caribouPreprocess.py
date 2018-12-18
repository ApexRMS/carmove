# coding=utf-8
"""
Caribou Pre-processing script.

This script performs a number of pre-processing task required to get the raw Caribou spatial and vector data into a
form that can be used by downstream modelling.

"""
import time
import datetime
import csv

from caribouUtils import *
from caribouDevelopments import createDevelopments
import caribouConstants as cc
from caribouUtils import calcApproxDist

def interpolateCollarPoints(config):
    """
    Interpolate the Collar Points CSV file.  This involves creating a new CSV file, which includes new points for the
    days
    that weren't in the original file. The new points LAT/LON location will be interpolated between the two existing
    points.

    @type config: Config

    """

    print "\rInterpolating Collar Points ..."

    # Set up the CSV output writer
    csvOutputfilename = config.getWorkingFilePath(cc.COLLAR_DAILY_CSV_FILENAME)
    csvFile = open(csvOutputfilename, 'w')
    csvWriter = csv.writer(csvFile, lineterminator='\n')
    csvWriter.writerow(['PTT_IDX', 'PTT',
                        'SAMPLE_DATE', 'SAMPLE_DATE_SERIAL', 'PTT_YEAR_IDX', 'JULIAN_DAY',
                        'LAT', 'LON', 'LL_INTERPOLATED',
                        'ORIGINAL_ID'])

    # Import the Collar Points CSV
    csvInputFilename = config.CollarDataFile
    collarData = numpy.genfromtxt(csvInputFilename, delimiter=',', names=True, dtype=None)
    if collarData is None:
        sys.exit("Cannot open collar points file '%s'" % csvInputFilename)

    # Check for required columns in the input CSV file'
    requiredFields = ['PTT', 'YEAR_', 'MONTH_', 'DAY_', 'LAT', 'LON', 'ID']
    inputFields = collarData.dtype.names
    for field in requiredFields:
        if field not in inputFields:
            sys.exit("Input Data file '{0}' missing required field '{1}'".format(csvInputFilename, field))

    uniquePTT = numpy.unique(collarData['PTT'])

    pttIdx = 1
    for ptt in uniquePTT:
        # print("Processing PTT {0}".format(ptt))
        # Get the records for this PTT
        mask = collarData['PTT'] == ptt
        pttCollarData = collarData[mask,]
        # Sort them by Date
        pttCollarData.sort(axis=0, order=['YEAR_', 'MONTH_', 'DAY_'])
        startYear = pttCollarData['YEAR_'][0]

        # Lets see if the 1st point is sufficiently close to the Start of the Year that we can fudge a Jan 1st record
        pointFirst = numpy.copy(pttCollarData[0])
        pointLast = numpy.copy(pttCollarData[len(pttCollarData) - 1])

        sampleDate = datetime.date(pointFirst['YEAR_'], pointFirst['MONTH_'], pointFirst['DAY_'])

        # Check for Date close to specified Start of Year Julian Day
        if sampleDate.timetuple().tm_yday != config.StartJulianDay:

            startofYearDate = datetime.datetime.strptime(str(pointFirst['YEAR_']) + str(config.StartJulianDay), '%Y%j').date()
            if (sampleDate - startofYearDate).days < 0:
                #  Shift the StartofYear by a year earlier
                startofYearDate = datetime.datetime.strptime(str(pointFirst['YEAR_']-1) + str(config.StartJulianDay),
                                                             '%Y%j').date()

            daysDiff = (sampleDate - startofYearDate).days
            if daysDiff < 10 :
                # Prepend another point at the very start
                pttCollarData = numpy.append(pointFirst, pttCollarData)
                pttCollarData[0]['DAY_'] = startofYearDate.timetuple().tm_mday
                pttCollarData[0]['MONTH_'] =startofYearDate.timetuple().tm_mon
                pttCollarData[0]['YEAR_'] = startofYearDate.timetuple().tm_year
                print "Create a new Start point for PTT {2}, because the 1st point @ {1} is within 10 days after Start Year {0} ".format(startofYearDate,sampleDate,pttIdx)

                pttCollarData.sort(axis=0, order=['YEAR_', 'MONTH_', 'DAY_'])

        sampleDate = datetime.date(pointLast['YEAR_'], pointLast['MONTH_'], pointLast['DAY_'])
        # Check for Date close to specified Start of Year Julian Day - 1
        if config.StartJulianDay == 1:
            endOfYearJD = 365
        else:
            endOfYearJD =  config.StartJulianDay -1

        if sampleDate.timetuple().tm_yday != endOfYearJD:

            endofYearDate = datetime.datetime.strptime(str(pointLast['YEAR_']) + str(endOfYearJD), '%Y%j').date()
            if ( endofYearDate - sampleDate).days < 0:
                #  Shift the EndofYear by a year later
                endofYearDate = datetime.datetime.strptime(str(pointLast['YEAR_'] + 1) + str(endOfYearJD),'%Y%j').date()

            daysDiff = ( endofYearDate - sampleDate).days
            if daysDiff  < 10:
                # Append another point
                pttCollarData = numpy.append(pointLast,pttCollarData)
                pttCollarData[0]['DAY_'] = endofYearDate.timetuple().tm_mday
                pttCollarData[0]['MONTH_'] = endofYearDate.timetuple().tm_mon
                pttCollarData[0]['YEAR_'] = endofYearDate.timetuple().tm_year
                print "Create a new End point for PTT {2}, because the Last point @ {1} is within 10 days before End Year {0} ".format(endofYearDate,sampleDate,pttIdx)

                pttCollarData.sort(axis=0, order=['YEAR_', 'MONTH_', 'DAY_'])


        # Now lets step thru the records and pick out Date diffs, so we can interpolate daily locations between
        for i in range(0, len(pttCollarData) - 1):
            pointA = pttCollarData[i]
            pointB = pttCollarData[i + 1]
            dateA = datetime.date(pointA['YEAR_'], pointA['MONTH_'], pointA['DAY_'])
            dateB = datetime.date(pointB['YEAR_'], pointB['MONTH_'], pointB['DAY_'])
            dateDiff = dateB - dateA

            # If the date difference between 2 points is more than a day, we need to create some new points
            latDiff = pointB['LAT'] - pointA['LAT']
            lonDiff = pointB['LON'] - pointA['LON']
            for j in range(0, dateDiff.days):
                newLat = pointA['LAT'] + (latDiff * j) / dateDiff.days
                newLon = pointA['LON'] + (lonDiff * j) / dateDiff.days
                newDate = dateA + datetime.timedelta(days=j)
                yearIdx = newDate.year - startYear + 1
                csvWriter.writerow(
                    [pttIdx, pointA['PTT'], newDate, newDate.toordinal(), yearIdx, newDate.strftime("%j"),
                     newLat,
                     newLon,
                     j > 0,
                     pointA['ID']])

        # Lets lay down the last point for this PTT
        # We're guaranteed to have at least one point, or we wouldnt have got here, but test for case of single point
        if len(pttCollarData) == 1:
            pointA = pttCollarData[0]
        else:
            pointA = pttCollarData[i + 1]

        sampleDate = datetime.date(pointA['YEAR_'], pointA['MONTH_'], pointA['DAY_'])
        yearIdx = pointA['YEAR_'] - startYear + 1
        csvWriter.writerow(
            [pttIdx, pointA['PTT'], sampleDate, sampleDate.toordinal(), yearIdx, sampleDate.strftime("%j"),
             pointA['LAT'],
             pointA['LON'], False,
             pointA['ID']])


        # PTT_IDX needs to be an index starting from 1, without gaps.
        pttIdx += 1

    csvFile.close()

    print ("Done Interpolating Collar Points. Output file:'%s'" % csvOutputfilename)


def loadCMOutputLocation(config,collarData):
    """
        Load the contents of the collarData array into the database CM_OutputLocation table, replacing
        whatever data exists for the current Runtime Scenario

    @type config: Config
    @type collarData:
    @return:
    @rtype:
    """

    db = config.db

    db.clearCMOutputLocation(config.scenarioId)

    for point in collarData:
        db.insertCMOutputLocation(
            config.scenarioId,
            point['ITERATION_ID'],
            point['YEAR_ID'],
            point['JULIAN_DAY'],
            point['STRATUM_ID'],
            point['HARVEST_ZONE'],
            point['LAT'], point['LON'],
            point['OUT_OF_BOUNDS'],
            point['DISTANCE'],
            point['RELATION_TO_ZOI'],
            point['RANGE_ASSESSMENT_AREA']
        )


    db.commit()

def extractCollarPointsValues(config):
    """
    Extract the Collar Points Values for the Veg, Development, Climate layers, and Harvest Zone . The values from Veg,
    Development, Climate layers layers are combined to provide a Stratum ID value.
    """

    from numpy.lib import recfunctions as rfn

    print "\rExtracting Collar Point Values from specified Raster and Vector layers..."

    # startTime = time.time()

    # Import the Collar Points CSV
    inputFilename = config.getWorkingFilePath(cc.SAMPLED_COLLAR_DATA_CSV_FILENAME)
    collarData = numpy.genfromtxt(inputFilename, delimiter=',', names=True, dtype=None)

    collarData = collarData
    if collarData is None:
        sys.exit("Cannot open Collar Points file '%s'" % inputFilename)

    # Check for required columns in the input CSV file, which is the output file from sampleCollarDatum()
    requiredFields = ['ITERATION_ID', 'YEAR_ID', 'JULIAN_DAY', 'LAT', 'LON', 'PTT_IDX', 'YEAR_IDX']

    inputFields = collarData.dtype.names
    for field in requiredFields:
        if field not in inputFields:
            sys.exit("Collar Points Input Data file '{0}' missing required field '{1}'".format(inputFilename, field))

    print "\tProcessing Collar Points Input Data file '{0}'.".format(inputFilename)

    # Add some new columns to hold our processes data
    collarData = rfn.append_fields(collarData,
                                   names=['CLIMATE_VAL', 'DEV_VAL', 'VEG_VAL', 'STRATUM_ID','STRATUM_DESC',
                                          'HARVEST_ZONE', 'OUT_OF_BOUNDS', 'DISTANCE','RELATION_TO_ZOI','RANGE_ASSESSMENT_AREA'],
                                   dtypes=['S50', '<i4', '<i4', '<i4','S50', 'bool', 'S10', 'f8','S50','S20'],
                                   data=[cc.NO_DATA_VALUE, 0, cc.NO_DATA_VALUE, cc.NO_DATA_VALUE, "", False, "",
                                         0.0,"",""],
                                   usemask=False, asrecarray=True)

    # Fill in default values
    collarData['CLIMATE_VAL'] = cc.NO_DATA_VALUE
    collarData['DEV_VAL'] = 0
    collarData['VEG_VAL'] = cc.NO_DATA_VALUE
    collarData['STRATUM_ID'] = cc.NO_DATA_VALUE
    collarData['STRATUM_DESC'] = ""
    collarData['HARVEST_ZONE'] = False
    collarData['OUT_OF_BOUNDS'] = ""
    collarData['DISTANCE'] = 0.0
    collarData['RELATION_TO_ZOI'] = ''
    collarData['RANGE_ASSESSMENT_AREA'] = ''


    drv = ogr.GetDriverByName('ESRI Shapefile')

    # load the Climate Vector
    filename =  config.getWorkingFilePath(cc.WORKING_CLIMATE_FILENAME)
    if not os.path.exists(filename):
        sys.exit('Cannot find Climate Shapefile {0}.'.format(filename))

    # # DEVNOTE: Reproject the Climate shapefile to EPSG:3857, to get around issue in getVectorLayerAttrVal, which only
    # # seems to play nice when input SRS is fixed at 3857. May be the same issue as with Qgis and 3857/54004.
    # reprFile = filename.replace(".shp",".repr.shp")
    # reprojectShapefile(filename,reprFile,3857)

    ds_Climate = drv.Open(filename)
    if ds_Climate is None:
        sys.exit('Cannot open Climate Shapefile %s' % filename)

    climateLayer = ds_Climate.GetLayer()
    if climateLayer is None:
        sys.exit('Climate Shapefile %s doesnt contain expected layer.' % filename)

    if climateLayer.GetLayerDefn().GetFieldIndex(cc.CLIMATE_LAYER_ATTRIBUTE_NAME) == -1:
        sys.exit("Climate Shapefile '{0}' doesn\'t contain the expected attribute {1}.".format(filename,
                                                                                               cc.CLIMATE_LAYER_ATTRIBUTE_NAME))
    print("\tLoaded Climate Shapefile '{0}'".format(filename))

    # load the  Range Assessment Area File, if specified
    raaLayer = None
    if config.RangeAssessmentShapeFile <> '':
        filename = config.getWorkingFilePath(cc.WORKING_RANGE_ASSESSMENT_AREA_FILENAME)
        if not os.path.exists(filename):
            sys.exit('Cannot find Range Assessment Area Shapefile {0}.'.format(filename))

        ds_RAA= drv.Open(filename)
        if ds_RAA is None:
            sys.exit('Cannot open Range Assessment Area  Shapefile %s' % filename)

        raaLayer = ds_RAA.GetLayer()
        if raaLayer is None:
            sys.exit('Range Assessment Area  Shapefile %s doesnt contain expected layer.' % filename)

        if raaLayer.GetLayerDefn().GetFieldIndex(cc.RANGE_ASSESSMENT_AREA_LAYER_ATTRIBUTE_NAME) == -1:
            sys.exit("Range Assessment Area  Shapefile '{0}' doesn\'t contain the expected attribute {1}.".format(filename,
                                                                                                   cc.RANGE_ASSESSMENT_AREA_LAYER_ATTRIBUTE_NAME))
        print("\tLoaded Range Assessment Area Shapefile '{0}'".format(filename))

    # Load the Veg Raster
    filename = config.VegRaster
    ds_Veg = gdal.Open(filename, gdal.GA_ReadOnly)
    if ds_Veg is None:
        sys.exit("Cannot open Vegetation Raster file '{0}'".format(filename))

    print("\tLoaded Vegetation Raster '{0}'".format(filename))

    pointIdx = 0
    lastIteration = 0
    for point in collarData:

        pointIdx += 1

        # Throw out some status message as this is a long running process
        if pointIdx % 200 == 0:
            print "\tProcessed {0} of {1}. {2}".format(pointIdx, len(collarData), time.strftime("%H:%M:%S",
                                                                                              time.localtime()))

        # See if we're into a new iteration. If so, we need to load new Development and Habitat Zone Shapefiles
        if lastIteration != point['ITERATION_ID']:

            if config.NumNewDev == 0 and point['ITERATION_ID'] > config.MinimumIteration: #DEVTODO: Tom please review
                # If we have Num Devs = 0, then we didnt bother generated HZ and Dev layers for other than Iteration 0,
                # so use those layers for all.
                pass
            else:
                iterIdx = point['ITERATION_ID']
                lastIteration = iterIdx


                # Fetch the Harvest Zone Shapefile, to look for presence absence
                hzFilename = config.getWorkingFilePath(cc.MERGED_HARVEST_ZONE_FILENAME.format(iterIdx))
                dsHz = drv.Open(hzFilename)
                if dsHz is None:
                    sys.exit("Could not open Harvest Zone Shapefile '{0}' file".format(hzFilename))

                print("\tLoaded Harvest Zone Shapefile '{0}'".format(hzFilename))

                hzLayer = dsHz.GetLayer()
                if hzLayer is None:
                    sys.exit("Could not open Harvest Zone Shapefile '{0}' layer".format(hzFilename))


                devBufFilename = config.getWorkingFilePath(cc.ZOI_FILENAME.format(iterIdx))

                if config.ExistingDevShapefile != "":

                    ds_Dev = drv.Open(devBufFilename)
                    if ds_Dev is None:
                        sys.exit('Cannot open ZOI Development Shapefile %s' % devBufFilename)

                    devLayer = ds_Dev.GetLayer()
                    if devLayer is None:
                        sys.exit("Could not open ZOI Development Shapefile '{0}' layer")

                    print("\tLoaded  ZOI Development Shapefile '{0}'".format(devBufFilename))

        # Lets see if we have intersection with Climate Shapefile
        climateVal = getVectorLayerAttrVal(point['LON'], point['LAT'], climateLayer, cc.CLIMATE_LAYER_ATTRIBUTE_NAME)
        point['CLIMATE_VAL'] = climateVal

        # Lets see if we have intersection with RAA Shapefile
        if raaLayer is None:
            point['RANGE_ASSESSMENT_AREA'] = cc.NO_DATA_VALUE
        else:
            raaVal = getVectorLayerAttrVal(point['LON'], point['LAT'], raaLayer, cc.RANGE_ASSESSMENT_AREA_LAYER_ATTRIBUTE_NAME)
            point['RANGE_ASSESSMENT_AREA'] = raaVal

        # Lets see if we have intersection with Development Shapefile
        if config.ExistingDevShapefile == "":
            point['DEV_VAL'] = 0
        else:
            # If we dont get a hit, then use a value of 0 ( convention for FALSE state, now that Dev supports Attr values
            val = getVectorLayerAttrVal(point['LON'], point['LAT'], devLayer,cc.DEV_LAYER_ATTRIBUTE_NAME)
            if val == cc.NO_DATA_VALUE:
                point['DEV_VAL'] = 0
            else:
                point['DEV_VAL'] = val

        # Relation To ZOI processing
        relationToZOI = getRelationToZOI(collarData, pointIdx, devLayer)
        point['RELATION_TO_ZOI'] = relationToZOI

        # Lets see if we have intersection with Harvest Zone Shapefile
        # for hzVal we just concerned to with presence/absence.
        hzVal = getVectorLayerContains(point['LON'], point['LAT'], hzLayer)
        point['HARVEST_ZONE'] = hzVal


        # Find the values from the Veg raster
        vegVal = getRasterLayerValue(point['LON'], point['LAT'], ds_Veg)
        point['VEG_VAL'] = vegVal


    # Out of bounds processing
    # Lets flag any record that have out of bound values
    for point in collarData:
        if point['CLIMATE_VAL'] == str(cc.NO_DATA_VALUE):
            point['OUT_OF_BOUNDS'] = cc.CLIMATE_VECTOR_LAYER_NAME
        if point['VEG_VAL'] == cc.NO_DATA_VALUE:
            point['OUT_OF_BOUNDS'] = "Veg"

    # Check that there any out of bounds points to process
    oob = numpy.unique(collarData['OUT_OF_BOUNDS'])
    if len(oob) > 1:
        # Now that we've got all the Layer values, lets look for any missing values ( as in incomplete coverage),
        # and fill in from nearest sample neighbor
        # Start with rare case of the 1st record for a Iteration having Out of Bounds values

        uniqueIterations = numpy.unique(collarData['ITERATION_ID'])

        # Sort them by iteration, year, julian_day
        collarData.sort(axis=0, order=['ITERATION_ID', 'YEAR_ID', 'JULIAN_DAY'])

        # DEVNOTE: I tried to use masks to filter to working on a iteration at a time, but the mask only produces a
        # copy of the source numpy array, so any change wouldnt take. The following loops seem a little bit overly
        # complicated, but works. The ideal mechanism probably would be Panda, but this isn't included in the stock
        # Qgis install, which is our current LCD.
        for iter in uniqueIterations:
            iterIdx = collarData['ITERATION_ID'].tolist().index(iter)

            point1stOfIter = collarData[iterIdx]

            if len(point1stOfIter['OUT_OF_BOUNDS'].strip()) > 0:
                if point1stOfIter['CLIMATE_VAL'] == str(cc.NO_DATA_VALUE):
                    # Get the 1st occurrence of a non-NO_DATA_VALUE for this Iteration
                    vals = collarData[numpy.logical_and(collarData['ITERATION_ID'] == iter, collarData['CLIMATE_VAL'] !=
                                                        str(cc.NO_DATA_VALUE))]
                    if len(vals) > 0:
                        point1stOfIter['CLIMATE_VAL'] = vals[0]['CLIMATE_VAL']
                    else:
                        print "The 1st sample point of Iteration {0} cannot be back-filled with a valid value because no other " \
                              "valid points exist.".format(iter)
                if point1stOfIter['VEG_VAL'] == cc.NO_DATA_VALUE:
                    # Get the 1st occurrence of a non-NO_DATA_VALUE for this PTT
                    vals = collarData[numpy.logical_and(collarData['ITERATION_ID'] == iter, collarData[
                        'VEG_VAL'] != cc.NO_DATA_VALUE)]
                    if len(vals) > 0:
                        point1stOfIter['VEG_VAL'] = vals[0]['VEG_VAL']
                    else:
                        print "The 1st sample point of Iteration {0} cannot be back-filled with a valid value because no other " \
                              "valid points exist.".format(iter)

        #  DEVNOTE: We don't need to do bounds check for Dev, as it doesnt have complete coverage like VEG & Climate


        for iter in uniqueIterations:
            iterList = collarData['ITERATION_ID'].tolist()
            startIdx = iterList.index(iter)

            # Now lets do it again walking thru all the samples for a Iteration and filling from previous sample.
            # Start at 1 instead of 0, so pointPrev doesnt blow up.
            for i in range(startIdx + 1, len(collarData)):
                point = collarData[i]
                pointPrev = collarData[i - 1]

                # Check whether we're gone of the end of the Iteration samples
                if point['ITERATION_ID'] <> pointPrev['ITERATION_ID']:
                    break

                if point['CLIMATE_VAL'] == str(cc.NO_DATA_VALUE):
                    # Use the previous points val, as its going to be legal
                    point['CLIMATE_VAL'] = pointPrev['CLIMATE_VAL']

                if point['VEG_VAL'] == cc.NO_DATA_VALUE:
                    # Use the previous points val, as its going to be legal
                    point['VEG_VAL'] = pointPrev['VEG_VAL']


    # ['CM_StratumID', 'Name', 'StratumId', 'Name', 'VegID', 'Name', 'ClimateID', 'Name', 'DevID']
    stratumMaps = config.Strata

    print("\tCalculating Strata...")
    for i in range(0, len(collarData)):
        point = collarData[i]

        if point['CLIMATE_VAL'] == str(cc.NO_DATA_VALUE) or point['VEG_VAL'] == cc.NO_DATA_VALUE:
            point['STRATUM_ID'] = cc.NO_DATA_VALUE
        else:
            # Cycle thru the stratum map looking for a match
            point['STRATUM_ID'] = cc.NO_DATA_VALUE  # initialize to default value
            for smap in stratumMaps:
                if point['VEG_VAL'] == smap['VegID'] \
                        and point['CLIMATE_VAL'] ==  str(smap['ClimateID']) \
                        and point['DEV_VAL'] == smap['DevID']:
                    point['STRATUM_ID'] = smap['StratumId']
                    point['STRATUM_DESC'] = smap['Name']
                    break


    # Calculate Distance between points
    print("\tCalculating Distance between points...")
    for i in range(1, len(collarData)):
        point = collarData[i]
        prevPoint = collarData[i - 1]

        if point['JULIAN_DAY'] == config.CalvingPeakJulianDay:
            dist = 0.0
        else:
            dist = calcApproxDist(prevPoint['LON'], prevPoint['LAT'], point['LON'], point['LAT'])

        point['DISTANCE'] = dist


    # Write out CSV location file
    outputFilename = config.getWorkingFilePath(cc.COLLAR_VALUES_CSV_FILENAME)
    csvFile = open(outputFilename, 'w')
    csvWriter = csv.writer(csvFile, lineterminator='\n')

    csvWriter.writerow(['ITERATION_ID', 'YEAR_ID', 'JULIAN_DAY','STRATUM_DESC',
                        'CLIMATE_VAL', 'DEV_VAL', 'VEG_VAL', 'STRATUM_VAL',
                        'HARVEST_ZONE',
                        'LAT', 'LON', 'OUT_OF_BOUNDS', 'DISTANCE_KM',
                        'RELATION_TO_ZOI','RANGE_ASSESSMENT_AREA'
                        ])


    for point in collarData:
        csvWriter.writerow([point['ITERATION_ID'],
                            point['YEAR_ID'],
                            point['JULIAN_DAY'],
                            point['STRATUM_DESC'],
                            point['CLIMATE_VAL'], point['DEV_VAL'], point['VEG_VAL'], point['STRATUM_ID'],
                            point['HARVEST_ZONE'],
                            point['LAT'], point['LON'], point['OUT_OF_BOUNDS'], point['DISTANCE'],
                            point['RELATION_TO_ZOI'],
                            point['RANGE_ASSESSMENT_AREA']
        ])

    csvFile.close()

    print ("\tExtracting Collar Points Values complete. Output file:'%s'" % outputFilename)

    #     Pump the collarData array into the database
    loadCMOutputLocation(config,collarData)

    # Convert the collarData array into shapefiles, per iteration per year
    print ("\nConverting Collar Points Values into Shapefiles.")
    makeLocationPtShapefile(config,collarData)



def sampleCollarData(config, verbose=False):
    """
        Refine the movement model to allow for each iteration and year in the model to sample with
        replacement from yearly collar data.  This will allow for us to run a large number of iterations
        (i.e. individual Caribou) across different scenarios. Start each year of movement on a Julian date
        where the cows are most congregated (e.g. peak of calving – Don to provide date)

        Parameters:
            @type config : Config
            @type verbose : bool - (Optional) Do you want verbose processing messages ?

        Notes:
            Only 365 samples per year are output. If a leap year, the 366th sample is discarded.

    """

    print "\rSampling Collar Points ..."

    # Import the Collar Daily Points CSV
    inpFilename = config.getWorkingFilePath(cc.COLLAR_DAILY_CSV_FILENAME)
    collarData = numpy.genfromtxt(inpFilename, delimiter=',', names=True, dtype=None)

    # For debug, use only some subset of points
    # collarData = collarData#[13400:13500]
    if collarData is None:
        sys.exit("Cannot open collar points file '%s'" % inpFilename)

    # Check for required columns in the input CSV file'
    requiredFields = ['PTT_IDX', 'PTT', 'SAMPLE_DATE', 'JULIAN_DAY', 'PTT_YEAR_IDX', 'SAMPLE_DATE_SERIAL', 'LAT', 'LON',
                      'LL_INTERPOLATED', 'ORIGINAL_ID']

    inputFields = collarData.dtype.names
    for field in requiredFields:
        if field not in inputFields:
            sys.exit("Input Data file '{0}' missing required field '{1}'".format(inpFilename, field))

    # Sort it Caribou, Year, Day
    collarData.sort(axis=0, order=['PTT_IDX', 'PTT_YEAR_IDX', 'JULIAN_DAY'])

    # Get a list of unique PTT (Caribou)
    # uniquePTTIdx = numpy.unique(collarData['PTT_IDX'])

    # Write out CSV location file
    outputfilename = config.getWorkingFilePath(cc.SAMPLED_COLLAR_DATA_CSV_FILENAME)
    csvFile = open(outputfilename, 'w')
    csvWriter = csv.writer(csvFile, lineterminator='\n')
    csvWriter.writerow(
        ['ITERATION_ID', 'YEAR_ID', 'JULIAN_DAY', 'LAT', 'LON', 'PTT_IDX', 'YEAR_IDX'])

    if config.SampleRandomCollarYear:
        sampleRandomCollarData(collarData, config, csvWriter, verbose)
    else:
        sampleCompleteCollarData(collarData, config, csvWriter, verbose)

    csvFile.close()

    print ("\tCompleted sampleCollarData(). Created Output file:'%s'" % outputfilename)


def sampleRandomCollarData(collarData, config, csvWriter, verbose):

    # Set up some local variables from the config object
    num_years = config.EndYear
    start_julian_day = config.StartJulianDay
    calving_peak_julian_day = config.CalvingPeakJulianDay

    startDateLead = start_julian_day < calving_peak_julian_day

    # Get a list of unique PTT (Caribou)
    uniquePTTIdx = numpy.unique(collarData['PTT_IDX'])

    # Loop thru the number of iterations specified
    for iteration in range(config.MinimumIteration, config.MaximumIteration + 1):

        calendarYearIdx = 1
        # Loop thru the number of years specified
        for yearIdx in range(1, num_years + 1):

            print ("\tPerforming iteration {0} Year {1}...".format(iteration, yearIdx))

            if yearIdx == 1:

                while True:
                    # Now pick a Caribou at Random from available
                    pttIdx = randint(1, len(uniquePTTIdx))

                    # Get the records for this PTT
                    mask = collarData['PTT_IDX'] == pttIdx
                    pttCollarData = collarData[mask,]
                    uniqueYears = numpy.unique(pttCollarData['PTT_YEAR_IDX'])
                    sampleYearIdx = randint(1, len(uniqueYears))

                    # Use a max 2 year range in case sample aren't contiguous for some reason
                    years = [sampleYearIdx, sampleYearIdx + 1]
                    mask = numpy.in1d(pttCollarData['PTT_YEAR_IDX'], years)
                    sampleYearData = pttCollarData[mask,]
                    sampleYearData.sort(axis=0, order=['PTT_YEAR_IDX', 'JULIAN_DAY'])

                    # We need enough samples to go from Start Day to Calving Day
                    # Even if this sample year isnt complete, we'll give it a break if it starts before  Start Day
                    sampleStartJDay = sampleYearData[0]['JULIAN_DAY']
                    samplesNeeded = 0
                    if sampleStartJDay <= start_julian_day:
                        if startDateLead:
                            samplesNeeded = calving_peak_julian_day - start_julian_day - sampleStartJDay
                        else:
                            samplesNeeded = calving_peak_julian_day - start_julian_day + 366 - sampleStartJDay

                        if len(sampleYearData) >= samplesNeeded:
                            break
                        else:
                            if verbose:
                                print(
                                    "PTT {0} doesnt have enough samples in year {1}, so 'resampling' PTT and Year.".format(
                                        pttIdx, sampleYearIdx))
                    else:
                        if verbose:
                            print(
                                "PTT {0}/year {1} isn't a full year (1st sample date > Calving Peak Date), so can't be used. "
                                "'Resampling' PTT and Year.".format(pttIdx, sampleYearIdx))

                    if verbose:
                        print("Resample:PTT_Idx={5},Year_Idx={6}, start_julian_day={0},calving_peak_julian_day={1},"
                              "sampleStartJDay={2},samplesNeeded = {3},samplesFound={4}".format(start_julian_day,
                                                                                                calving_peak_julian_day,
                                                                                                sampleStartJDay,
                                                                                                samplesNeeded,
                                                                                                len(sampleYearData),
                                                                                                pttIdx, sampleYearIdx))

                if verbose:
                    print(
                        "Success:PTT_Idx={5},Year_Idx={6}, start_julian_day={0},calving_peak_julian_day={1},sampleStartJDay={2},samplesNeeded = {"
                        "3}, samplesFound={4}".format(start_julian_day, calving_peak_julian_day, sampleStartJDay,
                                                      samplesNeeded,
                                                      len(sampleYearData), pttIdx, sampleYearIdx))

                # The 1st set of points will be from Start Date to calving_peak_julian_day
                # This works whether Start Date < or > Season Start Date
                # Find the Start Date in the sampleYearData
                for startIdx in range(0, len(sampleYearData) - 1):
                    sample = sampleYearData[startIdx]
                    if sample['JULIAN_DAY'] >= start_julian_day:
                        break

                # Now that we're at Start Julian Day, write out samples till we get to calving_peak_julian_day ( may wrap
                # through year end)
                for sampleIdx in range(startIdx, len(sampleYearData) - 1):
                    sample = sampleYearData[sampleIdx]
                    if startDateLead:
                        # Start Date < Calving Peak
                        if sample['JULIAN_DAY'] >= calving_peak_julian_day:
                            break
                    else:
                        # Start Date >= Calving Peak
                        if sample['JULIAN_DAY'] >= calving_peak_julian_day and sampleYearIdx != sample['PTT_YEAR_IDX']:
                            break

                    # If we're looping thru Jan 1, increment the year count
                    if start_julian_day > 1 and sample['JULIAN_DAY'] == 1:
                        calendarYearIdx += 1

                    # Write out all sample days from Start Day to Season Start
                    # Write out all sample days from Calving Peak to Start Day
                    # ['ITERATION_ID', 'YEAR_ID', 'JULIAN_DAY','LAT', 'LON','PTT_IDX','YEAR_IDX'])
                    if sample['JULIAN_DAY'] != 366:
                        csvWriter.writerow([
                            iteration,
                            calendarYearIdx,
                            sample['JULIAN_DAY'],  # sample['STRATUM_VAL'],  # hzVal,
                            sample['LAT'], sample['LON'],
                            sample['PTT_IDX'], sample['PTT_YEAR_IDX']
                        ])

            # We're at calving_peak_julian_day. We need a new Year and a new animal, and get samples from
            # calving_peak_julian_day for a year ( or to start_julian_day if last year)
            # Now pick a Caribou at Random from available
            while True:
                pttIdx = randint(1, len(uniquePTTIdx))

                # Get the records for this PTT
                mask = collarData['PTT_IDX'] == pttIdx
                pttCollarData = collarData[mask,]
                uniqueYears = numpy.unique(pttCollarData['PTT_YEAR_IDX'])
                sampleYearIdx = randint(1, len(uniqueYears))

                # Use a max 2 year range in case sample aren't contiguous for some reason
                years = [sampleYearIdx, sampleYearIdx + 1]
                mask = numpy.in1d(pttCollarData['PTT_YEAR_IDX'], years)
                sampleYearData = pttCollarData[mask,]
                sampleYearData.sort(axis=0, order=['PTT_YEAR_IDX', 'JULIAN_DAY'])
                # We need enough samples to go from Calving Day to Calving Day, unless its the last year
                sampleStartJDay = sampleYearData[0]['JULIAN_DAY']
                if sampleStartJDay <= calving_peak_julian_day:
                    if yearIdx != num_years:
                        samplesNeeded = 366 + calving_peak_julian_day - sampleStartJDay
                    else:
                        # Last year, so we're going from calving_peak_julian_day to start_julian_day
                        if startDateLead:
                            samplesNeeded = 366 + start_julian_day - sampleStartJDay
                        else:
                            samplesNeeded = start_julian_day - sampleStartJDay

                    if len(sampleYearData) >= samplesNeeded:
                        break
                    else:
                        if verbose:
                            print(
                                "PTT {0} doesnt have enough samples in year {1}, so 'resampling' PTT and Year.".format(
                                    pttIdx, sampleYearIdx))
                else:
                    if verbose:
                        print(
                            "PTT {0}/year {1} isn't a full year (1st sample date > Calving Peak Date), so can't be used. "
                            "'Resampling' PTT and Year.".format(pttIdx, sampleYearIdx))

                if verbose:
                    print(
                        "Resample:PTT_Idx={5},Year_Idx={6}, start_julian_day={0},calving_peak_julian_day={1},sampleStartJDay={2},samplesNeeded = {"
                        "3}, samplesFound={4}".format(start_julian_day, calving_peak_julian_day, sampleStartJDay,
                                                      samplesNeeded,
                                                      len(sampleYearData), pttIdx, sampleYearIdx))

            if verbose:
                print(
                    "Success:PTT_Idx={5},Year_Idx={6}, start_julian_day={0},calving_peak_julian_day={1},sampleStartJDay={2},samplesNeeded = {"
                    "3}, samplesFound={4}".format(start_julian_day, calving_peak_julian_day, sampleStartJDay,
                                                  samplesNeeded,
                                                  len(sampleYearData), pttIdx, sampleYearIdx))

            # Find the Calving Peak Date in the sampleYearData
            for startIdx in range(0, len(sampleYearData) - 1):
                sample = sampleYearData[startIdx]
                if sample['JULIAN_DAY'] >= calving_peak_julian_day:
                    break

            # Now that we're at Calving Peak, write out samples till we get to
            # Calving Peak again ( or Start Date if last year)
            for sampleIdx in range(startIdx, len(sampleYearData)):
                sample = sampleYearData[sampleIdx]
                if yearIdx == num_years:
                    if startDateLead:
                        # Start Date < Calving Peak
                        if sample['JULIAN_DAY'] >= start_julian_day and sampleYearIdx != sample['PTT_YEAR_IDX']:
                            break
                    else:
                        # Start Date >= Calving Peak
                        if sample['JULIAN_DAY'] >= start_julian_day:
                            break
                else:
                    if sample['JULIAN_DAY'] >= calving_peak_julian_day and sampleYearIdx != sample['PTT_YEAR_IDX']:
                        break

                # If we're looping thru Jan 1, increment the year count
                if sample['JULIAN_DAY'] == 1:
                    calendarYearIdx += 1

                # Write out all sample days from Calving Peak to Start Day
                # ['ITERATION_ID', 'YEAR_ID', 'JULIAN_DAY','LAT', 'LON','PTT_IDX','YEAR_IDX'])
                if sample['JULIAN_DAY'] != 366:
                    csvWriter.writerow([
                        iteration,
                        calendarYearIdx,
                        sample['JULIAN_DAY'],  # sample['STRATUM_VAL'],  # hzVal,
                        sample['LAT'], sample['LON'],
                        sample['PTT_IDX'], sample['PTT_YEAR_IDX']
                    ])


def sampleCompleteCollarData(collarData, config, csvWriter, verbose):

    # Set up some local variables from the config object
    num_years = config.EndYear
    start_julian_day = config.StartJulianDay
    calving_peak_julian_day = config.CalvingPeakJulianDay

    # Get a list of unique PTT (Caribou)
    uniquePTTIdx = numpy.unique(collarData['PTT_IDX'])

    # Loop thru the number of iterations specified
    # for iteration in range(config.MinimumIteration, config.MaximumIteration + 1):
    iteration = config.MinimumIteration
    yearsOutput = 0
    calendarYearIdx = 1

    # Loop thru the number of Caribou (PTT)
    for pttIdx in range(1, len(uniquePTTIdx)):

        # Have we done enough iterations
        if iteration > config.MaximumIteration:
            break

        mask = collarData['PTT_IDX'] == pttIdx
        pttCollarData = collarData[mask,]
        uniqueYears = numpy.unique(pttCollarData['PTT_YEAR_IDX'])

        for sampleYearIdx in range(1, len(uniqueYears)+1):

            # See if we've got as many years as we needed
            if yearsOutput >= num_years:
                yearsOutput = 0
                calendarYearIdx = 1
                iteration +=1
                if iteration > config.MaximumIteration:
                    break


            print ("\tPerforming sample for iteration {0} year {1} ...".format(iteration, yearsOutput+1))

            sampleYear = uniqueYears[sampleYearIdx-1]
            years = [sampleYear, sampleYear+ 1]
            mask = numpy.in1d(pttCollarData['PTT_YEAR_IDX'], years)
            sampleYearData = pttCollarData[mask,]

            # Also throw away the 366th day of any leap years. Do it now to make subsequent checks easier /leapyear tolerant
            mask = numpy.in1d(sampleYearData['JULIAN_DAY'], 366)
            mask = numpy.invert(mask)
            sampleYearData = sampleYearData[mask,]

            sampleYearData.sort(axis=0, order=['PTT_YEAR_IDX', 'JULIAN_DAY'])

            # We need enough samples to go from Start Day to Start Day Next Year
            sampleStartJDay = sampleYearData[0]['JULIAN_DAY']
            numSamples = len(sampleYearData)
            # Do we have at leave a years worth of samples and the 1st sample date is less or equal to the specified Start Day ?
            if numSamples >=365 and sampleStartJDay <= start_julian_day:
                # We're good
                pass
            else:
                # Go try next year
                if sampleYearIdx == 1:
                    # Only give year 1 as break, subsequent years should be complete
                    if verbose:
                        print(
                            "\t\tPTT {0} doesnt have enough samples in year {1}, so we'll take a stab at next year.".format(
                                pttIdx, sampleYearIdx))
                    continue
                else:
                    if verbose:
                        print("\t\tPTT {0} ran out of samples in year {1}.".format(pttIdx, sampleYearIdx))
                    break

            # Find the Start Date in the sampleYearData
            for startIdx in range(0, numSamples):
                sample = sampleYearData[startIdx]
                if sample['JULIAN_DAY'] >= start_julian_day:
                    break

            # Now that we're at Start Day, write out samples for a year
            if verbose:
                print("\t\tSampling from PTT {0} year {1} for Iteration {2} Year {3}.".format(pttIdx, sampleYearIdx,
                                                                                              iteration, yearsOutput+1))

            for sampleIdx in range(startIdx, len(sampleYearData)):
                sample = sampleYearData[sampleIdx]

                # Wrapped around a year and come back to the Start Day ?
                if sample['JULIAN_DAY'] >= start_julian_day and sampleYearIdx != sample['PTT_YEAR_IDX']:
                    break

                # If we're looping thru Jan 1, increment the year count
                if start_julian_day > 1 and sample['JULIAN_DAY'] == 1:
                    calendarYearIdx += 1

                # Write out all sample days from Start Day to Season Start
                # ['ITERATION_ID', 'YEAR_ID', 'JULIAN_DAY','LAT', 'LON','PTT_IDX','YEAR_IDX'])
                csvWriter.writerow([
                    iteration,
                    calendarYearIdx,
                    sample['JULIAN_DAY'],
                    sample['LAT'], sample['LON'],
                    sample['PTT_IDX'], sample['PTT_YEAR_IDX']
                ])

            yearsOutput+=1

    if iteration <= config.MaximumIteration:
        if verbose:
            print "We must have run out of PTT Sample Years for the specified number of Iterations/Num Years"



def preprocess(config):
    startTime = time.time()

    if not os.path.isdir(config.InputDirectory):
        sys.exit("The specified Scenario Input directory {0} does not exist.".format(config.InputDirectory))

    createDevelopments(config)
    interpolateCollarPoints(config)
    sampleCollarData(config)
    extractCollarPointsValues(config)

    print ("\rElapsed time: %f" % (time.time() - startTime))

