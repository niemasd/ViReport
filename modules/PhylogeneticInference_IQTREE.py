#! /usr/bin/env python3
'''
Implementation of the "PhylogeneticInference" module using IQ-TREE with GTR + invariable sites + FreeRate model of rate heterogeneity across sites
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
        return GC.CITATION_IQTREE

    def blurb():
        return "A maximum-likelihood phylogeny was inferred under the General Time-Reversible (GTR) model (Tavare, 1986) and under the FreeRate model of rate heterogeneity across sites (Soubrier et al., 2012) with sites allowed to be invariable using IQ-TREE (Nguyen et al., 2015)."

    def infer_phylogeny(aln_filename):
        if not isfile(aln_filename):
            raise ValueError("Invalid alignment file: %s" % aln_filename)
        iqtree_dir = '%s/IQTREE' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/unrooted.tre' % GC.OUT_DIR_OUTFILES
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Inferred phylogeny exists. Skipping recomputation.")
        else:
            makedirs(iqtree_dir, exist_ok=True)
            if aln_filename.lower().endswith('.gz'):
                unzipped_filename = '%s/aln_unzipped.fas' % iqtree_dir
                GC.write_file('\n'.join(GC.read_file(aln_filename)), unzipped_filename)
                aln_filename = unzipped_filename
            command = ['iqtree', '-m', 'GTR+I+R', '-s', aln_filename, '-nt']
            if GC.NUM_THREADS is None:
                command.append('AUTO')
            else:
                command.append(str(GC.NUM_THREADS))
            f = open('%s/command.txt' % iqtree_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            log = check_output(command)
            move('%s.treefile' % aln_filename, out_filename)
            for f in glob('%s.*' % aln_filename):
                move(f, '%s/%s' % (iqtree_dir, f.split('/')[-1]))
        return out_filename
