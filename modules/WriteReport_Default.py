#! /usr/bin/env python3
'''
Default implementation of the "WriteReport" module
'''
from WriteReport import WriteReport
import ViReport_GlobalContext as GC
from numpy import mean,std
from os import makedirs
from treeswift import read_tree_newick

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
        bullets = GC.SELECTED['ReportFormat'].bullets

        # Input Dataset
        ## make input sequence lengths figure
        seq_lengths = GC.seq_lengths_fasta(GC.INPUT_SEQS)
        seq_lengths_hist_filename = '%s/input_sequence_lengths.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_histogram(seq_lengths, seq_lengths_hist_filename, hist=True, kde=False, title="Input Sequence Lengths", xlabel="Sequence Length", ylabel="Count")

        ## make input sample times figure
        dates_vireport = {u:GC.days_to_date(GC.date_to_days(v)) for u,v in GC.load_dates_ViReport(GC.INPUT_TIMES)}
        dates = sorted(dates_vireport[l[1:].strip()] for l in open(GC.INPUT_SEQS) if l.startswith('>'))
        if len(dates) % 2 == 0:
            med_date = GC.days_to_date((GC.date_to_days(dates[int(len(dates)/2)]) + GC.date_to_days(dates[int(len(dates)/2)-1])) / 2)
        else:
            med_date = dates[int(len(dates)/2)]
        dates_hist_filename = '%s/input_sample_dates.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_barplot(dates, dates_hist_filename, rotate_labels=90, title="Input Sample Dates", xlabel="Sample Date", ylabel="Count")

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
            med_proc_date = GC.days_to_date((GC.date_to_days(proc_dates[int(len(proc_dates)/2)]) + GC.date_to_days(proc_dates[int(len(proc_dates)/2)-1])) / 2)
        else:
            med_proc_date = proc_dates[int(len(proc_dates)/2)]
        proc_dates_hist_filename = '%s/processed_sample_dates.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_barplot(proc_dates, proc_dates_hist_filename, rotate_labels=90, title="Processed Sample Dates", xlabel="Sample Date", ylabel="Count")

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
        msa_num_invariant = GC.num_invariant_sites(msa)
        msa_num_unique = len(set(msa.values()))
        dists_seq = [float(l.split(',')[2]) for l in open(GC.PAIRWISE_DISTS_SEQS) if not l.startswith('ID1')]
        dists_seq_hist_filename = '%s/pairwise_distances_sequences.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_histogram(dists_seq, dists_seq_hist_filename, hist=False, kde=True, title="Pairwise Sequence Distances", xlabel="Pairwise Distance", ylabel="Kernel Density Estimate")

        ## write section
        section("Multiple Sequence Alignment")
        write(GC.SELECTED['MultipleSequenceAlignment'].blurb())
        write("There were %d positions (%d invariant) and %d unique sequences in the multiple sequence alignment." % (msa_columns, msa_num_invariant, msa_num_unique))
        write(GC.SELECTED['PairwiseDistancesSequence'].blurb())
        write("The average pairwise sequence distance was %s," % GC.num_str(mean(dists_seq)))
        write("with a standard deviation of %s." % GC.num_str(std(dists_seq)))
        figure(dists_seq_hist_filename, width=0.75, caption="Distribution of pairwise sequence distances")

        # Phylogenetic Inference
        ## compute values of phylogeny
        tree_mut = read_tree_newick(GC.TREE_ROOTED); tree_mut.ladderize()
        tree_mut_viz_filename = '%s/tree_mutations.pdf' % GC.OUT_DIR_REPORTFIGS
        tree_mut.draw(show_labels=True, show_plot=False, export_filename=tree_mut_viz_filename, xlabel="Expected Number of Per-Site Mutations")
        dists_tree = [float(l.split(',')[2]) for l in open(GC.PAIRWISE_DISTS_TREE) if not l.startswith('ID1')]
        dists_tree_hist_filename = '%s/pairwise_distances_tree.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_histogram(dists_tree, dists_tree_hist_filename, hist=False, kde=True, title="Pairwise Phylogenetic Distances", xlabel="Pairwise Distance", ylabel="Kernel Density Estimate")

        ## write section
        section("Phylogenetic Inference")
        write(GC.SELECTED['PhylogeneticInference'].blurb())
        write(GC.SELECTED['Rooting'].blurb())
        write(GC.SELECTED['PairwiseDistancesTree'].blurb())
        write("The maximum pairwise phylogenetic distance (i.e., tree diameter) was %s," % GC.num_str(max(dists_tree)))
        write("and the average pairwise phylogenetic distance was %s," % GC.num_str(mean(dists_tree)))
        write("with a standard deviation of %s." % GC.num_str(std(dists_tree)))
        figure(tree_mut_viz_filename, width=1, height=1, caption="Rooted phylogenetic tree in unit of expected per-site mutations")
        figure(dists_tree_hist_filename, width=0.75, caption="Distribution of pairwise phylogenetic distances")

        # Phylogenetic Dating
        ## compute values of dated phylogeny
        tree_time = read_tree_newick(GC.TREE_DATED); tree_time.ladderize(); tree_time.root.edge_length = None
        tree_time_height = tree_time.height()
        tmrca_days = GC.date_to_days(max(proc_dates)) - tree_time_height
        tmrca_date = GC.days_to_date(tmrca_days)
        tree_time.scale_edges(1./365.)
        tree_time_viz_filename = '%s/tree_time.pdf' % GC.OUT_DIR_REPORTFIGS
        tmrca_year = int(tmrca_date.split('-')[0])
        tmrca_year_percent = tmrca_year + (tmrca_days - GC.date_to_days("%d-01-01" % tmrca_year))/365.
        tree_time.draw(show_labels=True, show_plot=False, export_filename=tree_time_viz_filename, xlabel="Year", start_time=tmrca_year_percent)

        ## write section
        section("Phylogenetic Dating")
        write(GC.SELECTED['Dating'].blurb())
        write("The height of the dated tree was %s days," % GC.num_str(tree_time_height))
        write("so given that the most recent sample was collected on %s," % proc_dates[-1])
        write("the estimated time of the most recent common ancestor (tMRCA) was %s." % tmrca_date)
        figure(tree_time_viz_filename, width=1, height=1, caption="Dated phylogenetic tree in unit of years")

        # Transmission Clustering
        ## compute values of transmission clustering
        clusters,singletons = GC.read_transmission_clusters(GC.TRANSMISSION_CLUSTERS)
        cluster_sizes = [len(clusters[k]) for k in clusters]
        cluster_sizes_hist_filename = '%s/cluster_sizes.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_histogram(cluster_sizes, cluster_sizes_hist_filename, hist=True, kde=False, title="Cluster Sizes", xlabel="Cluster Size", ylabel="Count")

        ## write section
        section("Transmission Clustering")
        write(GC.SELECTED['TransmissionClustering'].blurb())
        write("The total number of singletons (i.e., non-clustered individuals) was %d," % len(singletons))
        write("and the total number of clusters (excluding singletons) was %d." % len(clusters))
        write("The average cluster size (excluding singletons) was %s," % GC.num_str(mean(cluster_sizes)))
        write("with a standard deviation of %s," % GC.num_str(std(cluster_sizes)))
        write("and the maximum and minimum cluster sizes were %d and %d, respectively." % (max(cluster_sizes), min(cluster_sizes)))
        figure(cluster_sizes_hist_filename, width=0.75, caption="Distribution of cluster sizes (excluding singletons)")

        # Citations
        section("Citations")
        bullets(sorted(GC.CITATIONS))

        # finish up
        return close()
