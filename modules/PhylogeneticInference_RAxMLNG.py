#! /usr/bin/env python3
'''
Implementation of the "PhylogeneticInference" module using RAxML-NG
'''
from PhylogeneticInference import PhylogeneticInference
import ViReport_GlobalContext as GC
from glob import glob
from os import makedirs
from os.path import isfile
from shutil import move
from subprocess import check_output

class PhylogeneticInference_RAxMLNG(PhylogeneticInference):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_RAXML_NG

    def infer_phylogeny(aln_filename):
        if not isfile(aln_filename):
            raise ValueError("Invalid alignment file: %s" % aln_filename)
        raxmlng_dir = '%s/RAxML-NG' % GC.OUT_DIR_TMPFILES
        makedirs(raxmlng_dir, exist_ok=True)
        out_filename = '%s/unrooted.tre' % GC.OUT_DIR_OUTFILES
        command = ['raxml-ng', '--force', '--msa', aln_filename, '--model']
        seq_type = GC.predict_seq_type(aln_filename)
        if seq_type == 'DNA':
            command.append('GTR+I+G')
        elif seq_type == 'AA':
            command.append('PROTGAMMAAUTO')
        else:
            raise ValueError("Invalid sequence type: %s" % seq_type)
        f = open('%s/command.txt' % raxmlng_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
        check_output(command)
        move('%s.raxml.bestTree' % aln_filename, out_filename)
        for f in glob('%s.*' % aln_filename):
            move(f, '%s/%s' % (raxmlng_dir, f.split('/')[-1]))
        return out_filename
