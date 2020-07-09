#! /usr/bin/env python3
'''
"WriteReport" module implementation that does nothing
'''
from WriteReport import WriteReport
import ViReport_GlobalContext as GC

class WriteReport_None(WriteReport):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def write_report():
        return None
