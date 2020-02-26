#! /usr/bin/env python3
'''
Store global variables/functions to be accessible by all ViReport modules
'''
from datetime import datetime,timedelta
from os.path import isfile

# useful constants
VIREPORT_VERSION = '0.0.1'
SAFE_CHARS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
CITATION_CLUSTALOMEGA = 'Sievers F., Wilm A., Dineen D.G., Gibson T.J., Karplus K., Li W., Lopez R., McWilliam H., Remmert M., Söding J., Thompson J.D., Higgins D.G. (2011). "Fast, scalable generation of high-quality protein multiple sequence alignments using Clustal Omega". Molecular Systems Biology. 7, 539.'
CITATION_FASTTREE = 'Price M.N., Dehal P.S., Arkin A.P. (2010). "FastTree 2 -- Approximately Maximum-Likelihood Trees for Large Alignments". PLoS ONE. 5(3), e9490.'
CITATION_IQTREE = 'Nguyen L.T., Schmidt H.A., von Haeseler A., Minh B.Q. (2015). "IQ-TREE: A fast and effective stochastic algorithm for estimating maximum likelihood phylogenies". Molecular Biology and Evolution. 32(1), 268-274.'
CITATION_IQTREE_MFP = 'Kalyaanamoorthy S., Minh B.Q., Wong T.K.F., von Haeseler A., Jermiin L.S. (2017). "ModelFinder: Fast model selection for accurate phylogenetic estimates". Nature Methods. 14, 587-589.'
CITATION_LSD2 = 'To T.H., Jung M., Lycett S., Gascuel O. (2016). "Fast dating using least-squares criteria and algorithms". Systematic Biology. 65(1), 82-97.'
CITATION_MAFFT = 'Katoh K., Standley D.M. (2013). "MAFFT Multiple Sequence Alignment Software Version 7: Improvements in Performance and Usability". Molecular Biology and Evolution. 30(4), 772-780.'
CITATION_MINVAR = 'Mai U., Sayyari E., Mirarab S. (2017). "Minimum Variance Rooting of Phylogenetic Trees and Implications for Species Tree Reconstruction". PLoS ONE. 12(8), e0182238.'
CITATION_MUSCLE = 'Edgar R.C. (2004). "MUSCLE: multiple sequence alignment with high accuracy and high throughput". Nucleic Acids Research. 32(5), 1792-1797.'
CITATION_RAXML_NG = 'Kozlov A.M., Darriba D., Flouri T., Morel B., Stamatakis A. (2019). "RAxML-NG: A fast, scalable, and user-friendly tool for maximum likelihood phylogenetic inference". Bioinformatics. 35(21), 4453-4455.'
CITATION_TREEDATER = 'Volz E.M., Frost S.D.W. (2017). "Scalable relaxed clock phylogenetic dating". Virus Evolution. 3(2), vex025.'
CITATION_VIREPORT = 'Moshiri N. (2020). "ViReport" (https://github.com/niemasd/ViReport).'

# convert a string to a "safe" string (all non-letter/digit characters --> underscore)
def safe(s):
    return ''.join(c if c in SAFE_CHARS else '_' for c in s)

# check if a FASTA file contains DNA or protein sequences
def predict_seq_type(filename, thresh=0.8):
    if not isfile(filename):
        raise ValueError("Invalid FASTA file: %s" % filename)
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

# convert a date (YYYY-MM-DD) to days since 0001-01-01
def date_to_days(sample_time):
    num_dashes = sample_time.count('-')
    if num_dashes == 2:   # YYYY-MM-DD
        tmp = datetime.strptime(sample_time, '%Y-%m-%d')
    elif num_dashes == 1: # YYYY-MM(-01)
        tmp = datetime.strptime('%s-01' % sample_time, '%Y-%m-%d')
    elif num_dashes == 0: # YYYY(-01-01)
        tmp = datetime.strptime('%s-01-01' % sample_time, '%Y-%m-%d')
    else:
        raise ValueError("Invalid sample date (should be YYYY-MM-DD): %s" % sample_time)
    return (tmp - datetime(1,1,1)).days # days since 0001-01-01

# convert days since 0001-01-01 to a date (YYYY-MM-DD)
def days_to_date(days):
    return (datetime(1,1,1) + timedelta(days=days)).strftime('%Y-%m-%d')

# load ViReport sample times as a list of [ID, time] pairs
def load_dates_ViReport(dates_filename):
    return [[v.strip() for v in l.strip().split('\t')] for l in open(dates_filename) if len(l.strip()) != 0]

# read sample times in the ViReport format and return a single string in the LSD format
def convert_dates_LSD(dates_filename):
    if not isfile(dates_filename):
        raise ValueError("Invalid dates file: %s" % dates_filename)
    times = load_dates_ViReport(dates_filename)
    return "%d\n%s" % (len(times), '\n'.join("%s %s" % (u,date_to_days(t)) for u,t in times))

# read sample times in the ViReport format and return a single string in the treedater format
def convert_dates_treedater(dates_filename):
    if not isfile(dates_filename):
        raise ValueError("Invalid dates file: %s" % dates_filename)
    times = load_dates_ViReport(dates_filename)
    return '\n'.join("%s,%s" % (u,date_to_days(t)) for u,t in times)
