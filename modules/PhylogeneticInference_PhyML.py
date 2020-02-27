#! /usr/bin/env python3
'''
Implementation of the "PhylogeneticInference" module using PhyML
'''
from PhylogeneticInference import PhylogeneticInference
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from shutil import move
from subprocess import call

class PhylogeneticInference_PhyML(PhylogeneticInference):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_PHYML

    def infer_phylogeny(aln_filename):
        if not isfile(aln_filename):
            raise ValueError("Invalid alignment file: %s" % aln_filename)
        phyml_dir = '%s/PhyML' % GC.OUT_DIR_TMPFILES
        makedirs(phyml_dir, exist_ok=True)
        out_filename = '%s/unrooted.tre' % GC.OUT_DIR_OUTFILES
        log_file = open('%s/log.txt' % phyml_dir, 'w')
        phy_filename = '%s/alignment.phy' % phyml_dir
        f = open(phy_filename, 'w'); f.write(GC.fasta_to_phylip(aln_filename)); f.close()
        command = ['phyml', '--leave_duplicates', '-i', phy_filename, '-a', 'e']
        seq_type = GC.predict_seq_type(aln_filename)
        if seq_type == 'DNA':
            command += ['-d', 'nt', '-m', 'GTR']
        elif seq_type == 'AA':
            command += ['-d', 'aa', '-m', 'LG']
        else:
            raise ValueError("Invalid sequence type: %s" % seq_type)
        f = open('%s/command.txt' % phyml_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
        call(command, stdout=log_file)
        log_file.close()
        move('%s_phyml_tree.txt' % phy_filename, out_filename)
        return out_filename