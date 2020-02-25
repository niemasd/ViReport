#! /usr/bin/env python3
'''
Store global variables/functions to be accessible by all ViReport modules
'''
from os.path import isfile

# useful constants
VIREPORT_VERSION = '0.0.1'
SAFE_CHARS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
CITATION_FASTTREE = 'Price, M.N., Dehal, P.S., Arkin, A.P. (2010). "FastTree 2 -- Approximately Maximum-Likelihood Trees for Large Alignments". PLoS ONE. 5(3), e9490.'
CITATION_IQTREE = 'Nguyen L.T., Schmidt H.A., von Haeseler A., Minh B.Q. (2015). "IQ-TREE: A fast and effective stochastic algorithm for estimating maximum likelihood phylogenies". Molecular Biology and Evolution. 32(1), 268-274.'
CITATION_IQTREE_MFP = 'Kalyaanamoorthy S., Minh B.Q., Wong T.K.F., von Haeseler A., Jermiin L.S. (2017). "ModelFinder: Fast model selection for accurate phylogenetic estimates". Nature Methods. 14, 587-589.'
CITATION_MAFFT = 'Katoh K., Standley D.M. (2013). "MAFFT Multiple Sequence Alignment Software Version 7: Improvements in Performance and Usability". Molecular Biology and Evolution. 30(4), 772-780.'
CITATION_MINVAR = 'Mai U., Sayyari E., Mirarab S. (2017). "Minimum Variance Rooting of Phylogenetic Trees and Implications for Species Tree Reconstruction". PLoS ONE. 12(8), e0182238.'
CITATION_VIREPORT = 'Moshiri N. (2020). "ViReport" (https://github.com/niemasd/ViReport).'

# convert a string to a "safe" string (all non-letter/digit characters --> underscore)
def safe(s):
    return ''.join(c if c in SAFE_CHARS else '_' for c in s)

# check if a FASTA file contains DNA or protein sequences
def predict_seq_type(filename, thresh=0.8):
    if not isfile(filename):
        print("Invalid FASTA file: %s" % filename)
    count = dict()
    for line in open(filename):
        l = line.strip()
        if len(l) == 0 or l[0] == '>':
            continue
        for c in l.upper():
            if c == '-':
                continue
            if c not in count:
                count[c] = 0
            count[c] += 1
    tot = sum(count[c] for c in count)
    acgt = sum(count[c] for c in 'ACGT' if c in count)
    if acgt > tot*thresh:
        return 'DNA'
    else:
        return 'AA' # amino acid
