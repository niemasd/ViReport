#! /usr/bin/env python3
'''
Convert sample dates between different formats
'''
from datetime import datetime
from gzip import open as gopen
from sys import stdin,stdout
import argparse

def date_to_days(sample_time):
    num_dashes = sample_time.count('-')
    if num_dashes == 2:   # YYYY-MM-DD
        tmp = datetime.strptime(sample_time, '%Y-%m-%d')
    elif num_dashes == 1: # YYYY-MM(-01)
        tmp = datetime.strptime('%s-01' % sample_time, '%Y-%m-%d')
    elif num_dashes == 0: # YYYY(-01-01)
        tmp = datetime.strptime('%s-01-01' % sample_time, '%Y-%m-%d')
    else:
        raise ValueError("Invalid sample date (should be YYYY-MM-DD): %s" % sample_time)
    return (tmp - datetime(1,1,1)).days # days since 0001-01-01

def input_dates_vireport(lines):
    return [[v.strip() for v in l.strip().split('\t')] for l in lines if len(l.strip()) != 0]

def output_dates_vireport(vireport_dates):
    return vireport_dates

def output_dates_lsd(vireport_dates):
    return "%d\n%s" % (len(vireport_dates), '\n'.join("%s %s" % (u,date_to_days(t)) for u,t in vireport_dates))

def output_dates_treedater(vireport_dates):
    return '\n'.join("%s,%s" % (u,date_to_days(t)) for u,t in vireport_dates)

INPUT = {
    'vireport': input_dates_vireport,
}

OUTPUT = {
    'lsd': output_dates_lsd,
    'treedater': output_dates_treedater,
    'vireport': output_dates_vireport,
}

if __name__ == "__main__":
    # parse args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input File")
    parser.add_argument('-if', '--input_format', required=True, type=str, help="Input Format (options: %s)" % ', '.join(sorted(INPUT.keys())))
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File (LSD format)")
    parser.add_argument('-of', '--output_format', required=True, type=str, help="Output Format (options: %s)" % ', '.join(sorted(OUTPUT.keys())))
    args = parser.parse_args()
    args.input_format = args.input_format.lower().strip()
    if args.input_format not in INPUT:
        raise ValueError("Invalid input format: %s" % args.input_format)
    args.output_format = args.output_format.lower().strip()
    if args.output_format not in OUTPUT:
        raise ValueError("Invalid output format: %s" % args.output_format)
    if args.input == 'stdin':
        lines = [l.strip() for l in stdin.read().strip().splitlines()]
    elif args.input.lower().endswith('.gz'):
        lines = [l.strip() for l in gopen(args.input).read().decode().strip().splitlines()]
    else:
        lines = [l.strip() for l in open(args.input).read().strip().splitlines()]
    GZIP_OUT = False
    if args.output == 'stdout':
        out = stdout
    elif args.output.lower().endswith('.gz'):
        out = gopen(args.output, 'wb', 9); GZIP_OUT = True
    else:
        out = open(args.output, 'w')

    # convert dates
    input_times = INPUT[args.input_format](lines)
    output_times = OUTPUT[args.output_format](input_times)
    if GZIP_OUT:
        output_times = output_times.encode()
    out.write(output_times); out.close()
