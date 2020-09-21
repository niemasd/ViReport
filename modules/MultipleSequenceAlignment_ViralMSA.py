#! /usr/bin/env python3
'''
Implementation of the "MultipleSequenceAlignment" module using ViralMSA wrapping around Minimap2
'''
from MultipleSequenceAlignment import MultipleSequenceAlignment
import ViReport_GlobalContext as GC
from glob import glob
from os import makedirs,rmdir
from os.path import isfile
from shutil import move
from subprocess import call

class MultipleSequenceAlignment_ViralMSA(MultipleSequenceAlignment):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return [GC.CITATION_VIRALMSA, GC.CITATION_MINIMAP2]

    def blurb():
        return "Multiple sequence alignment was performed using ViralMSA (Moshiri, 2020) wrapped around Minimap2 (Li, 2018) using the reference sequence %s." % GC.INPUT_REF_ID

    def align(seqs_filename, ref_id):
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        viralmsa_dir = '%s/ViralMSA' % GC.OUT_DIR_TMPFILES
        viralmsa_tmp_dir = '%s/tmp' % viralmsa_dir
        out_filename = '%s/%s.aln' % (GC.OUT_DIR_OUTFILES, '.'.join(GC.rstrip_gz(seqs_filename.split('/')[-1]).split('.')[:-1]))
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Multiple sequence alignment exists. Skipping recomputation.")
        else:
            if ref_id is None:
                raise ValueError("ViralMSA requires a reference sequence")
            if GC.EMAIL is None:
                raise ValueError("ViralMSA requires an email address")
            makedirs(viralmsa_dir, exist_ok=True)
            if seqs_filename.lower().endswith('.gz'):
                unzipped_filename = '%s/seqs_unzipped.fas' % viralmsa_dir
                GC.write_file('\n'.join(GC.read_file(seqs_filename)), unzipped_filename)
                seqs_filename = unzipped_filename
            command = ['ViralMSA.py', '-e', GC.EMAIL, '-s', seqs_filename, '-o', viralmsa_tmp_dir, '-r', ref_id, '--omit_ref']
            if GC.NUM_THREADS is not None:
                command += ['-t', str(GC.NUM_THREADS)]
            f = open('%s/command.txt' % viralmsa_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            f_stdout = open('%s/log.txt' % viralmsa_dir, 'w')
            call(command, stdout=f_stdout); f_stdout.close()
            move('%s/%s.aln' % (viralmsa_tmp_dir, seqs_filename.split('/')[-1]), out_filename)
            for f in glob('%s/*' % viralmsa_tmp_dir):
                move(f, '%s/%s' % (viralmsa_dir, f.split('/')[-1]))
            rmdir(viralmsa_tmp_dir)
        return out_filename
