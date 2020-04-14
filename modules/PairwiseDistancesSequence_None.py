#! /usr/bin/env python3
'''
Implementation of the "PairwiseDistancesSequence" module using tn93
'''
from PairwiseDistancesSequence import PairwiseDistancesSequence
import ViReport_GlobalContext as GC

class PairwiseDistancesSequence_None(PairwiseDistancesSequence):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def blurb():
        return "Pairwise distances were not computed from the multiple sequence alignment."

    def pairwise_distances(aln_filename):
        return None
