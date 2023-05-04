import os

import fiona
import rasterio
from rasterio.features import geometry_mask
from shapely.geometry import Polygon, mapping
from fiona.crs import from_epsg
from fiona.crs import to_string, from_epsg
import json
from fiona.crs import CRS



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
    with rasterio.open(tif_path) as tif:
        print("HTTP 1.1/ 200 OK")
        print("Content-Type: Text/Plain")
        print("")
        print("Tiff Opened")
        print("######################")

        # Получение геометрии изображения
        tif_transform = tif.transform
        tif_crs = tif.crs

        # Чтение данных изображения
        tif_data = tif.read(1)

        # Создание маски изображения
        mask = geometry_mask(
            [mapping(Polygon([(tif_transform * (0, 0)),
                               (tif_transform * (tif.width, 0)),
                               (tif_transform * (tif.width, tif.height)),
                               (tif_transform * (0, tif.height)),
                               (tif_transform * (0, 0))]))],
            out_shape=tif_data.shape,
            transform=tif_transform,
            invert=True
        )

        # Преобразование маски в полигоны
        contours = rasterio.features.shapes(tif_data * mask, transform=tif_transform)

        # Создание GeoJSON-файла
        schema = {
            'geometry': 'Polygon',
            'properties': {},
        }
        with open(output_path, 'w') as output_file:
            with fiona.open(output_file, 'w', driver='GeoJSON', schema=schema, crs=CRS.from_epsg(tif_crs.to_epsg())) as c:
                for contour in contours:
                    c.write({
                        'geometry': contour[0],
                        'properties': {}
                    })

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
    args = os.environ.get("QUERY_STRING","input/test_365 (19).tif&output/test.geojson")
    args_list = args.split("&")
    if len(args_list) != 2:
        print("404") ################

    tif_to_geojson(args_list[0],args_list[1])
