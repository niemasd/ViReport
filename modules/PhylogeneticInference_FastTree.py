#! /usr/bin/env python3
'''
Implementation of the "PhylogeneticInference" module using FastTree
'''
from PhylogeneticInference import PhylogeneticInference
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import check_output

class PhylogeneticInference_FastTree(PhylogeneticInference):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return [GC.CITATION_FASTTREE, GC.CITATION_MODEL_GTR, GC.CITATION_MODEL_LG]

    def blurb():
        return "A maximum-likelihood phylogeny was inferred under the General Time-Reversible (GTR) model (Tavare, 1986) using FastTree 2 (Price et al., 2010) using a Gamma20-based likelihood."

    def infer_phylogeny(aln_filename):
        if not isfile(aln_filename):
            raise ValueError("Invalid alignment file: %s" % aln_filename)
        fasttree_dir = '%s/FastTree' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/unrooted.tre' % GC.OUT_DIR_OUTFILES
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Inferred phylogeny exists. Skipping recomputation.")
        else:
            makedirs(fasttree_dir, exist_ok=True)
            progress_file = open('%s/progress.txt' % fasttree_dir, 'w')
            command = ['FastTree', '-gamma', '-nt', '-gtr', '-out', out_filename]
            # the log file is somewhat large, so just disable for now
            #log_filename = '%s/log.txt' % fasttree_dir
            #command += ['-log', log_filename]
            f = open('%s/command.txt' % fasttree_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            check_output(command, input='\n'.join(GC.read_file(aln_filename)).encode(), stderr=progress_file); progress_file.close()
        return out_filename
