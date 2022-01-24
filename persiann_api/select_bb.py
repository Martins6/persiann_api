"""Given a .tiff select the geographic bounding box required."""

# data wrangling
import numpy as np

# image processing
from PIL import Image


def geotiff_to_arr(geotiff_path:str) -> np.array:
    """
    Open the GeoTIFF file and turn into a numpy array. 

    Args:
        geotiff_path (str): the path of the GeoTIFF file.

    Returns:
        np.array: representing the corresponding values on each coordinate.
    """
    arr = np.asarray(Image.open(geotiff_path, mode='r'))
    return arr


def get_bb_geoarr_from_global_data(
    arr:np.array,
    lat_bb=None, lon_bb=None
) -> np.array:
    """
    It takes an array of values representing the whole
    globe and selects only the values inside the bounding box.

    Args:
        arr (np.array): np.array of (440, 1440) shape.
        lat_bb (Tuple, optional): Tuple of limits in the latitude dimension.
            Defaults to None, which brings the whole globe.
        lon_bb (Tuple, optional): Tuple of limits in the longitude dimension.
            Defaults to None, which brings the whole globe.

    Returns:
        np.array: np.array of (value, lat_value, lon_value).
    """
    if lat_bb is None:
        lat_bb = (-60, 60)
    if lon_bb is None:
        lon_bb = (-180, 180)
    
    lat_bb = [- i for i in lat_bb] # because it is changed from the norm that North is +, and South is -.

    lat_index_arr = np.arange(480)
    lon_index_arr = np.arange(1440)
    lat = np.arange(-60, 60, .25)
    lon = np.arange(-180, 180, .25)

    mask_lat = (lat >= lat_bb[1]) & (lat <= lat_bb[0])
    mask_lon = (lon >= lon_bb[0]) & (lon <= lon_bb[1])

    target_lat_index = lat_index_arr[mask_lat]
    target_lon_index = lon_index_arr[mask_lon]

    target_lat = lat[mask_lat]
    target_lon = lon[mask_lon]

    geoarr = np.zeros((target_lat_index.shape[0], target_lon_index.shape[0], 3))
    for i, lat_i in enumerate(target_lat_index):
        for j, lon_j in enumerate(target_lon_index):
            value = arr[lat_i, lon_j]
            lat_value = -target_lat[i]
            lon_value = target_lon[j]
            geoarr[i, j] = np.array([value, lat_value, lon_value])

    return geoarr
