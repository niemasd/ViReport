#! /usr/bin/env python3
'''
Implementation of the "Preprocessing" module where sequences are given safe names (non-letters/digits --> underscore)
'''
from Preprocessing import Preprocessing
import ViReport_GlobalContext as GC
from os.path import isfile

class Preprocessing_SafeNames(Preprocessing):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def blurb():
        return "The input dataset was preprocessed such that sequences were given safe names: non-letters/digits in sequence IDs were converted to underscores."

    def preprocess(seqs_filename, sample_times_filename):
        # set things up
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        if not isfile(sample_times_filename):
            raise ValueError("Invalid sample times file: %s" % sample_times_filename)
        out_seqs_filename = '%s/sequences_safe.fas' % GC.OUT_DIR_OUTFILES
        out_times_filename = '%s/times_safe.txt' % GC.OUT_DIR_OUTFILES

        # output safe sequences
        f = open(out_seqs_filename, 'w')
        for line in open(seqs_filename):
            l = line.strip()
            if len(l) == 0:
                continue
            elif l[0] == '>':
                f.write('>'); f.write(GC.safe(l[1:]))
            else:
                f.write(l)
            f.write('\n')
        f.close()

        # output safe sample times
        f = open(out_times_filename, 'w')
        for line in open(sample_times_filename):
            parts = [v.strip() for v in line.strip().split('\t')]
            if len(parts) == 2:
                f.write(GC.safe(parts[0])); f.write('\t'); f.write(parts[1])
            else:
                raise ValueError("Invalid sample times file: %s" % sample_times_filename)
            f.write('\n')
        f.close()

        # return output filenames
        return out_seqs_filename, out_times_filename
