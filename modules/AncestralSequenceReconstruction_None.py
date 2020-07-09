#! /usr/bin/env python3
'''
Implementation of the "AncestralSequenceReconstruction" module that does nothing
'''
from AncestralSequenceReconstruction import AncestralSequenceReconstruction
import ViReport_GlobalContext as GC

class AncestralSequenceReconstruction_None(AncestralSequenceReconstruction):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def blurb():
        return "Ancestral sequence reconstruction was not performed."

    def reconstruct(rooted_tree_filename, aln_filename):
        return None
