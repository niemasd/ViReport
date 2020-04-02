#! /usr/bin/env python3
'''
Given a FASTA file, output a filtered FASTA file containing only sequences within the specified length range
'''
from gzip import open as gopen
from sys import stdin,stdout
import argparse

if __name__ == "__main__":
    # parse args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input Sequences (FASTA)")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File (FASTA)")
    parser.add_argument('-m', '--min_length', required=False, type=int, default=0, help="Minimum Sequence Length")
    parser.add_argument('-M', '--max_length', required=False, type=int, default=float('inf'), help="Maximum Sequence Length")
    parser.add_argument('-g', '--keep_gaps', action='store_true', help="Keep Gaps")
    args = parser.parse_args()
    assert args.min_length <= args.max_length, "Minimum length must be <= maximum length"
    if args.input == 'stdin':
        lines = [l.strip() for l in stdin.read().strip().splitlines()]
    elif args.input.lower().endswith('.gz'):
        lines = [l.strip() for l in gopen(args.input).read().decode().strip().splitlines()]
    else:
        lines = [l.strip() for l in open(args.input).read().strip().splitlines()]
    GZIP_OUT = False
    if args.output == 'stdout':
        out = stdout
    elif args.output.lower().endswith('.gz'):
        out = gopen(args.output, 'wb', 9); GZIP_OUT = True
    else:
        out = open(args.output, 'w')

    # output filtered sequences
    ID = None; seq = None
    for l in lines:
        if len(l.strip()) == 0:
            continue
        if l[0] == '>':
            if ID is not None and args.min_length <= len(seq) <= args.max_length:
                curr = "%s\n%s\n" % (ID, seq)
                if GZIP_OUT:
                    out.write(curr.encode())
                else:
                    out.write(curr)
            ID = l.strip(); seq = ''
        else:
            if args.keep_gaps:
                seq += l.strip()
            else:
                seq += l.strip().replace('-','')
    if ID is not None and args.min_length <= len(seq) <= args.max_length:
        curr = "%s\n%s\n" % (ID, seq)
        if GZIP_OUT:
            out.write(curr.encode())
        else:
            out.write(curr)
