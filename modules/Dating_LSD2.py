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

    def date(rooted_tree_filename, sample_times_filename):
        if not isfile(rooted_tree_filename):
            raise ValueError("Invalid tree file: %s" % rooted_tree_filename)
        if not isfile(sample_times_filename):
            raise ValueError("Invalid sample times file: %s" % sample_times_filename)
        lsd2_dir = '%s/LSD2' % GC.OUT_DIR_TMPFILES
        makedirs(lsd2_dir, exist_ok=True)
        out_filename = '%s/dated.tre' % GC.OUT_DIR_OUTFILES
        log_filename = '%s/log.txt' % lsd2_dir
        #command = ['FastRoot.py', '-i', tree_filename, '-m', 'MV']
        command = ['lsd2', '-c', '-i', rooted_tree_filename, '-d', sample_times_filename]
        f = open('%s/command.txt' % lsd2_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
        o = check_output(command)
        move('%s.result' % rooted_tree_filename, out_filename)
        for f in glob('%s.*' % rooted_tree_filename):
            move(f, '%s/%s' % (lsd2_dir, f.split('/')[-1]))
        return out_filename
