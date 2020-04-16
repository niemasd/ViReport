#! /usr/bin/env python3
'''
ViReport: Automated workflow for performing standard viral phylogenetic analyses and generating a report
'''
import argparse
from multiprocessing import cpu_count
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
    'Logging': 'FileSTDOUT',
    'MultipleSequenceAlignment': 'MAFFT',
    'PairwiseDistancesSequence': 'tn93',
    'PairwiseDistancesTree': 'TreeSwift',
    'PhylogeneticInference': 'IQTREEMFP',
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
    'Logging': 'log',
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
    parser.add_argument('-r', '--reference_id', required=False, default=None, type=str, help="Reference Genome ID")
    parser.add_argument('-t', '--times', required=True, type=str, help="Sample Times (TSV format)")
    parser.add_argument('-c', '--categories', required=False, default=None, type=str, help="Sample Categories (TSV format)")
    parser.add_argument('-og', '--outgroups', required=False, default=None, type=str, help="List of Outgroups")
    parser.add_argument('-o', '--out_dir', required=True, type=str, help="Output Directory")
    parser.add_argument('-mt', '--max_threads', action='store_true', help="Use Maximum Number of Threads")
    parser.add_argument('-gz', '--gzip_output', action='store_true', help="Gzip Large Output Files")
    parser.add_argument('--continue_workflow', action='store_true', help="Continue Workflow Execution")
    for arg in ARG_TO_MODULE:
        parser.add_argument('--%s'%arg, required=False, type=str, default=DEFAULT[ARG_TO_MODULE[arg]], help="%s Module" % ARG_TO_MODULE[arg])
    args = parser.parse_args()
    if args.max_threads:
        GC.NUM_THREADS = cpu_count()
    else:
        GC.NUM_THREADS = None
    GC.REF_ID = args.reference_id
    GC.GZIP_OUTPUT = args.gzip_output

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
    if args.categories is not None:
        if not isfile(args.categories):
            raise ValueError("Sample categories file not found: %s" % args.categories)
        args.categories = expanduser(abspath(args.categories))

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
        if isfile(GC.OUT_DIR):
            raise ValueError("Output destination exists as a file: %s" % GC.OUT_DIR)
        if isdir(GC.OUT_DIR) and not args.continue_workflow:
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
    if args.categories is None:
        GC.OUT_DIR_INFILES_CATEGORIES = None
    else:
        GC.OUT_DIR_INFILES_CATEGORIES = "%s/%s" % (GC.OUT_DIR_INFILES, args.categories.split('/')[-1])
        copyfile(args.categories, GC.OUT_DIR_INFILES_CATEGORIES)

if __name__ == "__main__":
    # initialize ViReport
    MF.init('/'.join(argv[0].split('/')[:-1]) + '/modules')

    # parse user arguments
    parse_args()
    GC.VIREPORT_COMMAND = ' '.join(argv)

    # run Driver
    GC.SELECTED['Driver'].run(GC.OUT_DIR_INFILES_SEQS, GC.REF_ID, GC.OUT_DIR_INFILES_TIMES, GC.OUT_DIR_INFILES_OUTGROUPS, GC.OUT_DIR_INFILES_CATEGORIES)
