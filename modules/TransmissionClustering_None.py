#! /usr/bin/env python3
'''
Implementation of the "TransmissionClustering" module that just doesn't perform transmission clustering
'''
from TransmissionClustering import TransmissionClustering
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import call

class TransmissionClustering_None(TransmissionClustering):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_TREEN93

    def blurb():
        return "Transmission clustering was not performed."

    def infer_transmission_clusters():
        return None
