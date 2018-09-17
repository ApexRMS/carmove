import sqlite3 as lite
import sys
import os

class SynrosimDB:

    con = None
    filename = ''
    ssim_version = 0
    isValidDB = False
    isValidVersion = False

    def __init__(self,ssimFilename):

        try:
            self.con = lite.connect(ssimFilename)
            self.filename = ssimFilename

            self.con.row_factory = lite.Row

            cur = self.con.cursor()
            cur.execute('SELECT * from SSim_Version')
            data = cur.fetchone()
            self.ssim_version = int(data['SchemaVersion'])
            # Must be at least v36 to have the correct Output/Input file structure, as well as SSim_File(s)->SSim_SysFolder,...
            self.isValidVersion = self.ssim_version >= 36

            # It can be a valid DB even tho its obsolete.
            self.isValidDB = True

        except lite.Error, e:

            print "Error %s:" % e.args[0]




    def getProject(self,projectId):

        self.con.row_factory = lite.Row
        cur = self.con.cursor()
        cur.execute("select * from SSim_Project WHERE ProjectID=?", (projectId,))

        return cur.fetchone()


    def getScenario(self,scenarioId):

        cur = self.con.cursor()
        cur.execute("select * from SSim_Scenario WHERE ScenarioID=?", (scenarioId,))
        return cur.fetchone()



    def getTransitionGroups(self,projectId):

        cur = self.con.cursor()
        sql = "select * from ST_TransitionGroup where ProjectID = ?"

        cur.execute(sql,(projectId,))
        return cur.fetchall()

    def getStockTypes(self,projectId):

        cur = self.con.cursor()
        sql = "select * from SF_StockType where ProjectID = ?"

        cur.execute(sql,(projectId,))
        return cur.fetchall()

    def getFlowTypes(self,projectId):

        cur = self.con.cursor()
        sql = "select * from SF_FlowType where ProjectID = ?"

        cur.execute(sql,(projectId,))
        return cur.fetchall()


    def getProjects(self):

        return self.con.cursor().execute('select * from SSim_Project').fetchall()

    def getScenarios(self):

        cur = self.con.cursor()

        sql = "select s.* from SSim_Scenario s, ST_RunControl r " \
              "where s.ProjectID = r.ProjectID and s.ScenarioID = r.ScenarioID and s.RunStatus > 1 and r.RunSpatially = -1"

        cur.execute(sql)
        return cur.fetchall()

    def getProjectScenarios(self,projectId):

        cur = self.con.cursor()

        sql = "select s.* from SSim_Scenario s, ST_RunControl r " \
              "where s.ProjectID = r.ProjectID and s.ScenarioID = r.ScenarioID and s.RunStatus > 1 and r.RunSpatially = -1 and s.ProjectID=?"

        cur.execute(sql, (projectId,))
        return cur.fetchall()

    def getStateAttributes(self,projectId):
        cur = self.con.cursor()
        sql = "select * from ST_StateAttributeType where ProjectID = ?"

        cur.execute(sql,(projectId,))
        return cur.fetchall()

    def getTransitionAttributes(self,projectId):
        cur = self.con.cursor()
        sql = "select * from ST_TransitionAttributeType where ProjectID = ?"

        cur.execute(sql,(projectId,))
        return cur.fetchall()



    def getFolders(self):

        cur = self.con.cursor()

        sql = "select * from SSim_SysFolder"

        cur.execute(sql)
        return cur.fetchone()


    def getLibraryRoot(self):
        return  os.path.dirname(self.filename)


    def getLibraryName(self):
       return os.path.splitext(os.path.basename(self.filename))[0]


    def getLibraryOutputPath(self):

        libFolders = self.getFolders()
        if libFolders is None:
            return self.filename + '.output'

        outputPath = libFolders['OutputFolderName']
        if outputPath is None:
            # Folder is relative, so figure out absolute path
            outputPath =self.filename + '.output'

        return outputPath

    def getLibraryInputPath(self):

        libFolders = self.getFolders()
        if libFolders is None:
            return self.filename + '.input'

        inputPath = libFolders['InputFolderName']

        if inputPath is None:
            # Folder is relative, so figure out absolute path
            inputPath = self.filename + '.input'

        return inputPath

    def getScenarioInputPath(self,scenarioId):

        return os.path.join(self.getLibraryInputPath(),"Scenario-{0}".format(scenarioId))

    def getScenarioOutputPath(self,scenarioId):
        return os.path.join(self.getLibraryOutputPath(),"Scenario-{0}".format(scenarioId))


    def getScenarioTempPath(self,scenarioId):
        """
            Get the Scenario Temporary Path
        @type scenarioId: int - The ID of the scenario of interest
        @return: The Scenario Temporary Path @rtype: str| unicode
        """
        return os.path.join(self.getLibraryTempPath(),"Scenario-{0}".format(scenarioId))


    def getLibraryTempPath(self):

        libFolders = self.getFolders()
        if libFolders is None:
            return self.filename + '.temp'

        tempPath = libFolders['TempFolderName']
        if tempPath is None:
            # Folder is relative, so figure out absolute path
            tempPath = self.filename + '.temp'

        return tempPath


# Caribou Movement Model specific methods
    def getCMDevelopmentInput(self, scenarioId):

        cur = self.con.cursor()

        sql = "select s.* from CM_DevelopmentInput s where s.ScenarioID = ?"

        cur.execute(sql,(scenarioId,))
        return cur.fetchone()


    def getCMOutputLocation(self, scenarioId):

        cur = self.con.cursor()

        sql = "select s.* from CM_OutputLocation s where s.ScenarioID = ?"

        cur.execute(sql, (scenarioId,))
        return cur.fetchone()


    def getCMRunControl(self, scenarioId):

        cur = self.con.cursor()

        sql = "select s.* from CM_RunControl s where s.ScenarioID = ?"

        cur.execute(sql, (scenarioId,))
        return cur.fetchone()


    def getCMSpatialFiles(self, scenarioId):

        cur = self.con.cursor()

        sql = "select s.* from CM_SpatialFiles s where s.ScenarioID = ?"

        cur.execute(sql, (scenarioId,))
        return cur.fetchone()


    def getCMStrata(self, projectId):
        """
            Get the Caribou Movement Model Strata

        @type projectId: int The Project ID of the Strata definition of interest
        @return: @rtype:
        """

        cur = self.con.cursor()

        sql = """
              select s.StratumID,s.Name,s.ID as StratumId,
              veg.Name, veg.ID as VegID,
              clim.Name, clim.ID as ClimateID,
              dev.Name, dev.ID as DevID
              from CM_Stratum s, CM_StratumLabelX as veg, CM_StratumLabelY as clim,
              CM_StratumLabelZ as dev
              WHERE s.StratumLabelXID = veg.StratumLabelXID
              AND s.StratumLabelYID = clim.StratumLabelYID
              AND s.StratumLabelZID = dev.StratumLabelZID
              AND s.ProjectID = ?
              """

        cur.execute(sql, (projectId,))
        return cur.fetchall()


    def getCMOutputOptions(self, scenarioId):

        cur = self.con.cursor()

        sql = "select s.* from CM_OutputOptions s where s.ScenarioID = ?"

        cur.execute(sql, (scenarioId,))
        return cur.fetchone()


    


    def clearCMOutputLocation(self,scenarioId):

        cur = self.con.cursor()

        sql = """
                delete FROM CM_OutputLocation where ScenarioID=?
                """

        cur.execute(sql, (scenarioId,))


    def insertCMOutputLocation(self,
                         scenarioID,
                         iteration,
                         timestep,
                         julianDay,
                         stratumid,
                         harvestzone,
                         latitude,
                         longitude,
                         outofbounds,
                         distancefromprevious,
                         relationToZOI,
                         rangeAssessmentArea
                         ):
        """
        Insert a location record into the CM_OutputLocation table

        @param scenarioID:
        @type scenarioID: int
        @param iteration:
        @type iteration:  int
        @param timestep:
        @type timestep: int
        @param julianDay:
        @type julianDay: int
        @param stratumid:
        @type stratumid: int
        @param harvestzone:
        @type harvestzone:
        @param latitude:
        @type latitude:
        @param longitude:
        @type longitude:
        @param outofbounds:
        @type outofbounds:
        @param distancefromprevious:
        @type distancefromprevious:
        @param relationToZOI
        @param rangeAssessmentArea
        @return:
        @rtype:
        """


        cur = self.con.cursor()

        sql = """
                insert into CM_OutputLocation (
                    ScenarioID,
                    Iteration,
                    Timestep,
                    JulianDay,
                    StratumID,
                    HarvestZone,
                    Latitude,
                    Longitude,
                    OutOfBounds,
                    DistanceFromPrevious,
                    RelationToZOI,
                    RangeAssessmentArea)
                    VALUES
                    (?,?,?,?,?,?,?,?,?,?,?,?)
        """


        cur.execute(sql, (scenarioID,
                          iteration,
                          timestep,
                          julianDay,
                          stratumid,
                          (-1 if harvestzone == True else 0),
                          latitude,
                          longitude,
                          0 if len(outofbounds)==0 else -1,
                          distancefromprevious,
                          relationToZOI,
                          rangeAssessmentArea
                          ))


    def commit(self):
        self.con.commit()


