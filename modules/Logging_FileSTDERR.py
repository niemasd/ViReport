#! /usr/bin/env python3
'''
Implementation of the "Logging" module where log messages are written to a file and to standard error (STDERR)
'''
from Logging import Logging
import ViReport_GlobalContext as GC
from Logging_File import Logging_File
from Logging_STDERR import Logging_STDERR

class Logging_FileSTDERR(Logging):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def blurb():
        return ''

    def write(s):
        Logging_File.write(s); Logging_STDERR.write(s)

    def writeln(s):
        Logging_File.writeln(s); Logging_STDERR.writeln(s)
