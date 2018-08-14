import os
import syncrosimDb
import config as cc
import sys
import caribouPreprocess as cp

def main(argv):

    if len(argv) < 2:
        sys.exit("The required Syncrosim file name and Scenario ID were not specified as command line arguments")

    syncrosimName = argv[0]
    scenarioId = argv[1]

    print("Running Caribou Movement Model scripts.")
    print "\tLibrary Name:{0}".format(syncrosimName)
    print "\tScenario ID:{0}".format(scenarioId)

    if not os.path.exists(syncrosimName):
        sys.exit("The specified Syncrosim file '{0}' does not exist.".format(syncrosimName))

    db = syncrosimDb.SynrosimDB(syncrosimName)

    config = cc.Config(db, scenarioId)

    cp.preprocess(config)

    config.db.con.close()

pass

if __name__ == '__main__':

    main(sys.argv[1:])