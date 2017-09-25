import netCDF4
import numpy as np
import argparse
import yaml
import sys

NOT_OK = 1
OK = 0

def check_nc_file_against_template(ncfile, template, debug):

    with open(template, 'r') as s:
        try:
            check_params = yaml.load(s)
        except yaml.YAMLError as e:
            print(e)

    dataset = netCDF4.Dataset(ncfile, "r")

    for dimension in check_params['dimensions']:
        name = dimension['name']
        if debug:
            print("Parsing dimension '{}'".format(name))
        if name not in dataset.dimensions.keys():
            print("Variable '{}' missing in the NetCDF file.".format(name))
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
        if 'unit' in variable and variable['unit'] != dataset.variables[name].units:
            print("Variable '{}' missing in the NetCDF file.".format(name))
            return NOT_OK

        """
        Check variable values
        """
        values = dataset.variables[name]
        if '% missing' in variable:
            val = np.mean(np.isnan(values)) * 100
            if variable['% missing'] < val:
                print("% missing values ({}) for '{}' is higher than {}".format(val, name, variable['% missing']))
                return NOT_OK
        if 'min' in variable:
            val = np.min(values)
            if variable['min'] > val:
                print("Minimum value ({}) for '{}' is lower than {}".format(val, name, variable['min']))
                return NOT_OK
        if 'max' in variable:
            val = np.max(values)
            if variable['max'] < np.max(values):
                print("Maximum value ({}) for '{}' is higher than {}".format(val, name, variable['max']))
                return NOT_OK

    return OK

def run(args):
    helptext = "Check a NetCDF file against a template specifying variables and their properties."
    parser = argparse.ArgumentParser(prog="yanc", description=helptext)
    parser.add_argument('--ncfile', required=True, help='Name of the input NetCDF file.')
    parser.add_argument('--template', required=True, help="Name of the file with parametrized checks.")
    parser.add_argument('--debug', help="Show debug information", action="store_true")
    args = parser.parse_args(args)

    return_code = check_nc_file_against_template(args.ncfile, args.template, args.debug)
    sys.exit(return_code)

def main():
   run(sys.argv[1:])

if __name__ == "__main__":
    main()
