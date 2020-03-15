#! /usr/bin/env python3
'''
Implementation of the "Logging" module where log messages are written to standard error (STDERR)
'''
from Logging import Logging
import ViReport_GlobalContext as GC
from sys import stderr

class Logging_STDERR(Logging):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def blurb():
        return ''

    def write(s):
        stderr.write(s); stderr.flush()

    def writeln(s):
        stderr.write(s); stderr.write('\n'); stderr.flush()
