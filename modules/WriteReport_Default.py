#! /usr/bin/env python3
'''
Default implementation of the "WriteReport" module
'''
from WriteReport import WriteReport
import ViReport_GlobalContext as GC
from numpy import mean,std
from os import makedirs

class WriteReport_Default(WriteReport):
    def init():
        pass

    def finalize():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def write_report():
        # set things up
        section = GC.SELECTED['ReportFormat'].section
        write = GC.SELECTED['ReportFormat'].write
        close = GC.SELECTED['ReportFormat'].close
        figure = GC.SELECTED['ReportFormat'].figure

        # Input Dataset
        ## make input sequence lengths figure
        seq_lengths = GC.seq_lengths_fasta(GC.INPUT_SEQS)
        seq_lengths_hist_filename = '%s/input_sequence_lengths.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_histogram(seq_lengths, seq_lengths_hist_filename, hist=True, kde=False, title="Input Sequence Lengths", xlabel="Sequence Length", ylabel="Count")

        ## make input sample times figure
        dates_vireport = {u:GC.days_to_date(GC.date_to_days(v)) for u,v in GC.load_dates_ViReport(GC.INPUT_TIMES)}
        dates = sorted(dates_vireport[l[1:].strip()] for l in open(GC.INPUT_SEQS) if l.startswith('>'))
        if len(dates) % 2 == 0:
            med_date = GC.days_to_date((GC.date_to_dates(dates[int(len(dates)/2)]) + GC.date_to_dates(dates[int(len(dates)/2)-1])) / 2)
        else:
            med_date = dates[int(len(dates)/2)]
        dates_hist_filename = '%s/input_sample_dates.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_barplot(dates, dates_hist_filename, title="Input Sample Dates", xlabel="Sample Date", ylabel="Count")

        ## write section
        section("Input Dataset")
        write("The analysis was conducted on a dataset containing %d sequences." % len(seq_lengths))
        write("The average sequence length was %s," % GC.num_str(mean(seq_lengths)))
        write("with a standard deviation of %s." % GC.num_str(std(seq_lengths)))
        write("The earliest sample date was %s," % dates[0])
        write("the median sample date was %s," % med_date)
        write("and the most recent sample date was %s." % dates[-1])
        figure(seq_lengths_hist_filename, width=0.75, caption="Distribution of input sequence lengths")
        figure(dates_hist_filename, width=0.75, caption="Distribution of input sample dates")

        # Preprocessing
        ## make processed sequence lengths figure
        proc_seq_lengths = GC.seq_lengths_fasta(GC.PROCESSED_SEQS)
        proc_seq_lengths_hist_filename = '%s/processed_sequence_lengths.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_histogram(proc_seq_lengths, proc_seq_lengths_hist_filename, hist=True, kde=False, title="Processed Sequence Lengths", xlabel="Sequence Length", ylabel="Count")

        ## make processed sample times figure
        proc_dates_vireport = {u:GC.days_to_date(GC.date_to_days(v)) for u,v in GC.load_dates_ViReport(GC.PROCESSED_TIMES)}
        proc_dates = sorted(proc_dates_vireport[l[1:].strip()] for l in open(GC.PROCESSED_SEQS) if l.startswith('>'))
        if len(proc_dates) % 2 == 0:
            med_proc_date = GC.days_to_date((GC.date_to_dates(proc_dates[int(len(proc_dates)/2)]) + GC.date_to_dates(proc_dates[int(len(proc_dates)/2)-1])) / 2)
        else:
            med_proc_date = proc_dates[int(len(proc_dates)/2)]
        proc_dates_hist_filename = '%s/processed_sample_dates.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_barplot(proc_dates, proc_dates_hist_filename, title="Processed Sample Dates", xlabel="Sample Date", ylabel="Count")

        ## write section
        section("Preprocessed Dataset")
        write(GC.SELECTED['Preprocessing'].blurb())
        write("After preprocessing, the dataset contained %d sequences." % len(proc_seq_lengths))
        write("The average sequence length was %s," % GC.num_str(mean(proc_seq_lengths)))
        write("with a standard deviation of %s." % GC.num_str(std(proc_seq_lengths)))
        write("The earliest sample date was %s," % proc_dates[0])
        write("the median sample date was %s," % med_proc_date)
        write("and the most recent sample date was %s." % proc_dates[-1])
        figure(proc_seq_lengths_hist_filename, width=0.75, caption="Distribution of preprocessed sequence lengths")
        figure(proc_dates_hist_filename, width=0.75, caption="Distribution of preprocessed sample dates")

        # Multiple Sequence Alignment
        ## compute values of MSA
        msa = GC.read_fasta(GC.ALIGNMENT)
        msa_columns = len(msa[list(msa.keys())[0]])
        msa_num_unique = len(set(msa.values()))
        dists_seq = [float(l.split(',')[2]) for l in open(GC.PAIRWISE_DISTS_SEQS) if not l.startswith('ID1')]
        dists_seq_hist_filename = '%s/pairwise_distances_sequences.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_histogram(dists_seq, dists_seq_hist_filename, hist=False, kde=True, title="Pairwise Sequence Distances", xlabel="Pairwise Distance", ylabel="Kernel Density Estimate")

        ## write section
        section("Multiple Sequence Alignment")
        write(GC.SELECTED['MultipleSequenceAlignment'].blurb())
        write("There were %d positions and %d unique sequences in the multiple sequence alignment." % (msa_columns, msa_num_unique))
        write(GC.SELECTED['PairwiseDistancesSequence'].blurb())
        write("The average pairwise sequence distance was %s," % GC.num_str(mean(dists_seq)))
        write("with a standard deviation of %s." % GC.num_str(std(dists_seq)))
        figure(dists_seq_hist_filename, width=0.75, caption="Distribution of pairwise sequence distances")

        # finish up
        return close()
