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

from snowdat.style_def import cmap_snow_accum
from snowdat.style_def import cmap_snow_depth
from snowdat.snowdat_utils import DatetimeParts


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


def plot_snow(ds, product_name, date, levels=None, vmin=None, vmax=None, cmap=None, tickspace=1):
    #key_var = list(ds.data_vars.keys())[0]
    ds4 = ds.coarsen(x=4, y=4, boundary='trim').mean()
    ts = ds4[product_name]
    scale = 0.03937 #(m to inches)/100
    vmin = 0
    if product_name == 'snow depth':
        cmap = cmap_snow_depth
        levels = np.linspace(0,72,73)
        vmax = 72
        tickspace = 3
    elif product_name == 'snow precip':
        cmap = cmap_snow_accum
        levels = np.linspace(0,24,100)
        vmax = 24
    else:
        raise ValueError(f"Invalid product name: {product_name}. Must be 'snow depth' or 'snow precip'.")
    #print(ts)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(13,8), subplot_kw=dict(projection=ccrs.PlateCarree()))
    contour = ax.contourf(ts.longitude.values, ts.latitude.values, (np.squeeze(ts.values))*scale, transform=ccrs.PlateCarree(), levels=levels, vmin=vmin, vmax=vmax, cmap=cmap, extend='max')
    ax.add_feature(cfeature.COASTLINE, edgecolor='black', facecolor='none')
    ax.add_feature(cfeature.STATES, edgecolor='black', facecolor='none')
    custom_ticks = np.arange(0, vmax+1, tickspace)
    cbar = fig.colorbar(contour, ticks=custom_ticks, shrink=1.0, orientation='horizontal', pad=0.03, aspect=60)
    plt.title(f'SNODAS {product_name} {date.date_str}')
    fig.savefig(f'data/SNODAS-{product_name}-{date.date_str}.png')


