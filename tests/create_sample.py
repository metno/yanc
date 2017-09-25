import netCDF4
import numpy as np


"""
This creates the sample file used by the tests
"""
fid = netCDF4.Dataset("sample.nc", "w")
fid.createDimension("time")
fid.createDimension("x", 5)
fid.createDimension("y", 2)

v_time = fid.createVariable("time", "f8", ("time"))
v_frt = fid.createVariable("forecast_reference_time", "f8", ())
v_x = fid.createVariable("x", "i4", ("x"))
v_y = fid.createVariable("y", "i4", ("y"))
v_temp = fid.createVariable("air_temperature_2m", "f4", ("time", "y", "x"))
v_precip = fid.createVariable("precipitation_amount", "f4", ("time", "y", "x"))

v_time[:] = np.arange(1483228800, 1483228800 + 3600*25, step=3600)
v_time.units = "seconds since 1970-01-01 00:00:00 +00:00"
v_frt[:] = 1483228800
v_frt.units = "seconds since 1970-01-01 00:00:00 +00:00"
v_x[:] = np.arange(0, 5000, step=1000)
v_y[:] = np.arange(0, 2000, step=1000)
v_temp[:] = np.random.rand(25, 2, 5)*40 + 253
v_temp.units = "K"

# Add missing values to the first time step for precipitation
precip = np.random.rand(25, 2, 5)*10 * (np.random.rand(25, 2, 5) < 0.3)
precip[0, :, :] = np.nan
v_precip[:] = precip
v_precip.units = "mm"

fid.close()
