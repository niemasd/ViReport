#! /usr/bin/env python3
'''
ViReport: Automated workflow for performing standard viral phylogenetic analyses and generating a report
'''
from modules import ViReport_GlobalContext as GC
from modules import ViReport_ModuleFactory as MF
import argparse
from os import environ
from os.path import abspath,expanduser,isdir
from sys import argv

# set defaults
DEFAULT = {
    'Driver': 'Default',
}

# map module names to CLI args
MODULE_TO_ARG = {
    'Driver': 'driver',
    'Preprocessing': 'preprocess',
    'MultipleSequenceAlignment': 'msa',
}
ARG_TO_MODULE = {MODULE_TO_ARG[k]:k for k in MODULE_TO_ARG}

def parse_args():
    '''
    Parse user arguments
    '''
    assert hasattr(MF,'MODULES'), "Initialize the ModuleFactory before parsing user arguments"

    # use argparse to parse user arguments
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--out_dir', required=True, type=str, help="Output Directory")
    args = parser.parse_args()

    # if running in Docker image, hardcode output directory
    if 'VIREPORT_DOCKER' in environ:
        GC.OUT_DIR = '/VIREPORT_MOUNT/OUT_DIR'
        GC.OUT_DIR_PRINT = environ['out_dir_print']
    else:
        GC.OUT_DIR = expanduser(abspath(args.out_dir))
        GC.OUT_DIR_PRINT = GC.OUT_DIR

if __name__ == "__main__":
    # initialize ViReport
    MF.init('/'.join(argv[0].split('/')[:-1]) + '/modules')

    # parse user arguments
    parse_args()
    print(MF.MODULES)
