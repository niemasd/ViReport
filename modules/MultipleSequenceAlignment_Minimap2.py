#! /usr/bin/env python3
'''
Implementation of the "MultipleSequenceAlignment" module using Minimap2
'''
from MultipleSequenceAlignment import MultipleSequenceAlignment
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import call

class MultipleSequenceAlignment_Minimap2(MultipleSequenceAlignment):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_MINIMAP2

    def blurb():
        return "Multiple sequence alignment was performed using Minimap2 (Li, 2018). Each input sequence was aligned to the reference sequence (%s), and the multiple sequence alignment was constructed based on positions in the reference." % GC.INPUT_REF_ID

    def align(seqs_filename, ref_id):
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        minimap2_dir = '%s/Minimap2' % GC.OUT_DIR_TMPFILES
        out_filename = '%s/%s.aln' % (GC.OUT_DIR_OUTFILES, '.'.join(GC.rstrip_gz(seqs_filename.split('/')[-1]).split('.')[:-1]))
        if GC.GZIP_OUTPUT:
            out_filename += '.gz'
        if isfile(out_filename) or isfile('%s.gz' % out_filename):
            GC.SELECTED['Logging'].writeln("Multiple sequence alignment exists. Skipping recomputation.")
        else:
            if ref_id is None:
                raise ValueError("Minimap2 requires a reference sequence")
            makedirs(minimap2_dir, exist_ok=True)
            seqs = GC.read_fasta(seqs_filename)
            ref_filename = '%s/ref.fas' % minimap2_dir
            seqs_filename = '%s/seqs.fas' % minimap2_dir
            index_filename = '%s/index.mmi' % minimap2_dir
            sam_filename = '%s/alignment.sam' % minimap2_dir
            found_ref_id = None; ref_seq = None
            f_ref = open(ref_filename, 'w')
            f_seqs = open(seqs_filename, 'w')
            for k in seqs:
                if k[0] == '>':
                    ID = k
                else:
                    ID = '>%s' % k
                if ref_id in ID:
                    if f_ref.closed:
                        raise ValueError("Reference ID was found in multiple sequence IDs: %s" % ref_id)
                    ref_seq = seqs[k]; found_ref_id = ID; f_ref.write(ID); f_ref.write('\n'); f_ref.write(ref_seq); f_ref.write('\n'); f_ref.close()
                else:
                    f_seqs.write(ID); f_seqs.write('\n'); f_seqs.write(seqs[k]); f_seqs.write('\n')
            f_seqs.close()
            if ref_seq is None:
                raise ValueError("Reference ID was not found: %s" % ref_id)
            f_stderr = open('%s/log.txt' % minimap2_dir, 'w')
            command = ['minimap2', '-a', '-d', index_filename, '-o', sam_filename]
            if GC.NUM_THREADS is not None:
                command += ['-t', str(GC.NUM_THREADS)]
            command += [ref_filename, seqs_filename]
            f = open('%s/command.txt' % minimap2_dir, 'w'); f.write('%s\n' % ' '.join(command)); f.close()
            call(command, stderr=f_stderr); f_stderr.close()
            out_lines = list()
            out_lines += [found_ref_id, ref_seq] # write ref to output alignment
            for line in open(sam_filename):
                if line[0] == '@':
                    continue
                parts = line.rstrip('\n').split('\t')
                flags = int(parts[1])
                if flags not in {0,16}:
                    continue
                ID = parts[0].strip()
                ref_ind = int(parts[3])-1
                cigar = parts[5].strip()
                seq = parts[9]
                edits = GC.parse_cigar(cigar)
                out_lines.append('>%s' % ID)
                out_seq = ''
                if ref_ind > 0:
                    out_seq = '-'*ref_ind # write gaps before alignment
                ind = 0; seq_len = ref_ind
                for e, e_len in edits:
                    if e in {'M','=','X'}: # (mis)match
                        out_seq += seq[ind:ind+e_len]; ind += e_len; seq_len += e_len
                    elif e == 'D':         # deletion (gap in query)
                        out_seq += '-'*e_len; seq_len += e_len
                    elif e == 'I':         # insertion (gap in reference)
                        ind += e_len
                    elif e in {'S','H'}:   # starting/ending segment of query not in reference (i.e., span of insertions)
                        ind += e_len
                if seq_len < len(ref_seq):
                    out_seq += '-'*(len(ref_seq)-seq_len) # write gaps after alignment
                out_lines.append(out_seq)
            GC.write_file('\n'.join(out_lines), out_filename)
        return out_filename
