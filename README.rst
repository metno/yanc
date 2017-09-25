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
