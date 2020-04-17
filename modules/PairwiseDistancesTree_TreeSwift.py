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
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Pairwise phylogenetic distances exist. Skipping recomputation.")
        else:
            tree = read_tree_newick(tree_filename); leaf_dists = dict()
            out = open(out_filename, 'w'); out.write("ID1,ID2,Distance\n")
            for node in tree.traverse_postorder():
                if node.is_leaf():
                    leaf_dists[node] = [[node,0]]
                else:
                    for c in node.children:
                        if c.edge_length is not None:
                            for i in range(len(leaf_dists[c])):
                                leaf_dists[c][i][1] += c.edge_length
                    for c1 in range(0,len(node.children)-1):
                        leaves_c1 = leaf_dists[node.children[c1]]
                        for c2 in range(c1+1,len(node.children)):
                            leaves_c2 = leaf_dists[node.children[c2]]
                            for i in range(len(leaves_c1)):
                                for j in range(len(leaves_c2)):
                                    u,ud = leaves_c1[i]; v,vd = leaves_c2[j]; d = ud+vd
                                    out.write(u.label); out.write(','); out.write(v.label); out.write(','); out.write(str(d)); out.write('\n')
                    leaf_dists[node] = leaf_dists[node.children[0]]; del leaf_dists[node.children[0]]
                    for i in range(1,len(node.children)):
                        leaf_dists[node] += leaf_dists[node.children[i]]; del leaf_dists[node.children[i]]
            out.close()
        return out_filename
