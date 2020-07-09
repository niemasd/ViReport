#! /usr/bin/env python3
'''
Implementation of the "Dating" module using treedater
'''
from Dating import Dating
import ViReport_GlobalContext as GC
from glob import glob
from os import makedirs
from os.path import isfile
from shutil import move
from subprocess import call
ZERO_THRESHOLD = 0.00001

class Dating_treedater(Dating):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_TREEDATER

    def blurb():
        return "The rooted phylogeny was dated using treedater (Volz & Frost, 2017)."

    def date(rooted_tree_filename, sample_times_filename):
        if not isfile(rooted_tree_filename):
            raise ValueError("Invalid tree file: %s" % rooted_tree_filename)
        if not isfile(sample_times_filename):
            raise ValueError("Invalid sample times file: %s" % sample_times_filename)
        treedater_dir = '%s/treedater' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/dated.tre' % GC.OUT_DIR_OUTFILES
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Dated tree exists. Skipping recomputation.")
        else:
            makedirs(treedater_dir, exist_ok=True)
            log_file = open('%s/log.txt' % treedater_dir, 'w')
            warn_file = open('%s/warnings.txt' % treedater_dir, 'w')
            tree_filename = out_filename
            treedater_times_filename = '%s/times_treedater.txt' % treedater_dir
            GC.write_file(GC.convert_dates_treedater(sample_times_filename), treedater_times_filename)
            msa = GC.read_fasta(GC.ALIGNMENT)
            msa_columns = len(msa[list(msa.keys())[0]])
            unzipped_intree_filename = rooted_tree_filename
            if rooted_tree_filename.lower().endswith('.gz'):
                unzipped_intree_filename = '%s/rooted_unzipped.tre' % treedater_dir
                GC.write_file('\n'.join(GC.read_file(rooted_tree_filename)), unzipped_intree_filename)
            mut_rate_est = GC.estimate_mutation_rate(rooted_tree_filename, sample_times_filename)
            rscript_filename = '%s/run_treedater.R' % treedater_dir
            f = open(rscript_filename, 'w')
            f.write("require(treedater)\ntree <- ape::read.tree('%s')\nseqlen <- %d\ntimes_tab <- read.csv('%s', header=FALSE)\ntimes <- setNames(times_tab[,2], times_tab[,1])\nout <- dater(tree, times, seqlen, clock='uncorrelated', numStartConditions=0" % (unzipped_intree_filename, msa_columns, treedater_times_filename))
            if mut_rate_est > ZERO_THRESHOLD:
                f.write(", omega0=%f" % mut_rate_est)
            if GC.NUM_THREADS is not None:
                f.write(", ncpu=%s" % str(GC.NUM_THREADS))
            f.write(")\nwrite.tree(out, '%s')\n" % tree_filename); f.close()
            command = ['Rscript', rscript_filename]
            f = open('%s/command.txt' % treedater_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            call(command, stdout=log_file, stderr=warn_file)
            log_file.close(); warn_file.close()
        return out_filename
