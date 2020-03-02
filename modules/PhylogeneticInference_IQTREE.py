#! /usr/bin/env python3
'''
Implementation of the "PhylogeneticInference" module using IQ-TREE
'''
from PhylogeneticInference import PhylogeneticInference
import ViReport_GlobalContext as GC
from glob import glob
from os import makedirs
from os.path import isfile
from shutil import move
from subprocess import check_output

class PhylogeneticInference_IQTREE(PhylogeneticInference):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return [GC.CITATION_IQTREE, GC.CITATION_IQTREE_MFP]

    def blurb():
        return "A maximum-likelihood phylogeny was inferred using IQ-TREE (Nguyen et al., 2015) in ModelFinder Plus mode (Kalyaanamoorthy et al., 2017)."

    def infer_phylogeny(aln_filename):
        if not isfile(aln_filename):
            raise ValueError("Invalid alignment file: %s" % aln_filename)
        iqtree_dir = '%s/IQTREE' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/unrooted.tre' % GC.OUT_DIR_OUTFILES
        makedirs(iqtree_dir, exist_ok=True)
        command = ['iqtree', '-m', 'MFP', '-nt', 'AUTO', '-s', aln_filename]
        f = open('%s/command.txt' % iqtree_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
        log = check_output(command)
        move('%s.treefile' % aln_filename , out_filename)
        for f in glob('%s.*' % aln_filename):
            move(f, '%s/%s' % (iqtree_dir, f.split('/')[-1]))
        return out_filename
