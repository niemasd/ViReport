#! /usr/bin/env python3
'''
Implementation of the "Preprocessing" module where sequences are given safe names (non-letters/digits --> underscore)
'''
from Preprocessing import Preprocessing
import ViReport_GlobalContext as GC
from os.path import isfile

class Preprocessing_SafeNames(Preprocessing):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def blurb():
        return "The input dataset was preprocessed such that sequences were given safe names: non-letters/digits in sequence IDs were converted to underscores."

    def preprocess(seqs_filename, ref_id, sample_times_filename, outgroups_filename, categories_filename):
        # set things up
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        if not isfile(sample_times_filename):
            raise ValueError("Invalid sample times file: %s" % sample_times_filename)
        out_seqs_filename = '%s/sequences_safe.fas' % GC.OUT_DIR_OUTFILES
        out_times_filename = '%s/times_safe.txt' % GC.OUT_DIR_OUTFILES
        if outgroups_filename is None:
            out_outgroups_filename = None
        else:
            if not isfile(outgroups_filename):
                raise ValueError("Invalid outgroups list file: %s" % outgroups_filename)
            out_outgroups_filename = '%s/outgroups_safe.txt' % GC.OUT_DIR_OUTFILES
        if categories_filename is None:
            out_categories_filename = None
        else:
            if not isfile(categories_filename):
                raise ValueError("Invalid sample categories file: %s" % categories_filename)
            out_categories_filename = '%s/categories_safe.txt' % GC.OUT_DIR_OUTFILES

        # output safe sequences
        if isfile(out_seqs_filename) or isfile('%s.gz' % out_seqs_filename):
            GC.SELECTED['Logging'].writeln("Safename sequences exist. Skipping recomputation.")
        else:
            lines = GC.read_file(seqs_filename)
            for i in range(len(lines)):
                if lines[i].startswith('>'):
                    lines[i] = ">%s" % GC.safe(lines[i][1:])
            GC.write_file('\n'.join(lines), out_seqs_filename)
        if ref_id is None:
            out_ref_id = None
        else:
            out_ref_id = GC.safe(ref_id)

        # output safe sample times
        if isfile(out_times_filename) or isfile('%s.gz' % out_times_filename):
            GC.SELECTED['Logging'].writeln("Safename sample times exist. Skipping recomputation.")
        else:
            lines = [l.strip().split('\t') for l in GC.read_file(sample_times_filename)]
            GC.write_file('\n'.join('%s\t%s' % (GC.safe(u),t) for u,t in lines), out_times_filename)

        # output safe outgroup names
        if outgroups_filename is not None:
            if isfile(out_outgroups_filename) or isfile('%s.gz' % out_outgroups_filename):
                GC.SELECTED['Logging'].writeln("Safename outgroups exist. Skipping recomputation.")
            else:
                GC.write_file('\n'.join(GC.safe(l.strip()) for l in GC.read_file(outgroups_filename)), out_outgroups_filename)

        # output safe categories
        if categories_filename is not None:
            if isfile(out_categories_filename) or isfile('%s.gz' % out_categories_filename):
                GC.SELECTED['Logging'].writeln("Safename sample categories exist. Skipping recomputation.")
            else:
                lines = [l.strip().split('\t') for l in GC.read_file(categories_filename)]
                GC.write_file('\n'.join('%s\t%s' % (GC.safe(u),c) for u,c in lines), out_categories_filename)

        # return output filenames
        return out_seqs_filename, out_ref_id, out_times_filename, out_outgroups_filename, out_categories_filename
