#! /usr/bin/env python3
'''
Implementation of the "MultipleSequenceAlignment" module using MAFFT
'''
from MultipleSequenceAlignment import MultipleSequenceAlignment
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import call

class MultipleSequenceAlignment_MAFFT(MultipleSequenceAlignment):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_MAFFT

    def align(seqs_filename):
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        mafft_dir = '%s/MAFFT' % GC.OUT_DIR_TMPFILES
        makedirs(mafft_dir, exist_ok=True)
        f_stderr = open('%s/log.txt' % mafft_dir, 'w')
        out_filename = '%s/%s.aln' % (GC.OUT_DIR_OUTFILES, '.'.join(seqs_filename.split('/')[-1].split('.')[:-1]))
        f_stdout = open(out_filename, 'w')
        command = ['mafft', '--thread', '-1', '--auto', seqs_filename]
        f = open('%s/command.txt' % mafft_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
        call(command, stdout=f_stdout, stderr=f_stderr)
        f_stdout.close(); f_stderr.close()
        return out_filename
