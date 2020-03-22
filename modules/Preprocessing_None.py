#! /usr/bin/env python3
'''
Implementation of the "Preprocessing" module where no preprocessing is done
'''
from Preprocessing import Preprocessing
import ViReport_GlobalContext as GC

class Preprocessing_None(Preprocessing):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def blurb():
        return "No preprocessing was done: the inputs were used as they were given."

    def preprocess(seqs_filename, ref_id, sample_times_filename, outgroups_filename, categories_filename):
        return seqs_filename, ref_id, sample_times_filename, outgroups_filename, categories_filename
