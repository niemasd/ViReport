#! /usr/bin/env python3
'''
Default implementation of the "Driver" module
'''
from Driver import Driver
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile

def print_message():
    '''
    Print author message
    '''
    title = "ViReport v%s" % GC.VIREPORT_VERSION
    devel = "Niema Moshiri 2020"
    l = max(len(title),len(devel))
    print("/-%s-\\" % ('-'*l))
    for e in (title,devel):
        lpad = int((l-len(e))/2)
        rpad = l - lpad - len(e)
        print("| %s%s%s |" % (lpad*' ',e,rpad*' '))
    print("\\-%s-/\n" % ('-'*l))

class Driver_Default(Driver):
    def init():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def run(seqs_filename, sample_times_filename):
        # print starting messages
        print_message()
        print("Output directory: %s" % GC.OUT_DIR_PRINT)
        print("Starting viral analysis workflow...")

        # check input files
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        if not isfile(sample_times_filename):
            raise ValueError("Invalid sample times file: %s" % sample_times_filename)
        GC.INPUT_SEQS = seqs_filename; GC.INPUT_TIMES = sample_times_filename

        # set up output and intermediate folders
        GC.OUT_DIR_OUTFILES = "%s/output_files" % GC.OUT_DIR
        makedirs(GC.OUT_DIR_OUTFILES, exist_ok=True)
        GC.OUT_DIR_TMPFILES = "%s/intermediate_files" % GC.OUT_DIR
        makedirs(GC.OUT_DIR_TMPFILES, exist_ok=True)

        # run preprocessing
        print("\nRunning '%s'..." % GC.SELECTED['Preprocessing'].__name__)
        GC.PROCESSED_SEQS, GC.PROCESSED_TIMES = GC.SELECTED['Preprocessing'].preprocess(GC.INPUT_SEQS, GC.INPUT_TIMES)
        print("Preprocessed sequence output to: %s" % GC.PROCESSED_SEQS)
        print("Preprocessed sample times output to: %s" % GC.PROCESSED_TIMES)

        # align the preprocessed sequences
        print("\nRunning '%s'..." % GC.SELECTED['MultipleSequenceAlignment'].__name__)
        GC.ALIGNMENT = GC.SELECTED['MultipleSequenceAlignment'].align(GC.PROCESSED_SEQS)
        print("Multiple sequence alignment output to: %s" % GC.ALIGNMENT)
