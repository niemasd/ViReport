#! /usr/bin/env python3
'''
Implementation of the "MultipleSequenceAlignment" module using MAFFT
'''
from MultipleSequenceAlignment import MultipleSequenceAlignment

class MultipleSequenceAlignment_MAFFT(MultipleSequenceAlignment):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_MAFFT

    def align(seqs_filename):
        assert False, "Need to implement"
