#! /usr/bin/env python3
'''
Implementation of the "ReportFormat" module using all "ReportFormat" module implementations
'''
from ReportFormat import ReportFormat
import ViReport_GlobalContext as GC
import ViReport_ModuleFactory as MF

class ReportFormat_All(ReportFormat):
    def init():
        GC.REPORTFORMATS = [MF.MODULES['ReportFormat'][k] for k in MF.MODULES['ReportFormat'] if k != 'All']

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def section(s):
        for fmt in GC.REPORTFORMATS:
            fmt.section(s)

    def subsection(s):
        for fmt in GC.REPORTFORMATS:
            fmt.subsection(s)

    def write(s, text_type='normal'):
        for fmt in GC.REPORTFORMATS:
            fmt.write(s, text_type=text_type)

    def writeln(s, text_type='normal'):
        for fmt in GC.REPORTFORMATS:
            fmt.writeln(s, text_type=text_type)

    def figure(filename, caption=None, width=None, height=None):
        for fmt in GC.REPORTFORMATS:
            fmt.figure(filename, caption=caption, width=width, height=height)

    def close():
        for fmt in GC.REPORTFORMATS:
            fmt.close()
        return GC.OUT_DIR
