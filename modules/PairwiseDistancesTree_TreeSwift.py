#! /usr/bin/env python3
'''
Implementation of the "PairwiseDistancesTree" module using TreeSwift
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
        if GC.GZIP_OUTPUT:
            out_filename += '.gz'
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Pairwise phylogenetic distances exist. Skipping recomputation.")
        else:
            dm = read_tree_newick(tree_filename).distance_matrix(leaf_labels=True)
            labels = sorted(dm.keys())
            out_lines = ['ID1,ID2,Distance']
            for i in range(len(labels)-1):
                u = labels[i]
                for j in range(i+1, len(labels)):
                    v = labels[j]
                    out_lines.append('%s,%s,%s' % (u, v, GC.num_str(dm[u][v])))
            GC.write_file('\n'.join(out_lines), out_filename)
        return out_filename
