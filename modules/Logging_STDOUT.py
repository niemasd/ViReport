#! /usr/bin/env python3
'''
Implementation of the "Logging" module where log messages are written to standard output (STDOUT)
'''
from Logging import Logging
import ViReport_GlobalContext as GC
from sys import stdout

class Logging_STDOUT(Logging):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def blurb():
        return ''

    def write(s):
        stdout.write(s); stdout.flush()

    def writeln(s):
        stdout.write(s); stdout.write('\n'); stdout.flush()
