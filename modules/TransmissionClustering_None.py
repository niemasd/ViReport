#! /usr/bin/env python3
'''
Implementation of the "TransmissionClustering" module that does nothing
'''
from TransmissionClustering import TransmissionClustering
import ViReport_GlobalContext as GC

class TransmissionClustering_None(TransmissionClustering):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def blurb():
        return "Transmission clustering was not performed."

    def infer_transmission_clusters():
        return None
