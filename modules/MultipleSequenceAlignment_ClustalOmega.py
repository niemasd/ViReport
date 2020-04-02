#! /usr/bin/env python3
'''
Implementation of the "MultipleSequenceAlignment" module using Clustal Omega
'''
from MultipleSequenceAlignment import MultipleSequenceAlignment
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import check_output

class MultipleSequenceAlignment_ClustalOmega(MultipleSequenceAlignment):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_CLUSTALOMEGA

    def blurb():
        return "Multiple sequence alignment was performed using Clustal Omega (Sievers et al., 2011) in automatic mode."

    def align(seqs_filename, ref_id):
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        clustalo_dir = '%s/ClustalOmega' % GC.OUT_DIR_TMPFILES
        log_filename = '%s/log.txt' % clustalo_dir
        out_filename = '%s/%s.aln' % (GC.OUT_DIR_OUTFILES, '.'.join(GC.rstrip_gz(seqs_filename.split('/')[-1]).split('.')[:-1]))
        if GC.GZIP_OUTPUT:
            out_filename += '.gz'
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Multiple sequence alignment exists. Skipping recomputation.")
        else:
            makedirs(clustalo_dir, exist_ok=True)
            command = ['clustalo', '-v', '-v', '--auto', '-i', '-', '-l', log_filename]
            if GC.NUM_THREADS is not None:
                command.append('--threads=%d' % GC.NUM_THREADS)
            f = open('%s/command.txt' % clustalo_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            GC.write_file(check_output(command, input='\n'.join(GC.read_file(seqs_filename)).encode()).decode(), out_filename)
        return out_filename
