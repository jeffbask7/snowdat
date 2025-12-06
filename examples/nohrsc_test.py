import snowdat as sn
from datetime import datetime


time_valid = sn.DatetimeParts(datetime(2025,12,5,12))
time_valid.Duration(duration=72)

#FILE TYPE CAN BE .png, .tif, .nc DEFAULT IS .png
file_path = sn.get_nohrsc(date=time_valid,  file_type='tif')

#ds = xr.load_dataset(file_path, engine='netcdf4')
sn.nohrsc_snow(file_path)