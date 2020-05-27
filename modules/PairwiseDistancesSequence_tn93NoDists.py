#! /usr/bin/env python3
'''
Implementation of the "PairwiseDistancesSequence" module using tn93, but without outputting the pairwise distances themselves (only the summary results)
'''
from PairwiseDistancesSequence import PairwiseDistancesSequence
from PairwiseDistancesSequence_tn93 import PairwiseDistancesSequence_tn93
import ViReport_GlobalContext as GC
from os import devnull,makedirs
from os.path import isfile
from subprocess import check_output

class PairwiseDistancesSequence_tn93NoDists(PairwiseDistancesSequence):
    def init():
        PairwiseDistancesSequence_tn93.init()

    def finalize():
        PairwiseDistancesSequence_tn93.finalize()

    def cite():
        return PairwiseDistancesSequence_tn93.cite()

    def blurb():
        return PairwiseDistancesSequence_tn93.blurb()

    def pairwise_distances(aln_filename):
        if not isfile(aln_filename):
            raise ValueError("Invalid alignment file: %s" % aln_filename)
        tn93_dir = '%s/tn93' % GC.OUT_DIR_TMPFILES
        GC.PAIRWISE_DISTS_SEQS_SUMMARY = '%s/pairwise_distances_sequence_summary.json' % GC.OUT_DIR_OUTFILES
        if isfile(GC.PAIRWISE_DISTS_SEQS_SUMMARY):
            GC.SELECTED['Logging'].writeln("Pairwise sequence distances exist. Skipping recomputation.")
        else:
            makedirs(tn93_dir, exist_ok=True)
            prog = open('%s/log.txt' % tn93_dir, 'w')
            command = ['tn93', '-t', '1', '-l', '1', '-o', devnull]
            f = open('%s/command.txt' % tn93_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            o = check_output(command, input='\n'.join(GC.read_file(aln_filename)).encode(), stderr=prog)
            prog.close()
            f = open(GC.PAIRWISE_DISTS_SEQS_SUMMARY, 'wb'); f.write(o); f.close()
        return None
