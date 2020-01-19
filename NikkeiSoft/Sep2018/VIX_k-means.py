# %matplotlib inline
import datetime

import pandas_datareader.data as web

start = datetime.datetime(1949, 1, 1)
end = datetime.datetime(2018, 5, 16)
tsd = web.DataReader('SPY', 'morningstar', start, end)
print(tsd.head(1))
print(tsd.tail(1))
vix = tsd.copy(1)
vix.plot()

# import pandas_datareader.data as web
# import datetime
# import matplotlib.pyplot as plt
#
# start = datetime.datetime(2012, 1, 1)
# end = datetime.datetime(2017, 12, 31)
#
# f = web.DataReader('SNE', 'morningstar', start, end)
#
# print(f.head())
