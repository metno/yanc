Yet another NetCDF checker
==========================

Template
--------

The template file understands the following keywords:

.. code-block:: bash

   dimensions:
   - name: time
       length: 15
   - name: x
       min_length: 10
       max_length: 20

   variables:
   - name: air_temperature
     min: 200
     max: 400
     units: K
     '% missing': 10
     missing_timesteps: [0,1,2]

Dimensions can be checked for an exact length (by using the work 'length') or a range of
lengths (inclusively, by using 'min_length' and 'max_length').

Neither 'dimensions' nor 'variables' are required to be present in the file.

Return codes
------------
The program returns 0 if the file is valid. Otherwise a non-zero code is returned. If the template
file is missing or contains invalid YAML, or if the NetCDF file does not exist or is invalid NetCDF,
then a non-zero code is returned.

Missing values
--------------

By default, variables are not allowed to have missing values. To allow a missing values, the '%
missing' can be added, which means the test will fail if there the percentage of missing values
exceeds the allowed value. Some variables (such as precipitation_amount) will have have missing
values on the first timestep. Data in timesteps specified by missing_timesteps will not count
towards the percentage missing.

For example, the following requires the precipitation_amount variable to have no missing values
except for the first time step:

.. code-block:: bash

   variables:
   - name: precipitation_amount
     units: m
     '% missing': 0
     missing_timesteps: 0

missing_timesteps can also be an array like this:

.. code-block:: bash

   variables:
   - name: precipitation_amount
     units: m
     '% missing': 0
     missing_timesteps: [0, 1, 2]

Example
-------

.. code-block:: bash

   python yanc.py --ncfile http://thredds.met.no/thredds/dodsC/meps25files/meps_det_pp_2_5km_latest.nc \
   --template templates/meps_det_pp.yml
