#! /usr/bin/env python3
'''
Implementation of the "MultipleSequenceAlignment" module using FSA
'''
from MultipleSequenceAlignment import MultipleSequenceAlignment
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import call

class MultipleSequenceAlignment_FSA(MultipleSequenceAlignment):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_FSA

    def blurb():
        return "Multiple sequence alignment was performed using FSA (Bradley et al., 2009)."

    def align(seqs_filename, ref_id):
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        fsa_dir = '%s/FSA' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/%s.aln' % (GC.OUT_DIR_OUTFILES, '.'.join(seqs_filename.split('/')[-1].split('.')[:-1]))
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Multiple sequence alignment exists. Skipping recomputation.")
        else:
            makedirs(fsa_dir, exist_ok=True)
            log_filename = '%s/log.txt' % fsa_dir
            err = open('%s/err.txt' % fsa_dir, 'w')
            out = open(out_filename, 'w')
            command = ['fsa', '--logfile', log_filename, seqs_filename]
            f = open('%s/command.txt' % fsa_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            call(command, stdout=out, stderr=err); out.close(); err.close()
        return out_filename
