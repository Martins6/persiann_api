"""Concentrate the main functions of the package."""
from persiann_api import (
    download,
    to_geotiff,
    select_bb
)

# utils
import os
import datetime

def download_data(
    from_date:datetime.date, to_date:datetime.date,
    folder:str,
    lat_bb=(-60, 60),
    lon_bb=(-180, 180)
):
    """
    Download daily weather data from the PERSIANN database
    into a collection of .tiff inside a folder.

    Args:
        from_date (datetime.date): the beginning date.
        to_date (datetime.date): the end date.
        folder (str): folder to download all of the data. It should be empty, but if not,
            the function will only look upon the .bin.gz data downloaded into it.
        lat_bb (tuple, optional): The bounding box (bb) coordinates for the latitude.
            Ordered as (min, max). Defaults to (-60, 60).
        lon_bb (tuple, optional): The bounding box (bb) coordinates for the longitude.
            Ordered as (min, max). Defaults to (-180, 180).
    
    Returns:
        None
    """

    print('Downloading data...')
    download.get_PERSIANN_raw_daily_data_global(
        from_date=from_date,
        to_date=to_date,
        local_folder=folder
    )
    
    for f in os.listdir(folder):
        if '.bin.gz' in f:
            aux = f.split('.bin.gz')[0]
            date_str = os.path.split(aux)[-1]
    
            to_geotiff.gz_to_geotiff(
                gzFile=os.path.join(folder, f'{date_str}.bin.gz')
            )

            geo_arr = select_bb.get_bb_geoarr_from_global_data(
                select_bb.geotiff_to_arr(os.path.join(folder, f'{date_str}.tiff')),
                lat_bb=lat_bb,
                lon_bb=lon_bb
            )
            geo_arr = geo_arr[:, :, 0].squeeze() # selecting only the values for each coord.

            to_geotiff.write_geotiff_from_arr(
                geo_arr[::-1], # must mirror to write correctly in the GeoTIFF format.
                originx=lon_bb[0],
                originy=lat_bb[0],
                pixelsize=0.25,
                OutputFile=os.path.join(folder, f'{date_str}.tiff')
            )

            os.remove(os.path.join(folder, f'{date_str}.bin'))
            os.remove(os.path.join(folder, f'{date_str}.bin.gz'))
    print('Data downloaded!')