import snowdat as sn
from datetime import datetime


date = sn.DatetimeParts(datetime(2025,12,6,0))
products = ['SNOW PRECIP', 'SNOW DEPTH']
print(date.day_name)
print(date.month_name)
print(date.date_str)
ds = sn.snowdas_dl(date)
for product in products:
    product = product.lower()
    outfile_name = sn.snowdas_to_cog(ds, product=product, date=date)
    sn.plot_snow(ds, product, date)