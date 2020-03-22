#! /usr/bin/env python3
'''
Implementation of the "MultipleSequenceAlignment" module using PRANK
'''
from MultipleSequenceAlignment import MultipleSequenceAlignment
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from shutil import move
from subprocess import call

class MultipleSequenceAlignment_PRANK(MultipleSequenceAlignment):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_PRANK

    def blurb():
        return "Multiple sequence alignment was performed using PRANK (Loytynoja, 2013)."

    def align(seqs_filename, ref_id):
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        prank_dir = '%s/PRANK' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/%s.aln' % (GC.OUT_DIR_OUTFILES, '.'.join(seqs_filename.split('/')[-1].split('.')[:-1]))
        if isfile(out_filename):
            GC.SELECTED['Logging'].writeln("Multiple sequence alignment exists. Skipping recomputation.")
        else:
            makedirs(prank_dir, exist_ok=True)
            log = open('%s/log.txt' % prank_dir, 'w')
            command = ['prank', '-o=%s' % out_filename, '-d=%s' % seqs_filename]
            f = open('%s/command.txt' % prank_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            call(command, stdout=log); log.close()
            move('%s.best.fas' % out_filename, out_filename)
        return out_filename
