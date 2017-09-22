import netCDF4
import numpy as np
import argparse
import yaml
import sys

NOT_OK = 1
OK = 0

def check_nc_file_against_template(ncfile, template):

    dataset = netCDF4.Dataset(ncfile, "r")

    with open(template, 'r') as s:
        try:
            check_params = yaml.load(s)
        except yaml.YAMLError as e:
            print(e)

    for variable in check_params['variables']:
        if variable['name'] not in dataset.variables.keys():
            print("Variable '{}' missing in the NetCDF file.".format(variable['name']))
            return NOT_OK

    return OK

def main():

    helptext = "Check a NetCDF file against a template specifying variables and their properties."
    parser = argparse.ArgumentParser(prog="yanc", description=helptext)
    parser.add_argument('--ncfile', required=True, help='Name of the input NetCDF file.')
    parser.add_argument('--template', required=True, help="Name of the file with parametrized checks.")
    args = parser.parse_args()

    return_code = check_nc_file_against_template(args.ncfile, args.template)
    sys.exit(return_code)

if __name__ == "__main__":
    main()
