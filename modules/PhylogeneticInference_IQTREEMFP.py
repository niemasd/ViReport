#! /usr/bin/env python3
'''
Implementation of the "PhylogeneticInference" module using IQ-TREE with ModelFinder Plus
'''
from PhylogeneticInference import PhylogeneticInference
import ViReport_GlobalContext as GC
from glob import glob
from os import makedirs
from os.path import isfile
from shutil import move
from subprocess import check_output

class PhylogeneticInference_IQTREEMFP(PhylogeneticInference):
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
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Inferred phylogeny exists. Skipping recomputation.")
        else:
            makedirs(iqtree_dir, exist_ok=True)
            if aln_filename.lower().endswith('.gz'):
                unzipped_filename = '%s/aln_unzipped.fas' % iqtree_dir
                GC.write_file('\n'.join(GC.read_file(aln_filename)), unzipped_filename)
                aln_filename = unzipped_filename
            command = ['iqtree', '-m', 'MFP', '-s', aln_filename, '-nt']
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
