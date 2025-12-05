import xarray as xr
import numpy as np
import requests
import tarfile
from io import BytesIO
import gzip
import io
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime

from style_def import cmap_snow_accum
from style_def import cmap_snow_depth
from snowdat_utils import DatetimeParts


product1 = "zz_ssmv11044bS__T0024TTNATSYYYYMMDD05DP000.dat.gz" #SNOW MELT
product2 = "zz_ssmv11039lL00T0024TTNATSYYYYMMDD05DP000.dat.gz" #SUBLIMATION
product3 = "zz_ssmv11038wS__A0024TTNATSYYYYMMDD05DP001.dat.gz" #SNOW PACK TEMPERATURE
product4 = "zz_ssmv11036tS__T0001TTNATSYYYYMMDD05HP001.dat.gz" #SNOW DEPTH
product5 = "zz_ssmv11034tS__T0001TTNATSYYYYMMDD05HP001.dat.gz" #SNOW WATER EQUIVALENT
product6 = "zz_ssmv01025SlL01T0024TTNATSYYYYMMDD05DP001.dat.gz" #FROZEN PRECIP
product7 = "zz_ssmv01025SlL00T0024TTNATSYYYYMMDD05DP001.dat.gz" #NON FROZEN PRECIP

product_list_all = [product1, product2, product3, product4, product5, product6, product7]
product_list = [product4, product6]

SNODAS_PRODUCTS = {'SNOW MELT':"zz_ssmv11044bS__T0024TTNATSYYYYMMDD05DP000.dat.gz",
                'SUBLIMATION':"zz_ssmv11039lL00T0024TTNATSYYYYMMDD05DP000.dat.gz",
                'SNOW PACK TEMPERATURE': "zz_ssmv11038wS__A0024TTNATSYYYYMMDD05DP001.dat.gz",
                'SNOW DEPTH': "zz_ssmv11036tS__T0001TTNATSYYYYMMDD05HP001.dat.gz",
                'SNOW WATER EQUIVALENT': "zz_ssmv11034tS__T0001TTNATSYYYYMMDD05HP001.dat.gz",
                'SNOW PRECIP': "zz_ssmv01025SlL01T0024TTNATSYYYYMMDD05DP001.dat.gz",
                'NON FROZEN PRECIP': "zz_ssmv01025SlL00T0024TTNATSYYYYMMDD05DP001.dat.gz"
                }
 
 
           

def snowdas_dl(date, products=None):
    if products is None:
        products = ['SNOW PRECIP', 'SNOW DEPTH'] 
    date = DatetimeParts(date)
    #remote_tar_url = "https://noaadata.apps.nsidc.org/NOAA/G02158/unmasked/2025/11_Nov/SNODAS_unmasked_20251130.tar"
    remote_tar_url = f"https://noaadata.apps.nsidc.org/NOAA/G02158/unmasked/{date.year}/{date.month}_{date.month_name}/SNODAS_unmasked_{date.year}{date.month_str}{date.day_str}.tar"

    response = requests.get(remote_tar_url, stream=True)
    response.raise_for_status()

    # Wrap the raw response stream in a BytesIO object for tarfile
    tar_stream = BytesIO(response.raw.read())

    nrows, ncols = 4096,8192
    dtype = np.dtype('>i2')

    lat_min, lat_max = 24.1000, 58.2333
    lon_min, lon_max = -130.5167, -62.2500

    lats = np.linspace(lat_max, lat_min, nrows)
    lons = np.linspace(lon_min, lon_max, ncols)

    #products = ['snod', 'sn24hr']

    ds_list = []


    with tarfile.open(fileobj=tar_stream, mode='r') as tar:
        for key, value in SNODAS_PRODUCTS.items():
            if key in products:
                target = value.replace('YYYYMMDD', date.date_str)
                member = tar.getmember(target)
                with tar.extractfile(member) as gf:
                    with gzip.open(gf, 'rb') as zf:
                        #raw = zf.read()
                        data = np.frombuffer(zf.read(), dtype = dtype)

                        nrows, ncols = 4096,8192
                        dtype = np.dtype('>i2')
                        lat_min, lat_max = 24.1000, 58.2333
                        lon_min, lon_max = -130.5167, -62.2500
                        lats = np.linspace(lat_max, lat_min, nrows)
                        lons = np.linspace(lon_min, lon_max, ncols)

                        data = data.reshape(nrows, ncols)
                        data = np.where(data == -9999, 0, data)
                        print(data)
                        product_name = key.lower()
                        ds = xr.Dataset({product_name: (["y","x"], data)}, coords={'latitude': ('y', lats), 'longitude': ('x', lons)})
                        ds_list.append(ds)
    ds = xr.merge(ds_list, compat='override')
    return ds

if __name__ == '__main__':
    date = DatetimeParts(datetime(2025,12,1,22))
    products = ['SNOW PRECIP', 'SNOW DEPTH']
    print(date.day_name)
    print(date.month_name)
    print(date.date_str)
    ds = snowdas_dl(date)
    print(ds)
    ds1 =ds