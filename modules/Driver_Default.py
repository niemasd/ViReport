#! /usr/bin/env python3
'''
Default implementation of the "Driver" module
'''
from Driver import Driver
import ViReport_GlobalContext as GC

class Driver_Default(Driver):
    def init():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def run():
        pass
