#! /usr/bin/env python3
'''
Implementation of the "Dating" module that does nothing
'''
from Dating import Dating
import ViReport_GlobalContext as GC

class Dating_None(Dating):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def blurb():
        return "Phylogenetic dating was not performed."

    def date(rooted_tree_filename, sample_times_filename):
        return None
