#! /usr/bin/env python3
'''
Implementation of the "PairwiseDistancesTree" module using tn93
'''
from PairwiseDistancesTree import PairwiseDistancesTree
import ViReport_GlobalContext as GC
from os.path import isfile
from treeswift import read_tree_newick

class PairwiseDistancesTree_TreeSwift(PairwiseDistancesTree):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_TREESWIFT

    def blurb():
        return "Pairwise distances were computed from the phylogeny using TreeSwift (Moshiri, 2020)."

    def pairwise_distances(tree_filename):
        if not isfile(tree_filename):
            raise ValueError("Invalid tree file: %s" % tree_filename)
        out_filename = '%s/pairwise_distances_phylogeny.csv' % GC.OUT_DIR_OUTFILES
        out = open(out_filename, 'w'); out.write("ID1,ID2,Distance\n")
        dm = read_tree_newick(tree_filename).distance_matrix(leaf_labels=True)
        labels = sorted(dm.keys())
        for i in range(len(labels)-1):
            u = labels[i]
            for j in range(i+1, len(labels)):
                v = labels[j]
                out.write(u); out.write(',')
                out.write(v); out.write(',')
                out.write(GC.num_str(dm[u][v])); out.write('\n')
        return out_filename
