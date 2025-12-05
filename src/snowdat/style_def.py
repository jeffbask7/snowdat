import numpy as np
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from cartopy.feature import ShapelyFeature
import matplotlib.colors as mcolors



color_values_windsp = {
        0: '#FFFFFF00',
        5: '#FFFFFF00',
        10: '#0000FF99',
        15: 'blue',
        20: 'yellow',
        25: 'orange',
        30: 'brown',
        35: 'red',
        40: 'pink',
        50: 'green',
        60: 'aqua',
        70: 'teal',
        80: 'slategray'
    }

norm_windsp = mcolors.Normalize(vmin=min(color_values_windsp.keys()), vmax=max(color_values_windsp.keys()))

# Create a LinearSegmentedColormap
cmap_windsp = mcolors.LinearSegmentedColormap.from_list(
    'colormap_tempF',
    [(norm_windsp(value), color) for value, color in color_values_windsp.items()]
)

color_values_2t = {
        -30: 'maroon',
        -20: 'teal',
        -10: 'lavender',
        0: 'white',
        10: 'fuchsia',
        20: 'purple',
        30: 'blue',
        40: 'aqua',
        50: 'green',
        60: 'yellow',
        70: 'orange',
        80: 'red',
        90: 'purple',
        100: 'white',
        110: 'pink',
        130: 'maroon'
    }

norm_2t = mcolors.Normalize(vmin=min(color_values_2t.keys()), vmax=max(color_values_2t.keys()))

# Create a LinearSegmentedColormap
cmap_2t = mcolors.LinearSegmentedColormap.from_list(
    'colormap_tempF',
    [(norm_2t(value), color) for value, color in color_values_2t.items()]
)


color_values_snow_accum = {
        0: '#00000000',
        0.01: '#00000000',
        0.1: '#00000000',
        #0.1: 'lightcyan',
        0.5: 'paleturquoise',
        1: 'cyan',
        2: 'deepskyblue',
        3: 'blue',
        4: 'darkblue',
        6: 'blueviolet',
        9: 'darkviolet',
        12: 'crimson',
        15: 'deeppink',
        18: 'lightpink',
        24: 'peru'
    }

norm_snow_accum = mcolors.Normalize(vmin=min(color_values_snow_accum.keys()), vmax=max(color_values_snow_accum.keys()))

# Create a LinearSegmentedColormap
cmap_snow_accum = mcolors.LinearSegmentedColormap.from_list(
    'colormap_snow_accum',
    [(norm_snow_accum(value), color) for value, color in color_values_snow_accum.items()]
)

color_values_snow_depth = {
        0: '#00000000',
        0.01: '#00000000',
        0.1: '#00000000',
        0.5: '#00000000',
        1: 'cyan',
        2: 'deepskyblue',
        3: 'blue',
        6: 'darkblue',
        9: 'blueviolet',
        12: 'darkviolet',
        18: 'crimson',
        24: 'deeppink',
        36: 'lightpink',
        72: 'peru'
    }

norm_snow_depth = mcolors.Normalize(vmin=min(color_values_snow_depth.keys()), vmax=max(color_values_snow_depth.keys()))

# Create a LinearSegmentedColormap
cmap_snow_depth = mcolors.LinearSegmentedColormap.from_list(
    'colormap_snow_depth',
    [(norm_snow_depth(value), color) for value, color in color_values_snow_depth.items()]
)

#USE FOR LISTED COLORMAP
""" bounds = list(color_values_2t.keys())
cmap_2t = mcolors.ListedColormap(list(color_values_2t.values()))
norm_2t = mcolors.BoundaryNorm(bounds, len(bounds)) """


color_values_refc = {
    5: '#FFFFFF00',
    10: '#00FF0088',
    20: 'green',
    30: 'yellow',
    40: 'orange',
    50: 'red',
    60: 'purple',
    70: 'pink',
    80: 'orange'
}


norm_refc = mcolors.BoundaryNorm(
    boundaries=list(color_values_refc.keys()),
    ncolors=len(color_values_refc),
    extend='neither' )

values_refc = list(color_values_refc.values())
levels_refc = list(color_values_refc.keys())
#print(levels_refc)
#print(values_refc)
cmap_refc = mcolors.ListedColormap(values_refc)
norm_refc = mcolors.BoundaryNorm(levels_refc, ncolors=cmap_refc.N, extend='neither')

color_values_refc_snow = {
    105: '#FFFFFF00',
    110: '#0000FF88',
    120: 'aqua',
    130: 'blue',
    140: 'purple',
    150: 'pink',
    160: 'white',
    170: 'green',
    180: 'orange'
}


norm_refc_snow = mcolors.BoundaryNorm(
    boundaries=list(color_values_refc_snow.keys()),
    ncolors=len(color_values_refc_snow),
    extend='neither' )

values_refc_snow = list(color_values_refc_snow.values())
levels_refc_snow = list(color_values_refc_snow.keys())
#print(levels_refc_snow)
#print(values_refc_snow)
cmap_refc_snow = mcolors.ListedColormap(values_refc_snow)

norm_refc_snow = mcolors.BoundaryNorm(levels_refc_snow, ncolors=cmap_refc_snow.N, extend='neither')

color_values_refc_ice = {
    205: '#FFFFFF00',
    210: '#0000FF88',
    220: 'red',
    230: 'yellow',
    240: 'green',
    250: 'brown',
    260: 'white',
    270: 'blue',
    280: 'black'
}

norm_refc_ice = mcolors.BoundaryNorm(
    boundaries=list(color_values_refc_ice.keys()),
    ncolors=len(color_values_refc_ice),
    extend='neither' )

values_refc_ice = list(color_values_refc_ice.values())
levels_refc_ice = list(color_values_refc_ice.keys())
#print(levels_refc_ice)
#print(values_refc_ice)
cmap_refc_ice = mcolors.ListedColormap(values_refc_ice)
norm_refc_ice = mcolors.BoundaryNorm(levels_refc_ice, ncolors=cmap_refc_ice.N, extend='neither')

color_values_prate_type = {
    0: '#FFFFFF00',
    0.001: '#00990077',
    0.002: 'greenyellow',
    0.003: 'green',
    0.004: 'yellow',
    0.006: 'orange',
    0.008: 'red',
    0.01: 'purple',
    0.02: 'brown',
    0.99: 'brown',
    1: '#FFFFFF00',
    1.0001: '#00009977',
    1.0002: 'skyblue',
    1.0005: 'blue',
    1.001: 'purple',
}

color_values_prate = {
    0: '#FFFFFF00',
    0.00001: '#00990077',
    0.002: 'greenyellow',
    0.003: 'green',
    0.004: 'yellow',
    0.006: 'orange',
    0.008: 'red',
    0.01: 'purple',
    0.02: 'brown',
}

color_values_prate_snow = {
    1: '#FFFFFF00',
    1.00001: '#00009977',
    1.0002: 'skyblue',
    1.0005: 'blue',
    1.001: 'purple',
}

norm_prate = mcolors.BoundaryNorm(
    boundaries=list(color_values_prate.keys()),
    ncolors=len(color_values_prate),
    extend='neither' )

values_prate = list(color_values_prate.values())
levels_prate = list(color_values_prate.keys())
#print(levels_prate)
#print(values_prate)
cmap_prate = mcolors.ListedColormap(values_prate)
norm_prate = mcolors.BoundaryNorm(levels_prate, ncolors=cmap_prate.N, extend='neither')

norm_prate_snow = mcolors.BoundaryNorm(
    boundaries=list(color_values_prate_snow.keys()),
    ncolors=len(color_values_prate_snow),
    extend='neither' )

values_prate_snow = list(color_values_prate_snow.values())
levels_prate_snow = list(color_values_prate_snow.keys())
#print(levels_prate_snow)
#print(values_prate_snow)
cmap_prate_snow = mcolors.ListedColormap(values_prate_snow)
norm_prate_snow = mcolors.BoundaryNorm(levels_prate_snow, ncolors=cmap_prate_snow.N, extend='neither')
                            
levels_mslp = np.linspace(88000,108000,51)
levels_thk = np.linspace(4500,6120, 28)
levels_prate = np.linspace(0,0.02,100)
levels_prate_snow = np.linspace(1,1.02,100)
levels_t2 = np.linspace(-30, 130, 161)
levels_windsp = np.linspace(0, 80, 81)