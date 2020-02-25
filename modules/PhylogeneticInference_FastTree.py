#! /usr/bin/env python3
'''
Implementation of the "PhylogeneticInference" module using FastTree
'''
from PhylogeneticInference import PhylogeneticInference
import ViReport_GlobalContext as GC
from glob import glob
from os import makedirs
from os.path import isfile
from subprocess import call

class PhylogeneticInference_FastTree(PhylogeneticInference):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_FASTTREE

    def infer_phylogeny(aln_filename):
        if not isfile(aln_filename):
            raise ValueError("Invalid alignment file: %s" % aln_filename)
        fasttree_dir = '%s/FastTree' % GC.OUT_DIR_TMPFILES
        makedirs(fasttree_dir, exist_ok=True)
        out_filename = '%s/unrooted.tre' % GC.OUT_DIR_OUTFILES
        progress_file = open('%s/progress.txt' % fasttree_dir, 'w')
        command = ['FastTree', '-out', out_filename, '-gamma']
        # the log file is somewhat large, so just disable for now
        #log_filename = '%s/log.txt' % fasttree_dir
        #command += ['-log', log_filename]
        seq_type = GC.predict_seq_type(aln_filename)
        if seq_type == 'DNA':
            command += ['-nt', '-gtr']
        elif seq_type == 'AA':
            command.append('-lg')
        else:
            raise ValueError("Invalid sequence type: %s" % seq_type)
        command.append(aln_filename)
        f = open('%s/command.txt' % fasttree_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
        call(command, stderr=progress_file)
        progress_file.close()
        return out_filename
