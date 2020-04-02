#! /usr/bin/env python3
'''
Implementation of the "MultipleSequenceAlignment" module using MAFFT
'''
from MultipleSequenceAlignment import MultipleSequenceAlignment
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import check_output

class MultipleSequenceAlignment_MAFFT(MultipleSequenceAlignment):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_MAFFT

    def blurb():
        return "Multiple sequence alignment was performed using MAFFT (Katoh & Standley, 2013) in automatic mode."

    def align(seqs_filename, ref_id):
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        mafft_dir = '%s/MAFFT' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/%s.aln' % (GC.OUT_DIR_OUTFILES, '.'.join(GC.rstrip_gz(seqs_filename.split('/')[-1]).split('.')[:-1]))
        if GC.GZIP_OUTPUT:
            out_filename += '.gz'
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Multiple sequence alignment exists. Skipping recomputation.")
        else:
            makedirs(mafft_dir, exist_ok=True)
            f_stderr = open('%s/log.txt' % mafft_dir, 'w')
            command = ['mafft', '--reorder', '--nomemsave', '--thread']
            if GC.NUM_THREADS is None:
                command.append('-1')
            else:
                command.append(str(GC.NUM_THREADS))
            if seqs_filename.lower().endswith('.gz'):
                unzipped_filename = '%s/seqs_unzipped.fas' % mafft_dir
                GC.write_file('\n'.join(GC.read_file(seqs_filename)), unzipped_filename)
                seqs_filename = unzipped_filename
            command += ['--auto', seqs_filename]
            f = open('%s/command.txt' % mafft_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            o = check_output(command, stderr=f_stderr).decode(); f_stderr.close()
            GC.write_file(o, out_filename)
        return out_filename
