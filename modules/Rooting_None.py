#! /usr/bin/env python3
'''
Implementation of the "Rooting" module that does nothing
'''
from Rooting import Rooting
import ViReport_GlobalContext as GC

class Rooting_None(Rooting):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def blurb():
        return "Phylogenetic rooting was not performed."

    def root(tree_filename):
        return None
