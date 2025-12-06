from pathlib import Path
import xarray as xr
import numpy as np
import requests
from datetime import datetime
import matplotlib.pyplot as plt
from cartopy import crs as ccrs
from cartopy import feature as cfeature   
from .snowdat_utils import DatetimeParts
from .style_def import cmap_snow_accum
from .style_def import cmap_snow_depth



def get_nohrsc(date, file_type='png', export_dir='data') -> Path:
    url = f"https://www.nohrsc.noaa.gov/snowfall_v2/data/{date.year}{date.month_str}/sfav2_CONUS_{date.duration}h_{date.year}{date.month_str}{date.day_str}{date.hour_str}.{file_type}"
    url_path = Path(url)  
    dir_path = Path(export_dir, f'nohrsc_{file_type}', f'{date.year}{date.month_str}')
    file_path = dir_path / url_path.name
    dir_path.mkdir(parents=True, exist_ok=True)
    #print(url)
    with open(file_path, 'wb') as f:
        result = requests.get(url)
        result.raise_for_status()
        contents = result.content
        f.write(contents)

    return file_path


def plot_nohrsc_snow(file_path=None, ds=None, bounding_box=None):
    if ds == None:
       if file_path == None:
          raise ValueError('Must provide either a dataset or a file path')
       print('loading dataset from file')
       ds = xr.load_dataset(file_path, engine='netcdf4')
       #print(ds)
    key_var = 'Data'
    ts = ds[key_var]
    #ds_lowres = ds.coarsen(lon=2, lat=2, boundary='trim').mean()
    #ts = ds_lowres[key_var]
    start_date = (ts.attrs['start_date'])
    stop_date = (ts.attrs['stop_date'])
    time_start = datetime.strptime(start_date, r'%Y-%m-%d %H:%M:%S UTC')
    time_stop = datetime.strptime(stop_date, r'%Y-%m-%d %H:%M:%S UTC')
    time_start_str = datetime.strftime(time_start, r'%a %b %d %H UTC')
    time_stop_str = datetime.strftime(time_stop, r'%a %b %d %H UTC')
    duration = int((time_stop-time_start).total_seconds()/3600)
    product_name = (ts.attrs['long_name'])
    scale = 39.37
    vmin = 0
    vmax = 24
    levels = np.arange(vmin,vmax+1,0.1)
    cmap = cmap_snow_accum
    if bounding_box is not None:
        extent = (bounding_box['xmin'], bounding_box['xmax'], bounding_box['ymin'], bounding_box['ymax'])
    else:
        extent = (-125, -65, 24, 50)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(13,8), subplot_kw=dict(projection=ccrs.PlateCarree()))
    contour = ax.contourf(ts.lon.values, ts.lat.values, (np.squeeze(ts.values))*scale, transform=ccrs.PlateCarree(), levels=levels, vmin=vmin, vmax=vmax, cmap=cmap, extend='max')
    #ax.set_extent((x0, x1, y0, y1))
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE, edgecolor='black', facecolor='none')
    ax.add_feature(cfeature.STATES, edgecolor='black', facecolor='none')
    custom_ticks = np.arange(0, vmax+1, 1)
    cbar = fig.colorbar(contour, ticks=custom_ticks, shrink=0.8, orientation='horizontal', pad=0.03, aspect=60)
    plt.title(f'{product_name.upper()} {duration}HR {time_start_str.upper()} TO {time_stop_str.upper()} (Inches)')
    fig.text(
            0.5,          # x position (0=left, 1=right)
            0.13,         # y position (0=bottom, 1=top)
            "National Gridded Snowfall Analysis | National Operational Hydrologic Remote Sensing Center \n" \
            "WARNING: THIS PRODUCT SHOULD NOT BE SOLELY RELIED UPON FOR SNOWFALL AMOUNT FOR A PARTICULAR LOCATION",
            ha="center",va="bottom",fontsize=9,color="gray",
    )


