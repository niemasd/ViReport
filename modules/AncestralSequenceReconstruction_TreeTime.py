#! /usr/bin/env python3
'''
Implementation of the "AncestralSequenceReconstruction" module using TreeTime
'''
from AncestralSequenceReconstruction import AncestralSequenceReconstruction
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from shutil import move
from subprocess import call
from treeswift import read_tree_newick

class AncestralSequenceReconstruction_TreeTime(AncestralSequenceReconstruction):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_TREETIME

    def blurb():
        return "Ancestral sequence reconstruction was performed using TreeTime (Sagulenko et al., 2018)."

    def reconstruct(rooted_tree_filename, aln_filename):
        if not isfile(rooted_tree_filename):
            raise ValueError("Invalid tree file: %s" % rooted_tree_filename)
        if not isfile(aln_filename):
            raise ValueError("Invalid alignment file: %s" % aln_filename)
        treetime_dir = '%s/TreeTime_AncestralSequenceReconstruction' % GC.OUT_DIR_TMPFILES
        makedirs(treetime_dir, exist_ok=True)
        out_filename = '%s/ancestral_sequences.fas' % GC.OUT_DIR_OUTFILES
        tree_with_internal_labels_filename = '%s/tree_with_internal_labels.tre' % treetime_dir
        log = open('%s/log.txt' % treetime_dir, 'w')
        tmp = read_tree_newick(rooted_tree_filename)
        for i,node in enumerate(tmp.traverse_levelorder(leaves=False)):
            if node.is_root():
                node.label = "ROOT"
            else:
                node.label = "I%d" % i
        f = open(tree_with_internal_labels_filename, 'w'); f.write(tmp.newick()); f.write('\n'); f.close()
        command = ['treetime', 'ancestral', '--aln', aln_filename, '--tree', tree_with_internal_labels_filename, '--outdir', treetime_dir]
        f = open('%s/command.txt' % treetime_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
        call(command, stdout=log)
        log.close()
        move('%s/ancestral_sequences.fasta' % treetime_dir, out_filename)
        return out_filename
