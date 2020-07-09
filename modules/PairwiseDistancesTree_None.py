#! /usr/bin/env python3
'''
Implementation of the "PairwiseDistancesTree" module using tn93
'''
from PairwiseDistancesTree import PairwiseDistancesTree
import ViReport_GlobalContext as GC

class PairwiseDistancesTree_None(PairwiseDistancesTree):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def blurb():
        return "Pairwise distances were not computed from the phylogeny."

    def pairwise_distances(tree_filename):
        return None
