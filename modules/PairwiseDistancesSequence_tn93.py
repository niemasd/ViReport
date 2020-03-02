#! /usr/bin/env python3
'''
Implementation of the "PairwiseDistancesSequence" module using tn93
'''
from PairwiseDistancesSequence import PairwiseDistancesSequence
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import call,DEVNULL

class PairwiseDistancesSequence_tn93(PairwiseDistancesSequence):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_HIVTRACE

    def blurb():
        return "Pairwise distances were computed from the multiple sequence alignment using the tn93 tool of HIV-TRACE (Pond et al., 2018)."

    def pairwise_distances(aln_filename):
        if not isfile(aln_filename):
            raise ValueError("Invalid alignment file: %s" % aln_filename)
        tn93_dir = '%s/tn93' % GC.OUT_DIR_TMPFILES
        makedirs(tn93_dir, exist_ok=True)
        out_filename = '%s/pairwise_distances_sequence.csv' % GC.OUT_DIR_OUTFILES
        log = open('%s/log.txt' % tn93_dir, 'w')
        command = ['tn93', '-t', '1', '-l', '1', '-q', '-o', out_filename, aln_filename]
        f = open('%s/command.txt' % tn93_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
        call(command, stdout=log, stderr=DEVNULL)
        log.close()
        return out_filename