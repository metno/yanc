import argparse
import yanc
import sys


def main(args=None):
    helptext = "Check a NetCDF file against a template specifying variables and their properties."
    parser = argparse.ArgumentParser(prog="yanc", description=helptext)
    parser.add_argument('--ncfile', required=True, help='Name of the input NetCDF file.')
    parser.add_argument('--template', required=True, help="Name of the file with parametrized checks.")
    parser.add_argument('--debug', help="Show debug information", action="store_true")
    parser.add_argument('--version', action="version", version="%(prog)s " + yanc.__version__)
    args = parser.parse_args(args)

    return_code = yanc.check_nc_file_against_template(args.ncfile, args.template, args.debug)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
