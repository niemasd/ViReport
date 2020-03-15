#! /usr/bin/env python3
'''
Implementation of the "Logging" module where log messages are written to a file and to standard output (STDOUT)
'''
from Logging import Logging
import ViReport_GlobalContext as GC
from Logging_File import Logging_File
from Logging_STDOUT import Logging_STDOUT

class Logging_FileSTDOUT(Logging):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def blurb():
        return ''

    def write(s):
        Logging_File.write(s); Logging_STDOUT.write(s)

    def writeln(s):
        Logging_File.writeln(s); Logging_STDOUT.writeln(s)
