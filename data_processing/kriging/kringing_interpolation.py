import io
import base64

import pandas as pd
import numpy as np
from pyproj import CRS, Transformer
from matplotlib.image import imsave

from skgstat import Variogram, OrdinaryKriging
import numpy as np
import json


#Code for Utah map projection
CRS_code = 32143

#Variogram hyperparameters
VARIO = dict(
    n_lags=100,
    estimator='matheron',
    model='exponential',
    # normalize=True
)
#Kringing hyperparameters
KRIG = dict(
    min_points=2,
    max_points=30
)
# number of cells in each dimension
GRIDSIZE = 200

def get_data(fname):
    df = pd.read_csv(fname)
    region = [39.906272, -112.668707, 41.396185, -111.169071]
    df = df.loc[(df['lat'] > region[0]) & (df['lat'] < region[2]) & (df['lon'] > region[1]) & (df['lon'] < region[3])]
    crs_4326 = CRS('epsg:4326')
    crs_proj = CRS('epsg:' + str(CRS_code))
    transformer = Transformer.from_crs(crs_4326, crs_proj)
    pts = [(lat, lon) for lat, lon in zip(df.lat.values, df.lon.values)]
    pts_proj = transformer.itransform(pts)
    pts_proj = [pt for pt in pts_proj]
    df['y'] = [pt[0]for pt in pts_proj]
    df['x'] = [pt[1] for pt in pts_proj]    

    return df
    
def variogram(df, **kwargs):
    coords = df[['x', 'y']].values
    values = df.value.values

    return Variogram(coords, values, **kwargs)

def get_bounds(df):
    xmin = df.x.min()
    xmax = df.x.max()
    ymin = df.y.min()
    ymax = df.y.max()

    return xmin, xmax, ymin, ymax

def build_grid(df, resolution=100):
    xmin, xmax, ymin, ymax = get_bounds(df)
    xx, yy = np.mgrid[xmin:xmax:resolution*1j, ymin:ymax:resolution*1j]

    return xx, yy

def krig(vario, grid, **kwargs):
    xx, yy = grid

    ok = OrdinaryKriging(vario, **kwargs)
    field = ok.transform(xx.flatten(), yy.flatten())
    sigma = ok.sigma

    return field.reshape(xx.shape), sigma.reshape(xx.shape)

def asBase64(field, name):
    f = io.BytesIO()

    vmin = 1.02 * np.nanmin(field)
    vmax = .98 * np.nanmax(field)
    imsave(f, np.fliplr(field), vmin=vmin, vmax=vmax, cmap='YlOrRd')

    f.seek(0)
    s = base64.b64encode(f.read())
    return 'data:image/png;base64,%s' % s.decode()

if __name__ == '__main__':
    df = get_data('coords.csv')

    grid = build_grid(df, GRIDSIZE)
    V = variogram(df, normalize=False, **VARIO)
    print('variogram found')
    field, sigma = krig(V, grid, **KRIG)
    print('kringing done')
    data = asBase64(field, 'field.png')
    # get the data bounds
    bounds = [[df.lat.max(), df.lon.min()], [df.lat.min(), df.lon.max()]]

    code = "var img = '%s';\nvar bnd = %s;" % (data, json.dumps(bounds))