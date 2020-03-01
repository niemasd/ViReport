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
        ## make sequence lengths figure
        seq_lengths = GC.seq_lengths_fasta(GC.INPUT_SEQS)
        seq_lengths_hist_filename = '%s/sequence_lengths.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_histogram(seq_lengths, seq_lengths_hist_filename, kde=False, title="Sequence Lengths", xlabel="Sequence Length", ylabel="Count")

        ## make sample times figure
        dates_vireport = {u:GC.days_to_date(GC.date_to_days(v)) for u,v in GC.load_dates_ViReport(GC.INPUT_TIMES)}
        dates = sorted(dates_vireport[l[1:].strip()] for l in open(GC.INPUT_SEQS) if l.startswith('>'))
        dates_hist_filename = '%s/sample_dates.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_barplot(dates, dates_hist_filename, title="Sample Dates", xlabel="Sample Date", ylabel="Count")

        ## write section
        section("Input Dataset")
        write("The analysis was conducted on a dataset containing %d sequences." % len(seq_lengths))
        write("The average sequence length was %s," % GC.num_str(mean(seq_lengths)))
        write("with a standard deviation of %s." % GC.num_str(std(seq_lengths)))
        figure(seq_lengths_hist_filename, caption="Distribution of input sequence lengths")
        write("The earliest sample date was %s," % dates[0])
        write("and the most recent sample date was %s." % dates[-1])
        figure(dates_hist_filename, caption="Distribution of sample dates")
        return close()
