#! /usr/bin/env python3
'''
Implementation of the "Logging" module where log messages are written to a file
'''
from Logging import Logging
import ViReport_GlobalContext as GC
GC.LOG_FILE = None

def log_init():
    if GC.LOG_FILE is None:
        GC.LOG_FILE = open('%s/vireport.log' % GC.OUT_DIR, 'w')

class Logging_File(Logging):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def blurb():
        return ''

    def write(s):
        log_init(); GC.LOG_FILE.write(s); GC.LOG_FILE.flush()

    def writeln(s):
        log_init(); GC.LOG_FILE.write(s); GC.LOG_FILE.write('\n'); GC.LOG_FILE.flush()
