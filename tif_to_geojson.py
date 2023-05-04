import os
from osgeo import gdal, ogr


def tif_to_geojson(tif_path, output_path):
    # Проверка, существует ли файл по указанному пути
    if not os.path.exists(tif_path):
        print("HTTP/1.1 404 Not Found")
        print("Content-Type: text/plain")
        print("")
        print("Bad Request")
        print("######################")
        return

    # Проверка, является ли файл Tiff
    if not tif_path.lower().endswith('.tif'):
        print("HTTP 1.1/ 415 Unsupported Media Type")
        print("Content-Type: Text/Plain")
        print("")
        print("Not tiff input")
        print("######################")
        return

    # Открытие Tiff-файла
    tif_ds = gdal.Open(tif_path)
    print("HTTP 1.1/ 200 OK")
    print("Content-Type: Text/Plain")
    print("")
    print("Tiff Opened")
    print("######################")

    # Получение геометрии изображения
    try:
        tif_layer = tif_ds.GetLayer()
        tif_srs = tif_layer.GetSpatialRef()
    except Exception as e:
        print("HTTP 1.1/ 415 Unsupported Media Type")
        print("Content-Type: Text/Plain")
        print("")
        print("Bad tif image")
        print("######################")
    # Создание GeoJSON-файла
    geojson_driver = ogr.GetDriverByName('GeoJSON')
    geojson_ds = geojson_driver.CreateDataSource(output_path)
    geojson_layer = geojson_ds.CreateLayer('layer', srs=tif_srs, geom_type=ogr.wkbPolygon)

    # Преобразование Tiff-изображения в GeoJSON-файл
    gdal.Polygonize(tif_layer, None, geojson_layer, 0, [], callback=None)

    # Закрытие файловых объектов
    tif_ds = None
    geojson_ds = None

    # Проверка, является ли созданный файл GeoJSON
    if not output_path.lower().endswith('.geojson'):
        print("HTTP 1.1/ 415 Unsupported Media Type")
        print("Content-Type: Text/Plain")
        print("")
        print("Not GeoJSON created")
        print("######################")

        return

    print("HTTP 1.1/ 200 OK")
    print("Content-Type: Text/Plain")
    print("")
    print(f"GeoJSON created - {os.environ}")
    print("######################")


if __name__ == '__main__':
    tif_to_geojson("input/test_365 (19).tif","output/")