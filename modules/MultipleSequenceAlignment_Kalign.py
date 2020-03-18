#! /usr/bin/env python3
'''
Implementation of the "MultipleSequenceAlignment" module using Kalign
'''
from MultipleSequenceAlignment import MultipleSequenceAlignment
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import call

class MultipleSequenceAlignment_Kalign(MultipleSequenceAlignment):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_KALIGN

    def blurb():
        return "Multiple sequence alignment was performed using Kalign (Lassmann, 2019)."

    def align(seqs_filename):
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        kalign_dir = '%s/Kalign' % GC.OUT_DIR_TMPFILES
        makedirs(kalign_dir, exist_ok=True)
        log = open('%s/log.txt' % kalign_dir, 'w')
        out_filename = '%s/%s.aln' % (GC.OUT_DIR_OUTFILES, '.'.join(seqs_filename.split('/')[-1].split('.')[:-1]))
        command = ['kalign', '-i', seqs_filename, '-o', out_filename]
        f = open('%s/command.txt' % kalign_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
        call(command, stdout=log); log.close()
        return out_filename
