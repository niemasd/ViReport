#! /usr/bin/env python3
'''
Implementation of the "Dating" module using TreeTime
'''
from Dating import Dating
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from re import sub
from shutil import move
from subprocess import call,DEVNULL
from treeswift import read_tree_nexus

class Dating_TreeTime(Dating):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_TREETIME

    def blurb():
        return "The rooted phylogeny was dated using TreeTime (Sagulenko et al., 2018)."

    def date(rooted_tree_filename, sample_times_filename):
        if not isfile(rooted_tree_filename):
            raise ValueError("Invalid tree file: %s" % rooted_tree_filename)
        if not isfile(sample_times_filename):
            raise ValueError("Invalid sample times file: %s" % sample_times_filename)
        treetime_dir = '%s/TreeTime_Dating' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/dated.tre' % GC.OUT_DIR_OUTFILES
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Dated tree exists. Skipping recomputation.")
        else:
            makedirs(treetime_dir, exist_ok=True)
            treetime_dates_filename = '%s/dates.csv' % treetime_dir
            log = open('%s/log.txt' % treetime_dir, 'w')
            err = open('%s/err.txt' % treetime_dir, 'w')
            msa = GC.read_fasta(GC.ALIGNMENT)
            msa_columns = len(msa[list(msa.keys())[0]])
            f = open(treetime_dates_filename, 'w'); f.write("name,date\n")
            for l in GC.read_file(sample_times_filename):
                f.write("%s\n" % l.strip().replace('\t',','))
            f.close()
            if rooted_tree_filename.endswith('.gz'):
                unzipped_filename = '%s/tree_unzipped.fas' % treetime_dir
                GC.write_file('\n'.join(GC.read_file(rooted_tree_filename)), unzipped_filename)
                rooted_tree_filename = unzipped_filename
            command = ['treetime', '--sequence-length', str(msa_columns), '--keep-root', '--tree', rooted_tree_filename, '--dates', treetime_dates_filename, '--outdir', treetime_dir]
            f = open('%s/command.txt' % treetime_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            call(command, stdout=log, stderr=err)
            log.close(); err.close()
            tmp = read_tree_nexus(sub("[\[].*?[\]]", '', open('%s/timetree.nexus' % treetime_dir).read()))
            GC.write_file(tmp[list(tmp.keys())[0]].newick(), out_filename)
        return out_filename
