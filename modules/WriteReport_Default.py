#! /usr/bin/env python3
'''
Default implementation of the "WriteReport" module
'''
from WriteReport import WriteReport
import ViReport_GlobalContext as GC
from matplotlib.patches import Patch
from numpy import mean,quantile,std
from os import makedirs
from seaborn import color_palette
from subprocess import call
from treeswift import read_tree_newick
ZERO_THRESHOLD = 0.0000001

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
        GC.OUT_DIR_REPORTFILES = "%s/report_files" % GC.OUT_DIR
        makedirs(GC.OUT_DIR_REPORTFILES, exist_ok=True)
        GC.OUT_DIR_REPORTFIGS = '%s/figs' % GC.OUT_DIR_REPORTFILES
        makedirs(GC.OUT_DIR_REPORTFIGS, exist_ok=True)

        ## make input sequence lengths figure
        seq_lengths = GC.seq_lengths_fasta(GC.INPUT_SEQS)
        seq_lengths_hist_filename = '%s/input_sequence_lengths.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_histogram(seq_lengths, seq_lengths_hist_filename, hist=True, kde=False, title="Input Sequence Lengths", xlabel="Sequence Length", ylabel="Count")

        ## make input sample times figure
        dates_vireport = {u:GC.days_to_date(GC.date_to_days(v)) for u,v in GC.load_dates_ViReport(GC.INPUT_TIMES)}
        if GC.INPUT_OUTGROUPS is not None:
            for l in GC.read_file(GC.INPUT_OUTGROUPS):
                if l.strip() in dates_vireport:
                    del dates_vireport[l.strip()]
        dates = sorted(dates_vireport[l[1:].strip()] for l in GC.read_file(GC.INPUT_SEQS) if l.startswith('>') and l[1:].strip() in dates_vireport)
        if len(dates) % 2 == 0:
            med_date = GC.days_to_date((GC.date_to_days(dates[int(len(dates)/2)]) + GC.date_to_days(dates[int(len(dates)/2)-1])) / 2)
        else:
            med_date = dates[int(len(dates)/2)]
        all_dates = [GC.days_to_date(i) for i in range(GC.date_to_days(dates[0]), GC.date_to_days(dates[-1])+1)]
        dates_hist_filename = '%s/input_sample_dates.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_barplot(dates, dates_hist_filename, all_labels=all_dates, rotate_labels=90, title="Input Sample Dates", xlabel="Sample Date", ylabel="Count")

        ## make input categories figure
        if GC.INPUT_CATEGORIES is not None:
            id_to_cat = {l.split('\t')[0].strip() : l.split('\t')[1].strip() for l in GC.read_file(GC.INPUT_CATEGORIES)}
            sample_cats = sorted(id_to_cat[l[1:].strip()] for l in GC.read_file(GC.INPUT_SEQS) if l.startswith('>') and l[1:].strip() in id_to_cat)
            cats_hist_filename = '%s/input_categories.pdf' % GC.OUT_DIR_REPORTFIGS
            GC.create_barplot(sample_cats, cats_hist_filename, horizontal=True, title="Input Sample Categories", ylabel="Category", xlabel="Count")

        ## write section
        section("Input Dataset")
        write("The analysis was conducted on a dataset containing %d sequences." % len(seq_lengths))
        write(" The average sequence length was %s," % GC.num_str(mean(seq_lengths)))
        write(" with a standard deviation of %s." % GC.num_str(std(seq_lengths)))
        write(" The earliest sample date was %s," % dates[0])
        write(" the median sample date was %s," % med_date)
        write(" and the most recent sample date was %s." % dates[-1])
        figure(seq_lengths_hist_filename, width=0.75, caption="Distribution of input sequence lengths")
        figure(dates_hist_filename, width=0.75, caption="Distribution of input sample dates")
        if GC.INPUT_CATEGORIES is not None:
            figure(cats_hist_filename, width=0.75, caption="Distribution of input sample categories")

        ## make processed sequence lengths figure
        proc_seq_lengths = GC.seq_lengths_fasta(GC.PROCESSED_SEQS)
        proc_seq_lengths_hist_filename = '%s/processed_sequence_lengths.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_histogram(proc_seq_lengths, proc_seq_lengths_hist_filename, hist=True, kde=False, title="Processed Sequence Lengths", xlabel="Sequence Length", ylabel="Count")

        ## make processed sample times figure
        proc_dates_vireport = {u:GC.days_to_date(GC.date_to_days(v)) for u,v in GC.load_dates_ViReport(GC.PROCESSED_TIMES)}
        if GC.PROCESSED_OUTGROUPS is not None:
            for l in GC.read_file(GC.PROCESSED_OUTGROUPS):
                if l.strip() in proc_dates_vireport:
                    del proc_dates_vireport[l.strip()]
        proc_dates = sorted(proc_dates_vireport[l[1:].strip()] for l in GC.read_file(GC.PROCESSED_SEQS) if l.startswith('>') and l[1:].strip() in proc_dates_vireport)
        if len(proc_dates) % 2 == 0:
            med_proc_date = GC.days_to_date((GC.date_to_days(proc_dates[int(len(proc_dates)/2)]) + GC.date_to_days(proc_dates[int(len(proc_dates)/2)-1])) / 2)
        else:
            med_proc_date = proc_dates[int(len(proc_dates)/2)]
        all_proc_dates = [GC.days_to_date(i) for i in range(GC.date_to_days(proc_dates[0]), GC.date_to_days(proc_dates[-1])+1)]
        proc_dates_hist_filename = '%s/processed_sample_dates.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_barplot(proc_dates, proc_dates_hist_filename, all_labels=all_proc_dates, rotate_labels=90, title="Processed Sample Dates", xlabel="Sample Date", ylabel="Count")

        ## make processed categories figure
        if GC.PROCESSED_CATEGORIES is None:
            proc_id_to_cat = dict()
        else:
            proc_id_to_cat = {l.split('\t')[0].strip() : l.split('\t')[1].strip() for l in GC.read_file(GC.PROCESSED_CATEGORIES)}
            proc_sample_cats = sorted(proc_id_to_cat[l[1:].strip()] for l in GC.read_file(GC.PROCESSED_SEQS) if l.startswith('>') and l[1:].strip() in proc_id_to_cat)
            proc_cats_hist_filename = '%s/processed_input_categories.pdf' % GC.OUT_DIR_REPORTFIGS
            GC.create_barplot(proc_sample_cats, proc_cats_hist_filename, horizontal=True, title="Processed Sample Categories", ylabel="Category", xlabel="Count")

        ## write section
        section("Preprocessed Dataset")
        write(GC.SELECTED['Preprocessing'].blurb())
        write(" After preprocessing, the dataset contained %d sequences." % len(proc_seq_lengths))
        write(" The average sequence length was %s," % GC.num_str(mean(proc_seq_lengths)))
        write(" with a standard deviation of %s." % GC.num_str(std(proc_seq_lengths)))
        write(" The earliest sample date was %s," % proc_dates[0])
        write(" the median sample date was %s," % med_proc_date)
        write(" and the most recent sample date was %s." % proc_dates[-1])
        figure(proc_seq_lengths_hist_filename, width=0.75, caption="Distribution of preprocessed sequence lengths")
        figure(proc_dates_hist_filename, width=0.75, caption="Distribution of preprocessed sample dates")
        if GC.PROCESSED_CATEGORIES is not None:
            figure(proc_cats_hist_filename, width=0.75, caption="Distribution of preprocessed sample categories")

        # Multiple Sequence Alignment
        ## compute values of MSA
        msa = GC.read_fasta(GC.ALIGNMENT)
        msa_columns = len(msa[list(msa.keys())[0]])
        msa_num_invariant = GC.num_invariant_sites(msa)
        msa_num_unique = len(set(msa.values()))

        ## make pairwise distances figure
        if GC.PAIRWISE_DISTS_SEQS is not None:
            dists_seq = [float(l.split(',')[2]) for l in GC.read_file(GC.PAIRWISE_DISTS_SEQS) if not l.startswith('ID1')]
            dists_seq_hist_filename = '%s/pairwise_distances_sequences.pdf' % GC.OUT_DIR_REPORTFIGS
            GC.create_histogram(dists_seq, dists_seq_hist_filename, hist=False, kde=True, title="Pairwise Sequence Distances", xlabel="Pairwise Distance", ylabel="Kernel Density Estimate")

        ## make Manhattan plot of Shannon entropy
        msa_position_entropies = GC.msa_shannon_entropy(msa)
        msa_position_entropies_filename = '%s/%s.entropies.txt' % (GC.OUT_DIR_OUTFILES, '.'.join(GC.ALIGNMENT.split('/')[-1].split('.')[:-1]))
        out = open(msa_position_entropies_filename, 'w')
        for v in msa_position_entropies:
            if abs(v) < ZERO_THRESHOLD:
                out.write('0\n')
            else:
                out.write(str(v)); out.write('\n')
        out.close()
        if GC.GZIP_OUTPUT:
            call(GC.PIGZ_COMMAND + [msa_position_entropies_filename])
            msa_position_entropies_filename += '.gz'
        msa_position_entropies_q1 = quantile(msa_position_entropies, 0.25)
        msa_position_entropies_q3 = quantile(msa_position_entropies, 0.75)
        msa_entropy_manhattan_ythresh = msa_position_entropies_q3 + 1.5*(msa_position_entropies_q3-msa_position_entropies_q1)
        if abs(msa_entropy_manhattan_ythresh) < ZERO_THRESHOLD:
            msa_entropy_manhattan_ythresh = min(y for y in msa_position_entropies if y != 0)/2
            msa_entropy_manhattan_ythresh_blurb = "Due to the abundance of zero-entropy positions, all non-zero entropies were deemed significant."
        else:
            msa_entropy_manhattan_ythresh_blurb = "A significance threshold was computed using Tukey's Rule: 1.5x the interquartile range added to the third quartile, which was %s." % GC.num_str(msa_entropy_manhattan_ythresh)
        msa_entropy_manhattan_filename = '%s/alignment_entropies.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_manhattan(msa_position_entropies, msa_entropy_manhattan_filename, sig_thresh=msa_entropy_manhattan_ythresh, dot_size=8, title="Alignment Position Entropies", xlabel="Position of Multiple Sequence Alignment", ylabel="Shannon Entropy")

        ## make Manhattan plot of coverage
        msa_position_coverage = GC.msa_coverage(msa)
        msa_position_coverage_filename = '%s/%s.coverage.txt' % (GC.OUT_DIR_OUTFILES, '.'.join(GC.ALIGNMENT.split('/')[-1].split('.')[:-1]))
        out = open(msa_position_coverage_filename, 'w')
        for v in msa_position_coverage:
            if abs(v) < ZERO_THRESHOLD:
                out.write('0\n')
            else:
                out.write(str(v)); out.write('\n')
        out.close()
        if GC.GZIP_OUTPUT:
            call(GC.PIGZ_COMMAND + [msa_position_coverage_filename])
            msa_position_coverage_filename += '.gz'
        msa_coverage_manhattan_filename = '%s/alignment_coverage.pdf' % GC.OUT_DIR_REPORTFIGS
        GC.create_manhattan(msa_position_coverage, msa_coverage_manhattan_filename, dot_size=8, title="Alignment Position Coverage", xlabel="Position of Multiple Sequence Alignment", ylabel="Proportion Non-Gap")

        ## write section
        section("Multiple Sequence Alignment")
        write(GC.SELECTED['MultipleSequenceAlignment'].blurb())
        write(" There were %d positions (%d invariant) and %d unique sequences in the multiple sequence alignment. " % (msa_columns, msa_num_invariant, msa_num_unique))
        if GC.PAIRWISE_DISTS_SEQS is not None:
            write(GC.SELECTED['PairwiseDistancesSequence'].blurb())
            write(" The average pairwise sequence distance was %s," % GC.num_str(mean(dists_seq)))
            write(" with a standard deviation of %s." % GC.num_str(std(dists_seq)))
            figure(dists_seq_hist_filename, width=0.75, caption="Distribution of pairwise sequence distances")
        write("Across the positions of the multiple sequence alignment,")
        write(" the minimum coverage was %s," % GC.num_str(min(v for v in msa_position_coverage)))
        write(" the maximum coverage was %s," % GC.num_str(max(v for v in msa_position_coverage)))
        write(" and the average coverage was %s," % GC.num_str(mean(msa_position_coverage)))
        write(" with a standard deviation of %s." % GC.num_str(std(msa_position_coverage)))
        figure(msa_coverage_manhattan_filename, width=0.75, caption="Coverage (proportion of non-gap characters) across the positions of the multiple sequence alignment")
        write(" Across the positions of the multiple sequence alignment that had non-zero Shannon entropy,")
        write(" the minimum Shannon entropy was %s," % GC.num_str(min(v for v in msa_position_entropies if abs(v) > ZERO_THRESHOLD)))
        write(" the maximum Shannon entropy was %s," % GC.num_str(max(v for v in msa_position_entropies if abs(v) > ZERO_THRESHOLD)))
        write(" and the average Shannon entropy was %s," % GC.num_str(mean([v for v in msa_position_entropies if abs(v) > ZERO_THRESHOLD])))
        write(" with a standard deviation of %s." % GC.num_str(std([v for v in msa_position_entropies if abs(v) > ZERO_THRESHOLD])))
        figure(msa_entropy_manhattan_filename, width=0.75, caption="Shannon entropy across the positions of the multiple sequence alignment. %s The significance threshold is shown as a red dashed line, and significant points are shown in red." % msa_entropy_manhattan_ythresh_blurb)

        # Phylogenetic Inference
        ## compute values of phylogeny
        tree_mut = read_tree_newick(GC.TREE_ROOTED); tree_mut.ladderize()
        count_cats_mut = dict()
        for node in tree_mut.traverse_leaves():
            if node.label in proc_id_to_cat:
                cat = proc_id_to_cat[node.label]
                if cat not in count_cats_mut:
                    count_cats_mut[cat] = 0
                count_cats_mut[cat] += 1
        colors_mut = list(color_palette("colorblind", n_colors=len(count_cats_mut)))
        pal_mut = {k:colors_mut[i] for i,k in enumerate(sorted(count_cats_mut.keys()))}
        handles_mut = [Patch(color=pal_mut[k], label='%s (%d)' % (k, count_cats_mut[k])) for k in sorted(count_cats_mut.keys())]
        for node in tree_mut.traverse_leaves():
            if node.label in proc_id_to_cat:
                node.color = pal_mut[proc_id_to_cat[node.label]]
        GC.color_internal(tree_mut)
        tree_mut_viz_filename = '%s/tree_mutations.pdf' % GC.OUT_DIR_REPORTFIGS
        try:
            tree_mut.draw(show_labels=True, handles=handles_mut, show_plot=False, export_filename=tree_mut_viz_filename, xlabel="Expected Number of Per-Site Mutations")
        except:
            tree_mut_viz_filename = None
        if GC.PAIRWISE_DISTS_TREE is not None:
            dists_tree = [float(l.split(',')[2]) for l in GC.read_file(GC.PAIRWISE_DISTS_TREE) if not l.startswith('ID1')]
            dists_tree_hist_filename = '%s/pairwise_distances_tree.pdf' % GC.OUT_DIR_REPORTFIGS
            GC.create_histogram(dists_tree, dists_tree_hist_filename, hist=False, kde=True, title="Pairwise Phylogenetic Distances", xlabel="Pairwise Distance", ylabel="Kernel Density Estimate")

        ## write section
        section("Phylogenetic Inference")
        write(GC.SELECTED['PhylogeneticInference'].blurb())
        write(' '); write(GC.SELECTED['Rooting'].blurb())
        if tree_mut_viz_filename is None:
            write(" The tree was too large to draw.")
        else:
            figure(tree_mut_viz_filename, width=1, height=1, caption="Rooted phylogenetic tree in unit of expected per-site mutations")
        if GC.PAIRWISE_DISTS_TREE is not None:
            write(GC.SELECTED['PairwiseDistancesTree'].blurb())
            write(" The maximum pairwise phylogenetic distance (i.e., tree diameter) was %s," % GC.num_str(max(dists_tree)))
            write(" and the average pairwise phylogenetic distance was %s," % GC.num_str(mean(dists_tree)))
            write(" with a standard deviation of %s." % GC.num_str(std(dists_tree)))
            figure(dists_tree_hist_filename, width=0.75, caption="Distribution of pairwise phylogenetic distances")

        # Phylogenetic Dating
        ## compute values of dated phylogeny
        tree_time = read_tree_newick(GC.TREE_DATED); tree_time.ladderize(); tree_time.root.edge_length = None
        count_cats_time = dict()
        for node in tree_time.traverse_leaves():
            if node.label in proc_id_to_cat:
                cat = proc_id_to_cat[node.label]
                if cat not in count_cats_time:
                    count_cats_time[cat] = 0
                count_cats_time[cat] += 1
        colors_time = list(color_palette("colorblind", n_colors=len(count_cats_time)))
        pal_time = {k:colors_time[i] for i,k in enumerate(sorted(count_cats_time.keys()))}
        handles_time = [Patch(color=pal_time[k], label='%s (%d)' % (k, count_cats_time[k])) for k in sorted(count_cats_time.keys())]
        for node in tree_time.traverse_leaves():
            if node.label in proc_id_to_cat:
                node.color = pal_time[proc_id_to_cat[node.label]]
        GC.color_internal(tree_time)
        tree_time_height = tree_time.height()
        tmrca_days = GC.date_to_days(max(proc_dates)) - tree_time_height
        tmrca_date = GC.days_to_date(tmrca_days)
        tree_time.scale_edges(1./365.)
        tree_time_viz_filename = '%s/tree_time.pdf' % GC.OUT_DIR_REPORTFIGS
        tmrca_year = int(tmrca_date.split('-')[0])
        tmrca_year_percent = tmrca_year + (tmrca_days - GC.date_to_days("%d-01-01" % tmrca_year))/365.
        try:
            tree_time.draw(show_labels=True, handles=handles_time, show_plot=False, export_filename=tree_time_viz_filename, xlabel="Year", start_time=tmrca_year_percent)
        except:
            tree_time_viz_filename = None

        ## write section
        section("Phylogenetic Dating")
        write(GC.SELECTED['Dating'].blurb())
        write(" The height of the dated tree was %s days," % GC.num_str(tree_time_height))
        write(" so given that the most recent sample was collected on %s," % proc_dates[-1])
        write(" the estimated time of the most recent common ancestor (tMRCA) was %s." % tmrca_date)
        if tree_time_viz_filename is None:
            write(" The tree was too large to draw.")
        else:
            figure(tree_time_viz_filename, width=1, height=1, caption="Dated phylogenetic tree in unit of years")

        # Ancestral Sequence Reconstruction
        if GC.ANCESTRAL_SEQS is not None:
            section("Ancestral Sequence Reconstruction")
            write(GC.SELECTED['AncestralSequenceReconstruction'].blurb())

        # Transmission Clustering
        if GC.TRANSMISSION_CLUSTERS is not None:
            ## compute values of transmission clustering
            clusters,singletons = GC.read_transmission_clusters(GC.TRANSMISSION_CLUSTERS)
            cluster_sizes = [len(clusters[k]) for k in clusters]
            cluster_sizes_hist_filename = '%s/cluster_sizes.pdf' % GC.OUT_DIR_REPORTFIGS
            GC.create_histogram(cluster_sizes, cluster_sizes_hist_filename, hist=True, kde=False, title="Cluster Sizes", xlabel="Cluster Size", ylabel="Count")

            ## write section
            section("Transmission Clustering")
            write(GC.SELECTED['TransmissionClustering'].blurb())
            write(" The total number of singletons (i.e., non-clustered individuals) was %d," % len(singletons))
            write(" and the total number of clusters (excluding singletons) was %d." % len(clusters))
            write(" The average cluster size (excluding singletons) was %s," % GC.num_str(mean(cluster_sizes)))
            write(" with a standard deviation of %s," % GC.num_str(std(cluster_sizes)))
            write(" and the maximum and minimum cluster sizes were %d and %d, respectively." % (max(cluster_sizes), min(cluster_sizes)))
            figure(cluster_sizes_hist_filename, width=0.75, caption="Distribution of cluster sizes (excluding singletons)")

        # Citations
        section("Citations")
        bullets(sorted(GC.CITATIONS))

        # finish up
        return close()
