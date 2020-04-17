#! /usr/bin/env python3
'''
Implementation of the "Dating" module using LSD2
'''
from Dating import Dating
import ViReport_GlobalContext as GC
from glob import glob
from os import makedirs
from os.path import isfile
from shutil import move
from subprocess import check_output

class Dating_LSD2(Dating):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_LSD2

    def blurb():
        return "The rooted phylogeny was dated using LSD2 (To et al., 2016) using temporal constraints."

    def date(rooted_tree_filename, sample_times_filename):
        if not isfile(rooted_tree_filename):
            raise ValueError("Invalid tree file: %s" % rooted_tree_filename)
        if not isfile(sample_times_filename):
            raise ValueError("Invalid sample times file: %s" % sample_times_filename)
        lsd2_dir = '%s/LSD2' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/dated.tre' % GC.OUT_DIR_OUTFILES
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Dated tree exists. Skipping recomputation.")
        else:
            makedirs(lsd2_dir, exist_ok=True)
            log_filename = '%s/log.txt' % lsd2_dir
            lsd_times_filename = '%s/times_lsd.txt' % lsd2_dir
            f = open(lsd_times_filename, 'w'); f.write(GC.convert_dates_LSD(sample_times_filename)); f.close()
            if rooted_tree_filename.lower().endswith('.gz'):
                unzipped_filename = '%s/tree_unzipped.tre' % lsd2_dir
                GC.write_file('\n'.join(GC.read_file(rooted_tree_filename)), unzipped_filename)
                rooted_tree_filename = unzipped_filename
            command = ['lsd2', '-c', '-i', rooted_tree_filename, '-d', lsd_times_filename]
            f = open('%s/command.txt' % lsd2_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            o = check_output(command)
            move('%s.result.nwk' % rooted_tree_filename, out_filename)
            for f in glob('%s.*' % rooted_tree_filename):
                move(f, '%s/%s' % (lsd2_dir, f.split('/')[-1]))
        return out_filename
