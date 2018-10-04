import os
import sys

from caribouUtils import createDevIDAttr

__author__ = 'Tom'



class Config:


    def __init__(self, db, scenarioId):

        self.db = db
        self.scenarioId = scenarioId

        # Lets load up the various runtime parameters needed to run the Movement model script

        dsDevelopmentInput = db.getCMDevelopmentInput(scenarioId)
        if dsDevelopmentInput is None:
            sys.exit("Fatal Error: No Development Inputs values are configured.")

        dsRunControl = db.getCMRunControl(scenarioId)
        if dsRunControl is None:
            sys.exit("Fatal Error: No Run Control values are configured.")

        dsSpatialFiles = db.getCMSpatialFiles(scenarioId)
        if dsSpatialFiles is None:
            sys.exit("Fatal Error: No Spatial Files are configured.")

        dsOutputOptions = db.getCMOutputOptions(scenarioId)

        projectId = db.getScenario(scenarioId)['ProjectId']
        dsStrata = db.getCMStrata(projectId)


        # CM_DevelopmentInput
        self.ZOIBufferWidthDev = dsDevelopmentInput['ZoneOfInfluenceBufferWidthDev']
        self.ZOIBufferWidthRoads = dsDevelopmentInput['ZoneOfInfluenceBufferWidthRoads']
        self.HarvestZoneBufferWidthRoadsAndDev = dsDevelopmentInput['HarvestZoneBufferWidthRoadsAndDev']
        self.NumNewDev = self.ifnull(dsDevelopmentInput['NumNewDev'],0)
        self.MinimumNewDevRadius = dsDevelopmentInput['MinimumNewDevRadius']
        self.MaximumNewDevRadius = dsDevelopmentInput['MaximumNewDevRadius']
        self.NearRadiusFromExistingDev = dsDevelopmentInput['NearRadiusFromExistingDev']
        self.FarRadiusFromExistingDev = dsDevelopmentInput['FarRadiusFromExistingDev']
        self.RelProbOutsideNearRadius = dsDevelopmentInput['RelProbOutsideNearRadius']
        self.RelProbOutsideFarRadius = dsDevelopmentInput['RelProbOutsideFarRadius']

        # CM_RunControl
        self.StartJulianDay = dsRunControl['StartJulianDay']
        self.EndYear = dsRunControl['EndYear']
        self.CalvingPeakJulianDay = dsRunControl['CalvingPeakJulianDay']
        self.MinimumIteration = dsRunControl['MinimumIteration']
        self.MaximumIteration = dsRunControl['MaximumIteration']

        # CM_SpatialFiles
        # Get the Scenario Input directory. All Spatial files are relative to it.
        self.InputDirectory = str(os.path.join(db.getScenarioInputPath(self.scenarioId),"CM_SpatialFiles"))
        self.OutputDirectory = str(os.path.join(db.getScenarioOutputPath(self.scenarioId),"Spatial"))

        self.CollarDataFile = self.getInputFilePath( dsSpatialFiles['CollarDataFile'])
        self.ExistingDevShapefile = self.getInputFilePath( dsSpatialFiles['ExistingStratumLabelZShapeFile'] )
        self.ExistingRoadsShapeFile = self.getInputFilePath( dsSpatialFiles['ExistingRoadsShapeFile'])
        self.VegRaster = self.getInputFilePath( dsSpatialFiles['StratumLabelXRasterFile'] )
        self.ClimateShapefile = self.getInputFilePath( dsSpatialFiles['StratumLabelYShapeFile'] )
        self.HarvestZoneShapeFile = self.getInputFilePath( dsSpatialFiles['HarvestZoneShapeFile'])
        self.RangeAssessmentShapeFile = self.getInputFilePath( dsSpatialFiles['RangeAssessmentAreaShapeFile'])

        # CM_Stratum
        self.Strata = dsStrata

        # CM_OutputOptions
        if dsOutputOptions is not None:
            self.OODevAndRoads = dsOutputOptions['DevAndRoads']
            self.OOZOI = dsOutputOptions['ZoneOfInfluence']
            self.OOHarvestZone = dsOutputOptions['HarvestZone']
        else:
            self.OODevAndRoads = False
            self.OOZOI = False
            self.OOHarvestZone = False

        print("\rUser selected Output Options of {0},{1},{2}".format(self.OODevAndRoads,self.OOHarvestZone, self.OOZOI))


        self.WorkingDirectory = str(os.path.join(db.getLibraryTempPath(),"CM_SpatialFiles"))

        # Do some QA
        # Runtime
        if self.StartJulianDay is None or self.EndYear is None or self.CalvingPeakJulianDay is None or \
                        self.MinimumIteration is None:
            sys.exit("Fatal Error: Run Control missing required field")

        # Development
        if self.NumNewDev >0:
            if self.MinimumNewDevRadius is None\
            or self.MaximumNewDevRadius is None\
            or self.NearRadiusFromExistingDev is None\
            or self.FarRadiusFromExistingDev is None\
            or self.RelProbOutsideNearRadius is None\
            or self.RelProbOutsideFarRadius is None:
                sys.exit('If "Number of New developments" >0, then complete "Development Inputs" are required')

        # Spatial
        if self.CollarDataFile == "":
            sys.exit("Fatal Error: The Collar Data file is required.")

        if self.VegRaster == "":
            sys.exit("Fatal Error:The Vegetation Raster file is required.")

        if self.ClimateShapefile == "":
            sys.exit("Fatal Error:The Climate Shapefile is required.")

        if self.HarvestZoneShapeFile == "":
            sys.exit("Fatal Error: The Harvest Zone Shapefile is required.")

        # QA for Projected ( ie NumNewDev <> 0)
        if self.NumNewDev != 0:
            if self.ExistingRoadsShapeFile == "":
                sys.exit("Fatal Error: The Existing Road Shapefile must be defined if 'NumNewDev' is <>0.")

        # What's the default Development Attribute value ( used when Attribute DEV_ID not defined in Dev or Roads shapefile
        self.DefaultDevID = 99999
        for stratum in self.Strata:
            val = int(stratum['DevID'])
            if val > 0 & val < self.DefaultDevID:
                self.DefaultDevID = val

        return


    def getWorkingFilePath(self,filename):

        if filename is None:
            return ""
        else:
            return os.path.join(self.WorkingDirectory, filename)

    def getInputFilePath(self, filename):

        if filename is None or filename == "":
            return ""
        else:
            return os.path.join(self.InputDirectory, filename)

    def getOutputFilePath(self, filename):

        if filename is None or filename == "":
            return ""
        else:
            return os.path.join(self.OutputDirectory, filename)


    def ifnull(self,var, val):
      if var is None:
        return val
      return var
