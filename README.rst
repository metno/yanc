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
     '% missing': 0
     missing_timesteps: [0,1,2]

Dimensions can be checked for an exact length (by using the work 'length') or a range of
lengths (inclusively, by using 'min_length' and 'max_length').

'missing_timeteps' allows the specified timesteps to be missing.

Neither 'dimensions' nor 'variables' are required to be present in the file.
