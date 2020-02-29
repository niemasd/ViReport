#! /usr/bin/env python3
'''
Default implementation of the "WriteReport" module
'''
from WriteReport import WriteReport
import ViReport_GlobalContext as GC

class WriteReport_Default(WriteReport):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def write_report():
        GC.SELECTED['ReportFormat'].section("Introduction")
        GC.SELECTED['ReportFormat'].writeln("This is my introduction")
        GC.SELECTED['ReportFormat'].close()
        return None
