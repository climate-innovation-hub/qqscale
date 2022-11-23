"""Command line program for calculating QQ-scaling adjustment factors."""

import argparse
import logging

from xclim import sdba
import xesmf as xe
import dask.diagnostics

import utils


def main(args):
    """Run the program."""
    
    dask.diagnostics.ProgressBar().register()
    
    ds_hist = utils.read_data(
        args.hist_files,
        args.hist_var,
        time_bounds=args.hist_time_bounds,
        input_units=args.input_hist_units,
        output_units=args.output_units,
        ssr=args.ssr,
    )
    ds_ref = utils.read_data(
        args.ref_files,
        args.ref_var,
        time_bounds=args.ref_time_bounds,
        input_units=args.input_ref_units,
        output_units=args.output_units,
        ssr=args.ssr,
    )

    if len(ds_hist['lat']) != len(ds_ref['lat']):
        regridder = xe.Regridder(ds_hist, ds_ref, "bilinear")
        ds_hist = regridder(ds_hist)
    
    mapping_methods = {'additive': '+', 'multiplicative': '*'}
    qm = sdba.EmpiricalQuantileMapping.train(
        ds_ref[args.ref_var],
        ds_hist[args.hist_var],
        nquantiles=100,
        group="time.month",
        kind=mapping_methods[args.method]
    )
        
    #output the reference quantiles, which aren't included by xclim
    qm_reverse = sdba.EmpiricalQuantileMapping.train(
        ds_hist[args.hist_var],
        ds_ref[args.ref_var],
        nquantiles=100,
        group="time.month",
        kind=mapping_methods[args.method]
    )
    qm.ds['ref_q'] = qm_reverse.ds['hist_q']
    
    qm.ds['hist_q'].attrs['units'] = args.output_units
    qm.ds['ref_q'].attrs['units'] = args.output_units
    qm.ds = qm.ds.assign_coords({'lat': ds_ref['lat'], 'lon': ds_ref['lon']}) #xclim strips lat/lon attributes
    qm.ds = qm.ds.transpose('quantiles', 'month', 'lat', 'lon')

    qm.ds.attrs['history'] = utils.get_new_log()
    qm.ds.attrs['historical_period_start'] = args.hist_time_bounds[0]
    qm.ds.attrs['historical_period_end'] = args.hist_time_bounds[1]
    qm.ds.attrs['reference_period_start'] = args.ref_time_bounds[0]
    qm.ds.attrs['reference_period_end'] = args.ref_time_bounds[1]
    qm.ds.to_netcdf(args.output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        argument_default=argparse.SUPPRESS,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )          
    parser.add_argument("hist_var", type=str, help="historical variable to process")
    parser.add_argument("ref_var", type=str, help="reference variable to process")
    parser.add_argument("output_file", type=str, help="output file")
    parser.add_argument(
        "--hist_files",
        type=str,
        nargs='*',
        required=True,
        help="historical data files"
    )
    parser.add_argument(
        "--ref_files",
        type=str,
        nargs='*',
        required=True,
        help="reference data files"
    )
    parser.add_argument(
        "--hist_time_bounds",
        type=str,
        nargs=2,
        metavar=('START_DATE', 'END_DATE'),
        required=True,
        help="historical time bounds in YYYY-MM-DD format"
    )
    parser.add_argument(
        "--ref_time_bounds",
        type=str,
        nargs=2,
        metavar=('START_DATE', 'END_DATE'),
        required=True,
        help="reference time bounds in YYYY-MM-DD format"
    )
    parser.add_argument(
        "--method",
        type=str,
        choices=('additive', 'multiplicative'),
        default='additive',
        help="scaling method",
    )
    parser.add_argument(
        "--input_hist_units",
        type=str,
        default=None,
        help="input historical data units"
    )
    parser.add_argument(
        "--input_ref_units",
        type=str,
        default=None,
        help="input reference data units"
    )
    parser.add_argument(
        "--output_units",
        type=str,
        default=None,
        help="output data units"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help='Set logging level to DEBUG',
    )
    parser.add_argument(
        "--ssr",
        action="store_true",
        default=False,
        help='Apply Singularity Stochastic Removal',
    )
    args = parser.parse_args()
    log_level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(level=log_level)
    main(args)
