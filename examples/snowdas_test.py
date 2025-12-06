import snowdat as sn
from datetime import datetime


date = sn.DatetimeParts(datetime(2025,12,6,0))
products = ['SNOW PRECIP', 'SNOW DEPTH']

#DOWNLOAD AND EXTRACT TAR FILE 
ds = sn.snowdas_dl(date)

#PROCESS PRODUCTS
for product in products:
    product = product.lower()
    outfile_name = sn.snowdas_to_cog(ds, product=product, date=date)
    sn.plot_snowdas(ds, product, date)