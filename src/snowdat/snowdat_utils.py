from dataclasses import dataclass
from datetime import datetime
import rioxarray  as rio
from rasterio.transform import from_bounds
from snowdat.style_def import cmap_snow_accum
from snowdat.style_def import cmap_snow_depth



@dataclass
class DatetimeParts:

    #write a docstring for this class
    dt: datetime

    def __getattr__(self, name):
        return getattr(self.dt, name)

    @property
    def year_str(self):
        return f"{self.dt.year}"

    @property
    def month_str(self):
        return f"{self.dt.month:02d}"
    
    @property
    def month_name(self):
        return self.dt.strftime(r'%b')
        #return f"{self.dt.month:02d}"
    
    @property
    def day_str(self):
        return f"{self.dt.day:02d}"
    
    @property
    def day_name(self):
        return self.dt.strftime(r'%a')
        #return f"{self.dt.day:02d}"

    @property
    def date_str(self):
        return self.dt.strftime(r'%Y%m%d')  
    
    @property
    def hour_str(self):
        if self.hour not in [0,6,12,18]:
            raise ValueError('Duration must be one of 0 6 12 18')
        return f"{self.dt.hour:02d}"
    
    def hour_str_fill(self, length):
        return (str(self.dt.hour)).zfill(length)
    
    def microsecond_str(self):
        return self.dt.strftime(r'%f')
    

    def Duration(self, duration, length=2):
        if duration not in [6,24,48,72]:
            raise ValueError('Duration must be one of 6 24 48 72')
        if (duration != 6) and self.hour in [6,18]:
            raise ValueError('Duration must be 6 if hour is 6 or 18')
        self.duration = duration
        self.duration_str = (str(duration)).zfill(length)


def snowdas_to_cog(ds, product='snow depth', date=None) -> str:
    snow_depth = ds[product].astype('float32')  # work with the DataArray you want


    scale_factor = 0.03937  # m → in
    snow_depth.attrs.update(units="in", scale_factor=scale_factor)

    lon = ds.longitude.values
    lat = ds.latitude.values

    # attach the geographic coordinates to the x/y dimensions
    snow_depth = snow_depth.assign_coords(
        x=("x", lon),
        y=("y", lat)
    )

    # make sure rows go from north→south (rioxarray expects this)
    if snow_depth.y[0] < snow_depth.y[-1]:
        snow_depth = snow_depth.sortby("y", ascending=False)

    transform = from_bounds(
        float(lon.min()), float(lat.min()),
        float(lon.max()), float(lat.max()),
        lon.size, lat.size
    )

    snow_depth = (
        snow_depth
        .rio.set_spatial_dims(x_dim="x", y_dim="y")  # tell rioxarray which dims carry geography
        .rio.write_transform(transform)
        .rio.write_crs("EPSG:4326")
        .rio.write_nodata(0)  # optional: keep your chosen nodata value explicit
    )

    date_str = f"{date.year_str}{date.month_str}{date.day_str}"
    file_out = f"data/snodas_cog/snodas-{product.replace(' ', '')}-{date_str}.tif"
    snow_depth.rio.to_raster(file_out,
                            driver="COG",
                            dtype="float32",   # or your dtype
                            compress="deflate",
                            blocksize=512,
                            num_threads="ALL_CPUS",
                            )
    return file_out


