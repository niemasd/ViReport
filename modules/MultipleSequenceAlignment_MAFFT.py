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

    def blurb():
        return "Multiple sequence alignment was performed using MAFFT (Katoh & Standley, 2013) in automatic mode."

    def align(seqs_filename, ref_id):
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        mafft_dir = '%s/MAFFT' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/%s.aln' % (GC.OUT_DIR_OUTFILES, '.'.join(seqs_filename.split('/')[-1].split('.')[:-1]))
        if isfile(out_filename):
            GC.SELECTED['Logging'].writeln("Multiple sequence alignment exists. Skipping recomputation.")
        else:
            makedirs(mafft_dir, exist_ok=True)
            f_stderr = open('%s/log.txt' % mafft_dir, 'w')
            f_stdout = open(out_filename, 'w')
            command = ['mafft', '--reorder', '--nomemsave', '--thread']
            if GC.NUM_THREADS is None:
                command.append('-1')
            else:
                command.append(str(GC.NUM_THREADS))
            command += ['--auto', seqs_filename]
            f = open('%s/command.txt' % mafft_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            ret = call(command, stdout=f_stdout, stderr=f_stderr)
            f_stdout.close(); f_stderr.close()
            if ret != 0 or '>' not in open(out_filename).read():
                raise RuntimeError("MAFFT did not run successfully")
        return out_filename
