from select import select
from persiann_api import (
    download,
    to_geotiff,
    select_bb
)

# utils
import shutil
import os
import datetime

if __name__ == '__main__':
    folder_test = './data/test_data'
    if not os.path.isdir(folder_test):
        os.mkdir(folder_test)
    # else:
    #     shutil.rmtree(folder_test)

    date_2 = datetime.date(2021, 12, 31)
    date_1 = datetime.date(2021, 12, 1)
    # download.get_PERSIANN_raw_daily_data_global(
    #     from_date=date_1,
    #     to_date=date_2,
    #     local_folder=folder_test
    # )

    date_str = '2021_12_01'
    to_geotiff.gz_to_geotiff(
        gzFile=f'data/test_data/{date_str}.bin.gz'
    )

    aux = select_bb.get_bb_geoarr(
        select_bb.geotiff_to_arr(f"data/test_data/{date_str}.tiff"),
        lat_bb=(-35, 6),
        lon_bb=(-69, -36)
    )
    print(aux.shape)
    #os.remove(f'data/test_data/{date_str}.bin')
    #os.remove(f'{date_str}.bin.gz')