from osgeo import ogr, osr
import os
import sys


def reprojectShapefile(input_shapefile, output_shapefile, output_epsg):
    """
    Reproject a shapefile to the specified SRS

    :param input_shapefile: The name of the source shapefile
    :param output_shapefile: The name of the destination reprojected file
    :param output_epsg: The EPSG Spatial Reference System of the reprojected file
    :return:
    """
    driver = ogr.GetDriverByName('ESRI Shapefile')

    # get the input layer
    inp_ds = driver.Open(input_shapefile)
    if not inp_ds:
        sys.exit("Unable to open Source Shapefile '{0}'".format(input_shapefile))

    inp_layer = inp_ds.GetLayer()
    if not inp_layer:
        sys.exit("Unable to open Source Shapefile Layer '{0}'".format(input_shapefile))

    # input SpatialReference
    inp_spatial_ref = inp_layer.GetSpatialRef()
    print "Reprojecting " + input_shapefile
    # print "inp_spatial_ref:" + inp_spatial_ref.ExportToProj4()

    # Input Geometry Type - Point, Line, Polygon...
    geom_type = inp_layer.GetLayerDefn().GetGeomType()

    # create the output layer
    if os.path.exists(output_shapefile):
        driver.DeleteDataSource(output_shapefile)
    if os.path.exists(output_shapefile):
        sys.exit("Unable to delete existing Output Shapefile '{0}'".format(output_shapefile))

    # create the CoordinateTransformation
    out_spatial_ref = osr.SpatialReference()
    out_spatial_ref.ImportFromEPSG(output_epsg)
    # print "out_spatial_ref:" + out_spatial_ref.ExportToProj4()

    transformation = osr.CoordinateTransformation(inp_spatial_ref, out_spatial_ref)

    out_dataset = driver.CreateDataSource(output_shapefile)
    basename = os.path.splitext(os.path.basename(output_shapefile))[0]
    outLayer = out_dataset.CreateLayer(basename, geom_type=geom_type, srs=out_spatial_ref)

    # add fields
    inLayerDefn = inp_layer.GetLayerDefn()
    for i in range(0, inLayerDefn.GetFieldCount()):
        fieldDefn = inLayerDefn.GetFieldDefn(i)
        outLayer.CreateField(fieldDefn)

    # get the output layer's feature definition
    outLayerDefn = outLayer.GetLayerDefn()

    # loop through the input features
    inFeature = inp_layer.GetNextFeature()
    while inFeature:
        # get the input geometry
        geom = inFeature.GetGeometryRef()
        # reproject the geometry
        geom.Transform(transformation)
        # create a new feature
        outFeature = ogr.Feature(outLayerDefn)
        # set the geometry and attribute
        outFeature.SetGeometry(geom)
        for i in range(0, outLayerDefn.GetFieldCount()):
            outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(), inFeature.GetField(i))
        # add the feature to the shapefile
        outLayer.CreateFeature(outFeature)
        # destroy the features and get the next input feature
        outFeature.Destroy()
        inFeature.Destroy()
        inFeature = inp_layer.GetNextFeature()

    # close the shapefiles
    inp_ds.Destroy()
    out_dataset.Destroy()


def createPrjFile(shpFilename,spatialRef):
    """
        Create a Prj file for the specified layer file.
            @:param shpFilename - The name of the Shapefile that we want to create a Prj file for.
            @:param spatialRef - The SRS of the shapefile.

        DEVNOTE: This function originally added as a way of getting around an issue with Qgis and misinterpretation
        of EPSG:3857. However, this doesnt seem to make any difference. See:
        http://gis.stackexchange.com/questions/112454/qgis-show-gdal-polygonized-file-in-epsg54004-instead-of-epsg3857

    """
    (root, ext) = os.path.splitext(shpFilename)
    prjFilename = root + ".prj"
    if spatialRef is not None:
        spatialRef.MorphToESRI()
        file = open(prjFilename, 'w')
        file.write(spatialRef.ExportToWkt())
        file.close()