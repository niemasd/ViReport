#! /usr/bin/env python3
'''
Implementation of the "MultipleSequenceAlignment" module using MUSCLE
'''
from MultipleSequenceAlignment import MultipleSequenceAlignment
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import check_output

class MultipleSequenceAlignment_MUSCLE(MultipleSequenceAlignment):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_MUSCLE

    def blurb():
        return "Multiple sequence alignment was performed using MUSCLE (Edgar, 2004)."

    def align(seqs_filename, ref_id):
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        muscle_dir = '%s/MUSCLE' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/%s.aln' % (GC.OUT_DIR_OUTFILES, '.'.join(seqs_filename.split('/')[-1].split('.')[:-1]))
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Multiple sequence alignment exists. Skipping recomputation.")
        else:
            makedirs(muscle_dir, exist_ok=True)
            log_filename = '%s/log.txt' % muscle_dir
            command = ['muscle', '-quiet', '-log', log_filename, '-out', out_filename]
            f = open('%s/command.txt' % muscle_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            check_output(command, input='\n'.join(GC.read_file(seqs_filename)).encode())
        return out_filename
