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
    'Preprocessing': 'None',
    'MultipleSequenceAlignment': 'MAFFT',
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
    for arg in ARG_TO_MODULE:
        parser.add_argument('--%s'%arg, required=False, type=str, default=DEFAULT[ARG_TO_MODULE[arg]], help="%s Module" % ARG_TO_MODULE[arg])
    args = parser.parse_args()

    # parse module implementation selections
    GC.SELECTED = dict()
    for arg in ARG_TO_MODULE:
        mod = ARG_TO_MODULE[arg]; mod_selection = getattr(args, arg)
        if mod_selection not in MF.MODULES[mod]:
            raise ValueError("Invalid %s: %s\n* Valid Options: %s" % (mod, mod_selection, ', '.join(sorted(MF.MODULES[mod]))))
        GC.SELECTED[mod] = MF.MODULES[mod][mod_selection]

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

    # run Driver
    GC.SELECTED['Driver'].run()
