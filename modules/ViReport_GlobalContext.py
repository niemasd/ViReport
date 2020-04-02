#! /usr/bin/env python3
'''
Store global variables/functions to be accessible by all ViReport modules
'''
from datetime import datetime,timedelta
from gzip import open as gopen
from math import log2
from matplotlib.ticker import MaxNLocator
from os import walk
from os.path import getsize,isdir,isfile,join
from pdf2image import convert_from_path
from PIL import Image
from seaborn import barplot,distplot
from treeswift import read_tree_newick
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
Image.MAX_IMAGE_PIXELS = 1000000000 # to avoid PIL decompression bomb warnings

# useful constants
VIREPORT_VERSION = '0.0.1'
SAFE_CHARS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
CIGAR_LETTERS = {'M','D','I','S','H','=','X'}
COMPLEMENT = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
CITATION_CLUSTALOMEGA = 'Sievers F., Wilm A., Dineen D.G., Gibson T.J., Karplus K., Li W., Lopez R., McWilliam H., Remmert M., Söding J., Thompson J.D., Higgins D.G. (2011). "Fast, scalable generation of high-quality protein multiple sequence alignments using Clustal Omega". Molecular Systems Biology. 7, 539.'
CITATION_FASTTREE = 'Price M.N., Dehal P.S., Arkin A.P. (2010). "FastTree 2 -- Approximately Maximum-Likelihood Trees for Large Alignments". PLoS ONE. 5(3), e9490.'
CITATION_FSA = 'Bradley R.K., Roberts A., Smoot M., Juvekar S., Do J., Dewey C., Holmes I., Pachter L. (2009). "Fast Statistical Alignment". PLoS Computational Biology. 5(5), e1000392.'
CITATION_HIVTRACE = 'Pond S.L.K., Weaver S., Leigh Brown A.J., Wertheim J.O. (2018). "HIV-TRACE (TRAnsmission Cluster Engine): a Tool for Large Scale Molecular Epidemiology of HIV-1 and Other Rapidly Evolving Pathogens". Molecular Biology and Evolution. 35(7), 1812-1819.'
CITATION_IQTREE = 'Nguyen L.T., Schmidt H.A., von Haeseler A., Minh B.Q. (2015). "IQ-TREE: A fast and effective stochastic algorithm for estimating maximum likelihood phylogenies". Molecular Biology and Evolution. 32(1), 268-274.'
CITATION_IQTREE_MFP = 'Kalyaanamoorthy S., Minh B.Q., Wong T.K.F., von Haeseler A., Jermiin L.S. (2017). "ModelFinder: Fast model selection for accurate phylogenetic estimates". Nature Methods. 14, 587-589.'
CITATION_KALIGN = 'Lassmann T. (2019). "Kalign 3: multiple sequence alignment of large data sets". Bioinformatics. 36(6), 1928-1929.'
CITATION_LOGDATE = 'Mai U., Mirarab S. (2019). "Log Transformation Improves Dating of Phylogenies". bioRxiv.'
CITATION_LSD2 = 'To T.H., Jung M., Lycett S., Gascuel O. (2016). "Fast dating using least-squares criteria and algorithms". Systematic Biology. 65(1), 82-97.'
CITATION_MAFFT = 'Katoh K., Standley D.M. (2013). "MAFFT Multiple Sequence Alignment Software Version 7: Improvements in Performance and Usability". Molecular Biology and Evolution. 30(4), 772-780.'
CITATION_MINIMAP2 = 'Li H. (2018). "Minimap2: pairwise alignment for nucleotide sequences". Bioinformatics. 34(18), 3094-3100.'
CITATION_MINVAR = 'Mai U., Sayyari E., Mirarab S. (2017). "Minimum Variance Rooting of Phylogenetic Trees and Implications for Species Tree Reconstruction". PLoS ONE. 12(8), e0182238.'
CITATION_MODEL_GTR = 'Tavare S. (1986). ""Some Probabilistic and Statistical Problems in the Analysis of DNA Sequences". Lectures on Mathematics in the Life Sciences. 17, 57-86.'
CITATION_MODEL_LG = 'Le S.Q., Gascuel O. (2008). "An Improved General Amino Acid Replacement Matrix". Molecular Biology and Evolution. 25(7), 1307-1320.'
CITATION_MUSCLE = 'Edgar R.C. (2004). "MUSCLE: multiple sequence alignment with high accuracy and high throughput". Nucleic Acids Research. 32(5), 1792-1797.'
CITATION_PHYML = 'Guindon S., Dufayard J.F., Lefort V., Anisimova M., Hordijk W., Gascuel O. (2010). "New Algorithms and Methods to Estimate Maximum-Likelihood Phylogenies: Assessing the Performance of PhyML 3.0". Systematic Biology. 59(3), 307-321.'
CITATION_PRANK = 'Loytynoja A. (2013). "Phylogeny-aware alignment with PRANK". Methods in Molecular Biology. 1079, 155-170.'
CITATION_RAXML_NG = 'Kozlov A.M., Darriba D., Flouri T., Morel B., Stamatakis A. (2019). "RAxML-NG: A fast, scalable, and user-friendly tool for maximum likelihood phylogenetic inference". Bioinformatics. 35(21), 4453-4455.'
CITATION_TREEDATER = 'Volz E.M., Frost S.D.W. (2017). "Scalable relaxed clock phylogenetic dating". Virus Evolution. 3(2), vex025.'
CITATION_TREEN93 = 'Moshiri N. (2018). "TreeN93: a non-parametric distance-based method for inferring viral transmission clusters". bioRxiv.'
CITATION_TREESWIFT = 'Moshiri N. (2020). "TreeSwift: a massively scalable Python tree package". SoftwareX. In press.'
CITATION_TREETIME = 'Sagulenko P., Puller V., Neher R.A. (2018). "TreeTime: Maximum-likelihood phylodynamic analysis". Virus Evolution. 4(1), vex042.'
CITATION_VIREPORT = 'Moshiri N. (2020). "ViReport" (https://github.com/niemasd/ViReport).'

# return the current time as a string
def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# rstrip Gzip extension
def rstrip_gz(s):
    return s.rstrip('.gz').rstrip('.GZ').rstrip('.Gz').rstrip('.gZ')

# read a file and return the lines as a list of str
def read_file(fn):
    if fn.lower().endswith('.gz'):
        return [l.strip() for l in gopen(fn).read().decode().strip().splitlines()]
    else:
        return [l.strip() for l in open(fn).read().strip().splitlines()]

# write a str to a file
def write_file(s, fn):
    if fn.lower().endswith('.gz'):
        f = gopen(fn, 'wb', 9); f.write(s.encode())
    else:
        f = open(fn, 'w'); f.write(s)
    f.close()

# get the filesize of a file or folder
def filesize(p):
    if isfile(p):
        return getsize(p)
    elif isdir(p):
        out = 0
        for dirpath,dirnames,filenames in walk(p):
            for f in filenames:
                fp = join(dirpath, f)
                out += getsize(fp)
        return out
    else:
        raise ValueError("Path not found: %s" % p)

# convert a string to a "safe" string (all non-letter/digit characters --> underscore)
def safe(s):
    return ''.join(c if c in SAFE_CHARS else '_' for c in s)

# convert a number to a string, removing trailing 0s if applicable
def num_str(n, dec_sigfigs=3):
    s = str(n)
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
        if '.' in s:
            left,right = s.split('.')
            round_places = dec_sigfigs
            for c in right:
                if c == '0':
                    round_places += 1
                else:
                    break
            return str(round(float(s), round_places)).rstrip('0').rstrip('.')
        else:
            return s
    else:
        return s

# get the reverse complement of a DNA string
def rev_comp(s):
    return ''.join(COMPLEMENT[c] if c in COMPLEMENT else c for c in s.upper()[::-1])

# parse a CIGAR string
def parse_cigar(s):
    out = list(); ind = len(s)-1
    while ind >= 0:
        let = s[ind]; ind -= 1; num = ''
        while s[ind] not in CIGAR_LETTERS:
            num += s[ind]; ind -= 1
        out.append((let, int(num[::-1])))
    return out[::-1]

# check if a FASTA file contains DNA or protein sequences
def predict_seq_type(filename, thresh=0.8):
    if not isfile(filename):
        raise ValueError("Invalid FASTA file: %s" % filename)
    count = dict()
    for line in read_file(filename):
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
    return [[v.strip() for v in l.strip().split('\t')] for l in read_file(dates_filename) if len(l.strip()) != 0]

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

# read a FASTA file as a dictionary (keys = IDs, values = sequences)
def read_fasta(seqs_filename):
    if not isfile(seqs_filename):
        raise ValueError("Invalid sequence file: %s" % seqs_filename)
    out = dict(); ID = None; seq = None
    for line in read_file(seqs_filename):
        l = line.strip()
        if len(l) == 0:
            continue
        if l[0] == '>':
            if ID is not None:
                out[ID] = seq
            ID = l[1:]; seq = ''
        else:
            seq += l
    out[ID] = seq
    return out

# remove outgroups from a FASTA
def remove_outgroups_fasta(seqs_filename, outgroups_filename):
    if outgroups_filename is None:
        return seqs_filename
    if not isfile(seqs_filename):
        raise ValueError("Invalid sequence file: %s" % seqs_filename)
    outgroups = {l.strip() for l in read_file(outgroups_filename)}
    out_filename = '%s.no_outgroup.%s' % ('.'.join(rstrip_gz(seqs_filename).split('.')[:-1]), rstrip_gz(seqs_filename).split('.')[-1])
    if GZIP_OUTPUT:
        out_filename += '.gz'
    seqs = read_fasta(seqs_filename)
    for o in outgroups:
        if o in seqs:
            del seqs[o]
    valid_pos = None
    for s in seqs.values():
        if valid_pos is None:
            valid_pos = [False for _ in range(len(s))]
        for i,c in enumerate(s.upper()):
            if c != '-' and c != 'N':
                valid_pos[i] = True
    out_lines = list()
    for k in sorted(seqs.keys()):
        out_lines.append('>%s' % k)
        seq = ''
        for i,c in enumerate(seqs[k].upper()):
            if valid_pos[i]:
                seq += c
        out_lines.append(seq)
    write_file('\n'.join(out_lines), out_filename)
    return out_filename

# remove outgroups from a Newick tree
def remove_outgroups_newick(tree_filename, outgroups_filename):
    if outgroups_filename is None:
        return tree_filename
    if not isfile(tree_filename):
        raise ValueError("Invalid tree file: %s" % tree_filename)
    outgroups = {l.strip() for l in read_file(outgroups_filename)}
    tree = read_tree_newick(tree_filename)
    out_filename = '%s.no_outgroup.%s' % ('.'.join(rstrip_gz(tree_filename).split('.')[:-1]), rstrip_gz(tree_filename).split('.')[-1])
    if GZIP_OUTPUT:
        out_filename += '.gz'
    tree_no_og = tree.extract_tree_without(outgroups)
    tree_no_og.root.edge_length = None
    write_file('%s\n' % tree_no_og.newick().lstrip('[&R] '), out_filename)
    return out_filename

# read transmission clusters in the TreeCluster format and return (clusters, singletons)
def read_transmission_clusters(clusters_filename):
    if not isfile(clusters_filename):
        raise ValueError("Invalid transmission clustering file: %s" % clusters_filename)
    clusters = dict()
    for line in read_file(clusters_filename):
        if line.startswith('SequenceName\t'):
            continue
        u,c = [v.strip() for v in line.strip().split('\t')]
        if c not in clusters:
            clusters[c] = set()
        clusters[c].add(u)
    if '-1' in clusters:
        singletons = clusters['-1']; del clusters['-1']
    else:
        singletons = set()
    return clusters,singletons

# return the number of sequences in a FASTA file
def num_seqs_fasta(seqs_filename):
    if not isfile(seqs_filename):
        raise ValueError("Invalid sequence file: %s" % seqs_filename)
    return sum(l.startswith('>') for l in read_file(seqs_filename))

# return the lengths of the sequences in a FASTA file
def seq_lengths_fasta(seqs_filename):
    if not isfile(seqs_filename):
        raise ValueError("Invalid sequence file: %s" % seqs_filename)
    out = list(); curr = None
    for line in read_file(seqs_filename):
        l = line.strip()
        if len(l) == 0:
            continue
        if l[0] == '>':
            if curr is not None:
                out.append(curr)
            curr = 0
        else:
            curr += len(l)
    out.append(curr)
    return out

# read a FASTA file and convert it to a single string in the Phylip format
def fasta_to_phylip(seqs_filename):
    if not isfile(seqs_filename):
        raise ValueError("Invalid sequence file: %s" % seqs_filename)
    seqs = read_fasta(seqs_filename)
    return "%d %d\n%s" % (len(seqs), len(seqs[list(seqs.keys())[0]]), '\n'.join("%s %s" % (k, seqs[k]) for k in seqs))

# count the number of invariant sites in a multiple sequence alignment
def num_invariant_sites(aln_filename):
    if isinstance(aln_filename, dict):
        aln = aln_filename
    else:
        if not isfile(aln_filename):
            raise ValueError("Invalid alignment file: %s" % aln_filename)
        aln = read_fasta(aln_filename)
    n = len(aln[list(aln.keys())[0]]); nucs = [set() for _ in range(n)]
    for k in aln:
        s = aln[k]
        for i in range(n):
            if s[i] != '-':
                nucs[i].add(s[i])
    return sum(len(x) <= 1 for x in nucs)

# color the internal nodes of a tree if all their children are the same color
def color_internal(tree):
    for node in tree.traverse_postorder(leaves=False):
        if hasattr(node.children[0], 'color'):
            color = node.children[0].color
        else:
            color = None
        for child in node.children[1:]:
            if not hasattr(child, 'color') or child.color != color:
                color = None; break
        if color is not None:
            node.color = color

# compute the Shannon entropy of each position of an MSA
def msa_shannon_entropy(msa):
    freq = None # freq[i] = dict of character frequencies at position i of MSA
    for s in msa.values():
        if freq is None:
            freq = [dict() for _ in range(len(s))]
        for i,c in enumerate(s.upper()):
            if c not in freq[i]:
                freq[i][c] = 0
            freq[i][c] += 1
    for p in freq:
        for c in ['-','N','n']:
            if c in p:
                del p[c]
        tot = sum(p.values())
        for c in p:
            p[c] /= tot
    return [0 if len(p) == 0 else -sum(p[c]*log2(p[c]) for c in p) for p in freq]

# compute the coverage of each position of an MSA
def msa_coverage(msa, seq_type='DNA'):
    tot = 0.; cov = None # cov[i] = number of sequences with non-gap (and non-N for DNA)
    for s in msa.values():
        tot += 1
        if cov is None:
            cov = [0 for _ in range(len(s))]
        for i,c in enumerate(s.upper()):
            if (seq_type == 'DNA' and c not in {'-','N'}) or (seq_type == 'AA' and c not in {'-'}):
                cov[i] += 1
    return [v/tot for v in cov]

# convert a PDF to PNG
def pdf_to_png(pdf_filename, png_filename):
    convert_from_path(pdf_filename, dpi=300, size=(1500,None))[0].save(png_filename, 'PNG')

# create a Manhattan plot from a list of y-coordinates
def create_manhattan(data, filename, sig_thresh=None, insig_color='black', sig_color='red', sig_linestyle='--', dot_size=None, xlabel=None, ylabel=None, title=None, xmin=None, xmax=None, ymin=None, ymax=None, xlog=None, ylog=None):
    fig, ax = plt.subplots()
    if sig_thresh is None:
        colors = [insig_color]*len(data)
    else:
        colors = [insig_color if y < sig_thresh else sig_color for y in data]
        plt.plot([1,len(data)], [sig_thresh,sig_thresh], color=sig_color, linestyle=sig_linestyle)
    plt.scatter(list(range(1,len(data)+1)), data, s=dot_size, c=colors)
    if title is not None:
        plt.title(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if xlog:
        ax.set_xscale('log')
    if ylog:
        ax.set_yscale('log')
    if xmin is not None and xmax is not None:
        plt.xlim(xmin,xmax)
    elif xmin is not None:
        plt.xlim(xmin=xmin)
    elif xmax is not None:
        plt.xlim(xmax=xmax)
    if ymin is not None and ymax is not None:
        plt.ylim(ymin,ymax)
    elif ymin is not None:
        plt.ylim(ymin=ymin)
    elif ymax is not None:
        plt.ylim(ymax=ymax)
    plt.tight_layout()
    fig.savefig(filename)
    plt.close()

# create a histogram figure from a list of numbers
def create_histogram(data, filename, kde=True, hist=True, xlabel=None, ylabel=None, title=None, xmin=None, xmax=None, ymin=None, ymax=None, xlog=False, ylog=False, kde_linestyle='-'):
    if not kde and not hist:
        raise ValueError("kde or hist (or both) must be True")
    fig, ax = plt.subplots()
    kde_kws = {'linestyle':kde_linestyle}; hist_kws = dict()
    distplot(data, kde=kde, hist=hist, kde_kws=kde_kws, hist_kws=hist_kws)
    if title is not None:
        plt.title(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if xlog:
        ax.set_xscale('log')
    if ylog:
        ax.set_yscale('log')
    if xmin is not None and xmax is not None:
        plt.xlim(xmin,xmax)
    elif xmin is not None:
        plt.xlim(xmin=xmin)
    elif xmax is not None:
        plt.xlim(xmax=xmax)
    if ymin is not None and ymax is not None:
        plt.ylim(ymin,ymax)
    elif ymin is not None:
        plt.ylim(ymin=ymin)
    elif ymax is not None:
        plt.ylim(ymax=ymax)
    plt.tight_layout()
    fig.savefig(filename)
    plt.close()

# create a barplot from a list of labels
def create_barplot(data, filename, horizontal=False, all_labels=None, xlabel=None, ylabel=None, title=None, ymin=None, ymax=None, ylog=None, hide_labels=False, rotate_labels=0):
    count = dict(); x = list()
    for l in data:
        if l in count:
            count[l] += 1
        else:
            count[l] = 1; x.append(l)
    if all_labels is not None:
        x = all_labels
    y = [count[l] if l in count else 0 for l in x]
    if horizontal:
        fig, ax = plt.subplots(figsize=(8,max(2.5,0.2*len(x))))
        bp = barplot(x=y, y=x, ax=ax)
    else:
        fig, ax = plt.subplots()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        bp = barplot(x=x, y=y, ax=ax)
    if title is not None:
        plt.title(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if ylog:
        ax.set_yscale('log')
    if ymin is not None and ymax is not None:
        plt.ylim(ymin,ymax)
    elif ymin is not None:
        plt.ylim(ymin=ymin)
    elif ymax is not None:
        plt.ylim(ymax=ymax)
    if rotate_labels != 0:
        plt.xticks(rotation=rotate_labels)
    if hide_labels:
        ax.set_xticks(list())
    else:
        xticks = ax.xaxis.get_major_ticks()
        if len(x) < 20:
            den = 1
        else:
            den = int(len(x)/20)
        for ind, label in enumerate(bp.get_xticklabels()):
            if ind % den != 0:
                label.set_visible(False)
                xticks[ind].set_visible(False)
    plt.tight_layout()
    fig.savefig(filename)
    plt.close()
