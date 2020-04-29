#! /usr/bin/env python3
'''
Implementation of the "PhylogeneticInference" module that does nothing
'''
from PhylogeneticInference import PhylogeneticInference
import ViReport_GlobalContext as GC

class PhylogeneticInference_None(PhylogeneticInference):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def blurb():
        return "Phylogenetic inference was not performed."

    def infer_phylogeny(aln_filename):
        return None
