#! /usr/bin/env python3
'''
ViReport: Automated workflow for performing standard viral phylogenetic analyses and generating a report
'''
import argparse
from warnings import warn
from os import environ,makedirs
from os.path import abspath,expanduser,isdir,isfile
from shutil import copyfile,rmtree
from sys import argv,path

# set up path
path.append('%s/modules' % abspath(expanduser('/'.join(argv[0].split('/')[:-1]))))
import ViReport_GlobalContext as GC
import ViReport_ModuleFactory as MF

# set defaults
DEFAULT = {
    'AncestralSequenceReconstruction': 'TreeTime',
    'Dating': 'treedater',
    'Driver': 'Default',
    'MultipleSequenceAlignment': 'MAFFT',
    'PairwiseDistancesSequence': 'tn93',
    'PairwiseDistancesTree': 'TreeSwift',
    'PhylogeneticInference': 'IQTREE',
    'Preprocessing': 'SafeNames',
    'ReportFormat': 'All',
    'Rooting': 'MinVar',
    'TransmissionClustering': 'TreeN93TreeDists',
    'WriteReport': 'Default',
}

# map module names to CLI args
MODULE_TO_ARG = {
    'AncestralSequenceReconstruction': 'ancestral',
    'Dating': 'date',
    'Driver': 'driver',
    'MultipleSequenceAlignment': 'msa',
    'PairwiseDistancesSequence': 'dists_seq',
    'PairwiseDistancesTree': 'dists_tree',
    'PhylogeneticInference': 'phylo',
    'Preprocessing': 'preprocess',
    'ReportFormat': 'format',
    'Rooting': 'root',
    'TransmissionClustering': 'trans_clust',
    'WriteReport': 'report',
}
ARG_TO_MODULE = {MODULE_TO_ARG[k]:k for k in MODULE_TO_ARG}

def parse_args():
    '''
    Parse user arguments
    '''
    if not hasattr(MF,'MODULES'):
        raise RuntimeError("Initialize the ModuleFactory before parsing user arguments")

    # use argparse to parse user arguments
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--sequences', required=True, type=str, help="Input Sequences (FASTA format)")
    parser.add_argument('-t', '--times', required=True, type=str, help="Sample Times (TSV format)")
    parser.add_argument('-og', '--outgroups', required=False, default=None, type=str, help="List of Outgroups")
    parser.add_argument('-o', '--out_dir', required=True, type=str, help="Output Directory")
    parser.add_argument('-f', '--force_overwrite', action='store_true', help="Force Overwrite of Output")
    for arg in ARG_TO_MODULE:
        parser.add_argument('--%s'%arg, required=False, type=str, default=DEFAULT[ARG_TO_MODULE[arg]], help="%s Module" % ARG_TO_MODULE[arg])
    args = parser.parse_args()

    # check input files
    if not isfile(args.sequences):
        raise ValueError("Sequence file not found: %s" % args.sequences)
    args.sequences = expanduser(abspath(args.sequences))
    if not isfile(args.times):
        raise ValueError("Sample time file not found: %s" % args.times)
    args.times = expanduser(abspath(args.times))
    if args.outgroups is not None:
        if not isfile(args.outgroups):
            raise ValueError("Outgroups file not found: %s" % args.outgroups)
        args.outgroups = expanduser(abspath(args.outgroups))

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
        if isdir(GC.OUT_DIR) or isfile(GC.OUT_DIR):
            if args.force_overwrite:
                warn("Overwriting output directory: %s" % GC.OUT_DIR)
                rmtree(GC.OUT_DIR)
            else:
                raise ValueError("Output folder exits: %s" % GC.OUT_DIR)
    makedirs(GC.OUT_DIR, exist_ok=True)

    # copy input files to output directory
    GC.OUT_DIR_INFILES = "%s/input_files" % GC.OUT_DIR
    GC.OUT_DIR_INFILES_SEQS = "%s/%s" % (GC.OUT_DIR_INFILES, args.sequences.split('/')[-1])
    GC.OUT_DIR_INFILES_TIMES = "%s/%s" % (GC.OUT_DIR_INFILES, args.times.split('/')[-1])
    makedirs(GC.OUT_DIR_INFILES, exist_ok=True)
    copyfile(args.sequences, GC.OUT_DIR_INFILES_SEQS)
    copyfile(args.times, GC.OUT_DIR_INFILES_TIMES)
    if args.outgroups is None:
        GC.OUT_DIR_INFILES_OUTGROUPS = None
    else:
        GC.OUT_DIR_INFILES_OUTGROUPS = "%s/%s" % (GC.OUT_DIR_INFILES, args.outgroups.split('/')[-1])
        copyfile(args.outgroups, GC.OUT_DIR_INFILES_OUTGROUPS)

if __name__ == "__main__":
    # initialize ViReport
    MF.init('/'.join(argv[0].split('/')[:-1]) + '/modules')

    # parse user arguments
    parse_args()
    GC.VIREPORT_COMMAND = ' '.join(argv)

    # run Driver
    GC.SELECTED['Driver'].run(GC.OUT_DIR_INFILES_SEQS, GC.OUT_DIR_INFILES_TIMES, GC.OUT_DIR_INFILES_OUTGROUPS)
