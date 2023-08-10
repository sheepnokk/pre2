import pandas as pd
import geopandas as gpd
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import osgeo.ogr as ogr
import numpy as np
import osgeo.gdal as gdal
import glob
import matplotlib.pyplot as plt


def get_point():
    csv_file = "app/flood2.csv"
    df = pd.read_csv(csv_file)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df["the_geom"]))
    gdf.crs = "EPSG:4326"
    output_dir = "app\point_tif2"
    os.makedirs(output_dir, exist_ok=True)

    for idx, row in gdf.iterrows():
        single_gdf = gpd.GeoDataFrame([row], crs=gdf.crs, geometry="geometry")
        wkt = row["geometry"].wkt
        output_shapefile = f"{output_dir}/{idx}_geom_with_wkt.shp"
        single_gdf.to_file(output_shapefile)
        with open(f"{output_dir}/{idx}_wkt.txt", "w") as wkt_file:
            wkt_file.write(wkt)

    print("Separate Shapefiles and WKT files saved successfully.")


get_point()


def get_rainfall_from_points():
    # ให้ใส่ไฟล์ .shp และ .tif เข้าไปใน โฟลเดอร์ point_tif
    shapefile_paths = glob.glob("app/point_tif2/*.shp")

    rainfall_values = []

    for shapefile_path in shapefile_paths:
        driver = ogr.GetDriverByName("ESRI Shapefile")
        dataset = driver.Open(shapefile_path)
        layer = dataset.GetLayer()

        rasterfile_path = glob.glob("app/point_tif2/*.tif")[0]

        raster = gdal.Open(rasterfile_path)
        band = raster.GetRasterBand(1)

        for feature in layer:
            geom = feature.GetGeometryRef()
            x = geom.GetX()
            y = geom.GetY()

            transform = raster.GetGeoTransform()
            col = int((x - transform[0]) / transform[1])
            row = int((y - transform[3]) / transform[5])

            value = band.ReadAsArray(col, row, 1, 1)[0][0]
            rainfall_values.append(value)

        dataset = None
        raster = None

    return rainfall_values


# get_rainfall_from_points()


def get_file_name(dir_path):
    for file_path in os.listdir(dir_path):
        if file_path.endswith(".tif"):
            name_date = file_path.split(".")[0]
            return name_date


def get_point():
    csv_file = "app/flood2.csv"
    df = pd.read_csv(csv_file)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df["the_geom"]))
    gdf.crs = "EPSG:4326"
    output_dir = "app/point_tif2"
    os.makedirs(output_dir, exist_ok=True)

    for idx, row in gdf.iterrows():
        single_gdf = gpd.GeoDataFrame([row], crs=gdf.crs, geometry="geometry")
        wkt = row["geometry"].wkt
        output_shapefile = f"{output_dir}/{idx}_geom_with_wkt.shp"
        single_gdf.to_file(output_shapefile)
        with open(f"{output_dir}/{idx}_wkt.txt", "w") as wkt_file:
            wkt_file.write(wkt)

    print("Separate Shapefiles and WKT files saved successfully.")


get_point()


def get_rainfall_from_points():
    # ให้ใส่ไฟล์ .shp และ .tif เข้าไปใน โฟลเดอร์ point_tif
    shapefile_paths = glob.glob("app/point_tif2/*.shp")

    rainfall_values = []

    for shapefile_path in shapefile_paths:
        driver = ogr.GetDriverByName("ESRI Shapefile")
        dataset = driver.Open(shapefile_path)
        layer = dataset.GetLayer()

        rasterfile_path = glob.glob("app/point_tif2/*.tif")[0]

        raster = gdal.Open(rasterfile_path)
        band = raster.GetRasterBand(1)

        for feature in layer:
            geom = feature.GetGeometryRef()
            x = geom.GetX()
            y = geom.GetY()

            transform = raster.GetGeoTransform()
            col = int((x - transform[0]) / transform[1])
            row = int((y - transform[3]) / transform[5])

            value = band.ReadAsArray(col, row, 1, 1)[0][0]
            rainfall_values.append(value)

        dataset = None
        raster = None

    return rainfall_values


get_rainfall_from_points()


def get_file_name(dir_path):
    for file_path in os.listdir(dir_path):
        if file_path.endswith(".tif"):
            name_date = file_path.split(".")[0]
            return name_date


def prediction_flood_levels(new_rainfalls):
    dir_path = "app/point_tif2"
    data = pd.read_csv("app/modified_file2234.csv")

    x = data[["rain"]]
    y = data["flood_L"]

    model = RandomForestRegressor()
    model.fit(x, y)

    new_flood_levels = model.predict(np.array(new_rainfalls).reshape(-1, 1))
    new_flood_levels = np.round(new_flood_levels, 2)

    df = pd.read_csv("app/flood2.csv")
    specific_column = df["case_id"]

    for i, new_flood_level in enumerate(new_flood_levels):
        new_rainfall = new_rainfalls[i]
        print(
            "Predicted flood level for",
            new_rainfall,
            "millimeters of rainfall:",
            new_flood_level,
            "centimeters",
        )

        # CSV file
        new_prediction = pd.DataFrame(
            {
                "case_id": specific_column[i],
                "rain for the next 7 days(mm)": [new_rainfall],
                "prediction of flood level for the next 7 days(cm)": [new_flood_level],
            }
        )
        name_date = get_file_name(dir_path)
        prediction_file = "คาดการณ์ระดับน้ำ_" + name_date + ".csv"

        if os.path.exists(prediction_file):
            new_prediction.to_csv(prediction_file, mode="a", header=False, index=False)
        else:
            new_prediction.to_csv(prediction_file, mode="a", header=True, index=False)

        # R^2
        y_pred = model.predict(x)
        r2 = r2_score(y, y_pred)
        print("R^2 score:", r2)


def delete_files_in_point_tif_folder():
    # Delete all files in the "point_tif" folder
    folder_path = "app/point_tif2"
    files = glob.glob(os.path.join(folder_path, "*"))
    for file in files:
        os.remove(file)

    print("All files in 'point_tif' folder deleted successfully.")


def main():
    rainfall_values = get_rainfall_from_points()
    prediction_flood_levels(rainfall_values)
    # delete_files_in_point_tif_folder()


if __name__ == "__main__":
    main()
