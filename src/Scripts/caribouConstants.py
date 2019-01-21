# Constant for the caribouPreprocess script. The value of these constant shouldn't typically need to be changed, after
# the initial file structure has been implemented. caribouCfg.py contains constants that would be more typically
# tweaked from one "run" to next, during a modelling exercise.

# Collar Points - Daily values. This should be the output of interpolateCollarPoints, where points for missing days
# are added
COLLAR_DAILY_CSV_FILENAME = 'collar_daily.csv'

# Final Collar Points Daily with Stratum ID and Harvest Zone
COLLAR_VALUES_CSV_FILENAME = 'location.csv'

# Final Collar Points Daily Shapefile
COLLAR_VALUES_SHAPEFILE_FILENAME = "It{0:04d}_Ts{1:04d}_location.shp"

# Movement Model Export file. This should be the export of sampleCollarData()
SAMPLED_COLLAR_DATA_CSV_FILENAME = 'sampledCollarData.csv'

# Climate Shapefile
CLIMATE_VECTOR_LAYER_NAME = "Climate"
CLIMATE_LAYER_ATTRIBUTE_NAME = "Zone_id"

# Range Assessment Area (RAA)  Shapefile
RANGE_ASSESSMENT_AREA_LAYER_ATTRIBUTE_NAME = "RAA"

# Development Shapefile
DEV_LAYER_ATTRIBUTE_NAME = "DEV_ID"

# Name of Working version of User specified files
WORKING_CLIMATE_FILENAME = "climate.shp"
WORKING_RANGE_ASSESSMENT_AREA_FILENAME = "raa.shp"
WORKING_EXISTING_DEV_FILENAME = "existing_dev.shp"
WORKING_EXISTING_HARVEST_ZONE_FILENAME = "existing_harvest_zone.shp"
WORKING_EXISTING_ROAD_LINE_FILENAME = "existing_road_line.shp"
WORKING_EXISTING_ROAD_POLY_FILENAME = "existing_road_poly.shp"

# Zone of Influence (ZOI) Shapefile
# The name of the development shapefile which has been buffered by the Zone of Influence value.
ZOI_FILENAME = "It{0:04d}_zoi.shp"

ZOI_DEV_FILENAME = "It{0:04d}_zoi_dev.shp"
ZOI_ROADS_FILENAME = "It{0:04d}_zoi_road.shp"

# The NO_DATA_VALUE used in the raster file, and for processing within extractCollarPointValues()
NO_DATA_VALUE = -9999

# New Buffered Developments Shapefiles
DEVELOPMENT_FAR_RADIUS_FILENAME = "dev_far_radius.shp"
DEVELOPMENT_NEAR_RADIUS_FILENAME = "dev_near_radius.shp"

# New Development Points Output Shapefile
NEW_DEV_POINTS_FILENAME = "It{0:04d}_new_dev_points.shp"
# New Development Points Buffered Output Shapefile
NEW_DEV_POINTS_BUFFERED_FILENAME = "It{0:04d}_new_dev_points_buffer.shp"

# New Development Roads Output Shapefile
NEW_ROADS_LINE_FILENAME = "It{0:04d}_new_dev_roads_line.shp"
# New Development Roads Buffered 1M Output Shapefile
NEW_ROADS_POLY_FILENAME = "It{0:04d}_new_dev_roads_poly1m.shp"

# New Development (Merged Points and Roads) Output Shapefile
NEW_DEVELOPMENT_FILENAME = "It{0:04d}_new_dev.shp"

# New + Existing Development Output Shapefile
MERGED_DEV_FILENAME = "It{0:04d}_merged_dev.shp"

# New Dev + Roads + Existing Development Output Shapefile
MERGED_ROADS_DEV_FILENAME = "It{0:04d}_roads_dev.shp"

# New Harvest Zone ( due to New Development ) Output Shapefile
NEW_HARVEST_ZONE_FILENAME = "It{0:04d}_new_harvest_zone.shp"

# Merged Harvest Zone ( Merged Existing Harvest Zone + Development) Output Shapefile
MERGED_HARVEST_ZONE_FILENAME = "It{0:04d}_harvest_zone.shp"

# The default Spatial Reference System used by this script. Where necessary Vectors will be reprojected to this SRS
# before processing starts. Note that Qgis sometime misinterprets EPSG:3857 as EPSG:54004, so this correction must be
#  made manually in the layer properties dialog.
DEFAULT_SRS = 26912  # EPSG:26912  = NAD83 / UTM zone 12N
