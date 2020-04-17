#! /usr/bin/env python3
'''
Implementation of the "Rooting" module using FastRoot to Midpoint-root
'''
from Rooting import Rooting
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import check_output

class Rooting_Midpoint(Rooting):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_MINVAR

    def blurb():
        return "The inferred phylogeny was Midpoint-rooted using FastRoot (Mai et al., 2017)."

    def root(tree_filename):
        if not isfile(tree_filename):
            raise ValueError("Invalid tree file: %s" % tree_filename)
        fastroot_dir = '%s/FastRoot' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/rooted.tre' % GC.OUT_DIR_OUTFILES
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Rooted phylogeny exists. Skipping recomputation.")
        else:
            makedirs(fastroot_dir, exist_ok=True)
            command = ['FastRoot.py', '-m', 'MP']
            f = open('%s/command.txt' % fastroot_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            GC.write_file(check_output(command, input='\n'.join(GC.read_file(tree_filename)).encode()).decode().replace("'",''), out_filename)
        return out_filename
