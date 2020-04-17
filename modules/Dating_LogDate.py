#! /usr/bin/env python3
'''
Implementation of the "Dating" module using LogDate
'''
from Dating import Dating
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import check_output

class Dating_LogDate(Dating):
    def init():
        raise ValueError("Dating_LogDate is not functional (yet)")

    def finalize():
        pass

    def cite():
        return GC.CITATION_LOGDATE

    def blurb():
        return "The rooted phylogeny was dated using LogDate (Mai & Mirarab, 2019)."

    def date(rooted_tree_filename, sample_times_filename):
        if not isfile(rooted_tree_filename):
            raise ValueError("Invalid tree file: %s" % rooted_tree_filename)
        if not isfile(sample_times_filename):
            raise ValueError("Invalid sample times file: %s" % sample_times_filename)
        logdate_dir = '%s/LogDate' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/dated.tre' % GC.OUT_DIR_OUTFILES
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Dated tree exists. Skipping recomputation.")
        else:
            makedirs(logdate_dir, exist_ok=True)
            logdate_times_filename = '%s/times_logdate.txt' % logdate_dir
            f = open(logdate_times_filename, 'w'); f.write(GC.convert_dates_LSD(sample_times_filename)); f.close()
            logdate_output_filename = '%s/output_dated.tre' % logdate_dir
            msa = GC.read_fasta(GC.ALIGNMENT)
            msa_columns = len(msa[list(msa.keys())[0]])
            command = ['LogDate.py', '-i', rooted_tree_filename, '-t', logdate_times_filename, '-l', str(msa_columns), '-o', logdate_output_filename]
            f = open('%s/command.txt' % logdate_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            print(check_output(command).decode())
            exit()
            GC.write_file(check_output(command).decode(), out_filename)
        return out_filename
