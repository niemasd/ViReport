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
        if GC.GZIP_OUTPUT:
            out_filename += '.gz'
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Dated tree exists. Skipping recomputation.")
        else:
            makedirs(treedater_dir, exist_ok=True)
            log_file = open('%s/log.txt' % treedater_dir, 'w')
            warn_file = open('%s/warnings.txt' % treedater_dir, 'w')
            tree_filename = '%s/dated.tre' % treedater_dir
            treedater_times_filename = '%s/times_treedater.txt' % treedater_dir
            GC.write_file(GC.convert_dates_treedater(sample_times_filename), treedater_times_filename)
            msa = GC.read_fasta(GC.ALIGNMENT)
            msa_columns = len(msa[list(msa.keys())[0]])
            command = ['tdcl', '-t', rooted_tree_filename, '-s', treedater_times_filename, '-l', str(msa_columns), '-o', tree_filename]
            f = open('%s/command.txt' % treedater_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            call(command, stdout=log_file, stderr=warn_file)
            log_file.close(); warn_file.close()
            GC.write_file('\n'.join(GC.read_file(tree_filename)), out_filename)
        return out_filename
