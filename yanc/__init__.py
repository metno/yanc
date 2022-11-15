import netCDF4
import numpy as np
import argparse
import yaml
import sys
import os

NOT_OK = 1
OK = 0


def check_nc_file_against_template(ncfile, template, debug):

    if not os.path.exists(template):
        print("File '{}' is missing.".format(template))
        return NOT_OK

    with open(template, 'r') as s:
        try:
            check_params = yaml.safe_load(s)
        except yaml.YAMLError as e:
            print(e)
            return NOT_OK

    try:
        dataset = netCDF4.Dataset(ncfile, "r")
    except Exception:
        print("File '{}' is missing.".format(ncfile))
        return NOT_OK

    if 'dimensions' in check_params:
       for dimension in check_params['dimensions']:
           name = dimension['name']
           if debug:
               print("Parsing dimension '{}'".format(name))
           if name not in dataset.dimensions.keys():
               print("Dimension '{}' missing in the NetCDF file.".format(name))
               return NOT_OK
           val = len(dataset.dimensions[name])
           if 'length' in dimension:
               if val != dimension['length']:
                   print("Dimension length ({}) for  '{}' is not equal to {}".format(len(dataset.dimensions[name]), name, dimension['length']))
                   return NOT_OK
           if 'min_length' in dimension:
               if val < dimension['min_length']:
                   print("Dimension length ({}) for  '{}' is less than {}".format(len(dataset.dimensions[name]), name, dimension['min_length']))
                   return NOT_OK
           if 'max_length' in dimension:
               if val > dimension['max_length']:
                   print("Dimension length ({}) for  '{}' is greater than {}".format(len(dataset.dimensions[name]), name, dimension['max_length']))
                   return NOT_OK

    if 'variables' in check_params:
        for variable in check_params['variables']:
            name = variable['name']
            if debug:
                print("Parsing variable '{}'".format(name))
            """
            Check variable metadata
            """
            if name not in dataset.variables.keys():
                print("Variable '{}' missing in the NetCDF file.".format(name))
                return NOT_OK
            if 'units' in variable:
                if not hasattr(dataset.variables[name], 'units'):
                    print("Variable '{}' missing 'units' attribute.".format(name))
                    return NOT_OK
                if variable['units'] != dataset.variables[name].units:
                    print(("Wrong units of the '{}' variable.").format(name))
                    print("Expected: '{}'".format(variable['units']))
                    print("Found:    '{}'".format(dataset.variables[name].units))
                    return NOT_OK

            """
            Check missing values

            For non-scalar values, ignore timesteps in 'missing_timesteps'
            """
            values = dataset.variables[name]

            # Percent missing values
            allowed_missing_percent = 0.0  # Default value
            if '% missing' in variable:
                allowed_missing_percent = float(variable["% missing"])

            # Bypass the checks on the values if possible, to save time
            if allowed_missing_percent == 100 and 'min' not in variable and 'max' not in variable:
                if debug:
                    print("Bypassing reading of values for '{}'".format(name))
                continue

            missing_timesteps = []

            # Variables that are not scalars
            if len(values.shape) > 0:
                timesteps = range(values.shape[0])
                if "missing_timesteps" in variable:
                    allowed_missing_timesteps = variable["missing_timesteps"]
                    if not isinstance(allowed_missing_timesteps, (list, tuple)):
                        allowed_missing_timesteps = [allowed_missing_timesteps]
                    timesteps = [t for t in timesteps if t not in allowed_missing_timesteps]
                num_valid = np.ma.count(values[timesteps, ...])
                num_total = np.product(values[timesteps, ...].shape)
                val = (num_total - num_valid) / 1.0 / num_total * 100

            # Scalar variables
            else:
                val = (np.ma.count(values[:]) == 0) * 100

            if val > allowed_missing_percent:
                print("Missing values ({}%) for '{}' is higher than {}%".format(val, name, allowed_missing_percent))
                return NOT_OK

            """
            Check that values are within bounds. Here we ignore the missing values, since we only
            used the non-masked part.
            """
            if 'min' in variable:
                val = np.min(values[:])
                if variable['min'] > val:
                    print("Minimum value ({}) for '{}' is lower than {}".format(val, name, variable['min']))
                    return NOT_OK

            if 'max' in variable:
                val = np.max(values[:])
                if variable['max'] < val:
                    print("Maximum value ({}) for '{}' is higher than {}".format(val, name, variable['max']))
                    return NOT_OK

    return OK


def run(args):
    helptext = "Check a NetCDF file against a template specifying variables and their properties."
    parser = argparse.ArgumentParser(prog="yanc", description=helptext)
    parser.add_argument('--ncfile', required=True, help='Name of the input NetCDF file.')
    parser.add_argument('--template', required=True, help="Name of the file with parametrized checks.")
    parser.add_argument('--debug', help="Show debug information", action="store_true")
    parser.add_argument('--version', action="version", version="%(prog)s 0.1.0")
    args = parser.parse_args(args)

    return_code = check_nc_file_against_template(args.ncfile, args.template, args.debug)
    sys.exit(return_code)


def main():
   run(sys.argv[1:])

if __name__ == "__main__":
    main()
