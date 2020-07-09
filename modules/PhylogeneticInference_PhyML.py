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

    def blurb():
        return "A maximum-likelihood phylogeny was inferred under the General Time-Reversible (GTR) model (Tavare, 1986) using PhyML (Guindon et al., 2010)."

    def infer_phylogeny(aln_filename):
        if not isfile(aln_filename):
            raise ValueError("Invalid alignment file: %s" % aln_filename)
        phyml_dir = '%s/PhyML' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/unrooted.tre' % GC.OUT_DIR_OUTFILES
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Inferred phylogeny exists. Skipping recomputation.")
        else:
            makedirs(phyml_dir, exist_ok=True)
            log_file = open('%s/log.txt' % phyml_dir, 'w')
            phy_filename = '%s/alignment.phy' % phyml_dir
            GC.write_file(GC.fasta_to_phylip(aln_filename), phy_filename)
            command = ['phyml', '--leave_duplicates', '-i', phy_filename, '-a', 'e', '-d', 'nt', '-m', 'GTR']
            f = open('%s/command.txt' % phyml_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            call(command, stdout=log_file)
            log_file.close()
            move('%s_phyml_tree.txt' % phy_filename, out_filename)
        return out_filename
