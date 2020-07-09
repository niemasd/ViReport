#! /usr/bin/env python3
'''
Implementation of the "PhylogeneticInference" module using VeryFastTree
'''
from PhylogeneticInference import PhylogeneticInference
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import check_output

class PhylogeneticInference_VeryFastTree(PhylogeneticInference):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return [GC.CITATION_VERYFASTTREE, GC.CITATION_MODEL_GTR]

    def blurb():
        return "A maximum-likelihood phylogeny was inferred under the General Time-Reversible (GTR) model (Tavare, 1986) using VeryFastTree (Piñeiro et al., 2020) using a Gamma20-based likelihood."

    def infer_phylogeny(aln_filename):
        if not isfile(aln_filename):
            raise ValueError("Invalid alignment file: %s" % aln_filename)
        veryfasttree_dir = '%s/VeryFastTree' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/unrooted.tre' % GC.OUT_DIR_OUTFILES
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Inferred phylogeny exists. Skipping recomputation.")
        else:
            makedirs(veryfasttree_dir, exist_ok=True)
            progress_file = open('%s/progress.txt' % veryfasttree_dir, 'w')
            command = ['VeryFastTree', '-gamma', '-nt', '-gtr', '-double-precision', '-fastexp', '2', '-out', out_filename]
            if GC.NUM_THREADS is not None:
                command += ['-threads', str(GC.NUM_THREADS)]
            # the log file is somewhat large, so just disable for now
            #log_filename = '%s/log.txt' % veryfasttree_dir
            #command += ['-log', log_filename]
            f = open('%s/command.txt' % veryfasttree_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            check_output(command, input='\n'.join(GC.fasta_stream_upper(GC.stream_file(aln_filename))).encode(), stderr=progress_file); progress_file.close()
        return out_filename
