#!/usr/bin/python3
import os
from osgeo import gdal, ogr
import json


def tif_to_geojson(tif_path, output_path):
    # Проверка, существует ли файл по указанному пути
    if not os.path.exists(tif_path):
        print("HTTP/1.1 404 Not Found")
        print("Content-Type: text/plain")
        print("")
        print("Bad Request")

        return

    # Проверка, является ли файл Tiff
    if not tif_path.lower().endswith('.tif'):
        print("HTTP/1.1 415 Unsupported Media Type")
        print("Content-Type: text/plain")
        print("")
        print("Not tiff input")

        return

    # Открытие Tiff-файла
    tif_ds = gdal.Open(tif_path)

    # создание пустого объекта GeoJSON
    empty_geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # создание директории, если она не существует
    output_paths, filename = output_path.split("/")
    os.makedirs(output_paths, exist_ok=True)
    print(output_path)

    # формирование пути к файлу
    file_path = os.path.join(output_paths, filename)

    # открытие файла для записи
    with open(file_path, "w") as f:
        # запись пустого GeoJSON объекта в файл
        json.dump(empty_geojson, f)



    # Проверка, является созданный файл GeoJSON
    if not output_path.lower().endswith('.geojson'):
        print("HTTP/1.1 415 Unsupported Media Type")
        print("Content-Type: text/plain")
        print("")
        print("Not GeoJSON created")

        return

    print("HTTP/1.1 200 OK")
    print("Content-Type: text/plain")
    print("")
    print(f"GeoJSON created - {os.environ}")



if __name__ == '__main__':
    args = os.environ.get("QUERY_STRING","input/test_365 (19).tif&output/test.geojson")
    args_list = args.split("&")
    if len(args_list) != 2:
        print("HTTP 1.1/ 400 Bad request")
        print("Content-Type: text/plain")
        print("")
        print("Not 2 arguments")

    tif_to_geojson(args_list[0], args_list[1])