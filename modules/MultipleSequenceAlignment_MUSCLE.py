#! /usr/bin/env python3
'''
Implementation of the "MultipleSequenceAlignment" module using MUSCLE
'''
from MultipleSequenceAlignment import MultipleSequenceAlignment
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import call

class MultipleSequenceAlignment_MUSCLE(MultipleSequenceAlignment):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_MUSCLE

    def align(seqs_filename):
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        muscle_dir = '%s/MUSCLE' % GC.OUT_DIR_TMPFILES
        makedirs(muscle_dir, exist_ok=True)
        log_filename = '%s/log.txt' % muscle_dir
        out_filename = '%s/%s.aln' % (GC.OUT_DIR_OUTFILES, '.'.join(seqs_filename.split('/')[-1].split('.')[:-1]))
        command = ['muscle', '-quiet', '-in', seqs_filename, '-out', out_filename, '-log', log_filename]
        f = open('%s/command.txt' % muscle_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
        call(command)
        return out_filename
