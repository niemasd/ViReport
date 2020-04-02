#! /usr/bin/env python3
'''
Implementation of the "MultipleSequenceAlignment" module using Kalign
'''
from MultipleSequenceAlignment import MultipleSequenceAlignment
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import check_output

class MultipleSequenceAlignment_Kalign(MultipleSequenceAlignment):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_KALIGN

    def blurb():
        return "Multiple sequence alignment was performed using Kalign (Lassmann, 2019)."

    def align(seqs_filename, ref_id):
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        kalign_dir = '%s/Kalign' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/%s.aln' % (GC.OUT_DIR_OUTFILES, '.'.join(GC.rstrip_gz(seqs_filename.split('/')[-1]).split('.')[:-1]))
        if GC.GZIP_OUTPUT:
            out_filename += '.gz'
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Multiple sequence alignment exists. Skipping recomputation.")
        else:
            makedirs(kalign_dir, exist_ok=True)
            command = ['kalign', '-f', '-fasta']
            f = open('%s/command.txt' % kalign_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            parts = check_output(command, input='\n'.join(GC.read_file(seqs_filename)).encode()).decode().split('>')
            f = open('%s/log.txt' % kalign_dir, 'w'); f.write(parts[0]); f.close()
            parts[0] = ''; GC.write_file('>'.join(parts), out_filename)
        return out_filename
