#! /usr/bin/env python3
'''
Implementation of the "MultipleSequenceAlignment" module using Clustal Omega
'''
from MultipleSequenceAlignment import MultipleSequenceAlignment
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import call

class MultipleSequenceAlignment_ClustalOmega(MultipleSequenceAlignment):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_CLUSTALOMEGA

    def align(seqs_filename):
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        clustalo_dir = '%s/ClustalOmega' % GC.OUT_DIR_TMPFILES
        makedirs(clustalo_dir, exist_ok=True)
        log_filename = '%s/log.txt' % clustalo_dir
        out_filename = '%s/%s.aln' % (GC.OUT_DIR_OUTFILES, '.'.join(seqs_filename.split('/')[-1].split('.')[:-1]))
        command = ['clustalo', '--auto', '-i', seqs_filename, '-o', out_filename, '-l', log_filename]
        f = open('%s/command.txt' % clustalo_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
        call(command)
        return out_filename
