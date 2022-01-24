"Download data from the PERSIANN database."

# url
from urllib import request

# utils
import datetime
import os


def download_file(remote_url, local_file):
    request.urlretrieve(remote_url, local_file)


def download_PERSIANN_raw_daily_data_global_singleday(day:datetime.date, local_file:str=None):
    base_url = 'http://persiann.eng.uci.edu/CHRSdata/PERSIANN/daily/'
    target_data = 'ms6s4' + '_d' + str(day.year)[-2:] + str(day.strftime('%j')) + '.bin.gz'
    full_url = ''.join([base_url, target_data])
    if local_file is None:
        local_file = target_data

    download_file(full_url, local_file)


def get_PERSIANN_raw_daily_data_global(
    from_date:datetime.date,
    to_date:datetime.date,
    local_folder:str
):
    """
    Download the PERSIANN data in the binary format (.bin)
    given a set of dates and a local folder.

    Args:
        from_date (datetime.date): 
        to_date (datetime.date):
        local_folder (str): 

    Raises:
        Exception: '"from_date" must be lesser or equal to "to_date".'
    
    Returns:
        None
    """
    if not from_date <= to_date:
        raise Exception(
            '"from_date" must be lesser or equal to "to_date".'
        )

    diff_days = (to_date - from_date).days

    for i in range(diff_days+1):
        target_date = from_date + datetime.timedelta(days=i)
        filename = (str(target_date) + '.bin.gz').replace('-', '_')
        lfile = os.path.join(local_folder, filename)
        download_PERSIANN_raw_daily_data_global_singleday(
            target_date,
            local_file=lfile
        )

