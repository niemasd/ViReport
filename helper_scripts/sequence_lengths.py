#! /usr/bin/env python3
'''
Plot histogram (and/or KDE) of sequence lengths (gaps excluded)
'''
from gzip import open as gopen
from matplotlib.ticker import MaxNLocator
from seaborn import distplot
from sys import stdin
import argparse
import matplotlib.pyplot as plt

def fasta_lengths(lines, keep_gaps=False):
    out = list(); curr = 0
    for l in lines:
        if len(l.strip()) == 0:
            continue
        if l[0] == '>' and curr != 0:
            out.append(curr); curr = 0
        elif l[0] != '>':
            if keep_gaps:
                curr += len(l.strip())
            else:
                curr += len(l.strip().replace('-',''))
    out.append(curr)
    return out

if __name__ == "__main__":
    # parse args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input Sequences (FASTA)")
    parser.add_argument('-g', '--keep_gaps', action='store_true', help="Keep Gaps")
    parser.add_argument('-c', '--cumulative', action='store_true', help="Cumulative Density (instead of Probability Density)")
    parser.add_argument('-k', '--kde', action='store_true', help="Show Kernel Density Estimation (KDE)")
    parser.add_argument('-kl', '--kde_linestyle', required=False, type=str, default='-', help="KDE Linestyle")
    parser.add_argument('-nh', '--nohist', action='store_true', help="Hide Histogram")
    parser.add_argument('-b', '--binsize', required=False, type=float, default=None, help="Bin Size")
    parser.add_argument('-t', '--title', required=False, type=str, default=None, help="Figure Title")
    parser.add_argument('-xl', '--xlabel', required=False, type=str, default=None, help="X-Axis Label")
    parser.add_argument('-yl', '--ylabel', required=False, type=str, default=None, help="Y-Axis Label")
    parser.add_argument('-xmin', '--xmin', required=False, type=float, default=None, help="X-Axis Minimum")
    parser.add_argument('-xmax', '--xmax', required=False, type=float, default=None, help="X-Axis Maximum")
    parser.add_argument('-ymin', '--ymin', required=False, type=int, default=None, help="Y-Axis Minimum")
    parser.add_argument('-ymax', '--ymax', required=False, type=int, default=None, help="Y-Axis Maximum")
    parser.add_argument('-xlog', '--xlog', action='store_true', help="Log-Scaled X-Axis")
    parser.add_argument('-ylog', '--ylog', action='store_true', help="Log-Scaled Y-Axis")
    parser.add_argument('-xint', '--xint', action='store_true', help="Integer Ticks on X-Axis")
    parser.add_argument('-yint', '--yint', action='store_true', help="Integer Ticks on Y-Axis")
    args = parser.parse_args()
    assert args.kde or not args.nohist, "Must show either Histogram or Kernel Density Estimation (or both)"
    if args.input == 'stdin':
        lines = [l.strip() for l in stdin.read().strip().splitlines()]
    elif args.input.lower().endswith('.gz'):
        lines = [l.strip() for l in gopen(args.input).read().decode().strip().splitlines()]
    else:
        lines = [l.strip() for l in open(args.input).read().strip().splitlines()]
    data = fasta_lengths(lines, keep_gaps=args.keep_gaps)

    # create figure+axes
    fig, ax = plt.subplots()

    # set integer ticks (if applicable)
    if args.xint:
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if args.yint:
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # create custom bins (if applicable)
    MIN = min(data); MAX = max(data)
    if args.binsize:
        bins = [MIN]
        while bins[-1] < MAX:
            bins.append(bins[-1] + args.binsize)
    else:
        bins = None

    # plot the histogram
    kde_kws = {'linestyle':args.kde_linestyle}; hist_kws = dict()
    if args.cumulative:
        kde_kws['cumulative'] = True; hist_kws['cumulative'] = True
    distplot(data, bins=bins, kde=args.kde, hist=(not args.nohist), kde_kws=kde_kws, hist_kws=hist_kws)

    # set figure title and labels (if applicable)
    if args.title is not None:
        plt.title(args.title)
    if args.xlabel is not None:
        plt.xlabel(args.xlabel)
    if args.ylabel is not None:
        plt.ylabel(args.ylabel)

    # log-scale the axes (if applicable)
    if args.xlog:
        ax.set_xscale('log')
    if args.ylog:
        ax.set_yscale('log')

    # set X-axis range (if applicable)
    if args.xmin is not None and args.xmax is not None:
        plt.xlim(args.xmin,args.xmax)
    elif args.xmin is not None:
        plt.xlim(xmin=args.xmin)
    elif args.xmax is not None:
        plt.xlim(xmax=args.xmax)

    # set Y-axis range (if applicable)
    if args.ymin is not None and args.ymax is not None:
        plt.ylim(args.ymin,args.ymax)
    elif args.ymin is not None:
        plt.ylim(ymin=args.ymin)
    elif args.ymax is not None:
        plt.ylim(ymax=args.ymax)

    # clean up the figure and show
    plt.tight_layout()
    plt.show()
