#! /usr/bin/env python3
'''
Implementation of the "MultipleSequenceAlignment" module using Minimap2
'''
from MultipleSequenceAlignment import MultipleSequenceAlignment
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import call

class MultipleSequenceAlignment_Minimap2(MultipleSequenceAlignment):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_Minimap2

    def blurb():
        return "Multiple sequence alignment was performed using Minimap2 (Katoh & Standley, 2013) in automatic mode."

    def align(seqs_filename, ref_id):
        raise RuntimeError("NEED TO IMPLEMENT") # TODO
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        minimap2_dir = '%s/Minimap2' % GC.OUT_DIR_TMPFILES
        makedirs(minimap2_dir, exist_ok=True)
        f_stderr = open('%s/log.txt' % minimap2_dir, 'w')
        out_filename = '%s/%s.aln' % (GC.OUT_DIR_OUTFILES, '.'.join(seqs_filename.split('/')[-1].split('.')[:-1]))
        f_stdout = open(out_filename, 'w')
        command = ['mafft', '--reorder', '--nomemsave', '--thread']
        if GC.NUM_THREADS is None:
            command.append('-1')
        else:
            command.append(str(GC.NUM_THREADS))
        command += ['--auto', seqs_filename]
        f = open('%s/command.txt' % minimap2_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
        ret = call(command, stdout=f_stdout, stderr=f_stderr)
        f_stdout.close(); f_stderr.close()
        if ret != 0 or '>' not in open(out_filename).read():
            raise RuntimeError("Minimap2 did not run successfully")
        return out_filename
