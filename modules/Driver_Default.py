#! /usr/bin/env python3
'''
Default implementation of the "Driver" module
'''
from Driver import Driver
import ViReport_GlobalContext as GC
from os import makedirs
from os.path import isfile
from subprocess import call
from time import time

def print_message():
    '''
    Print author message
    '''
    title = "ViReport v%s" % GC.VIREPORT_VERSION
    devel = "Niema Moshiri 2020"
    l = max(len(title),len(devel))
    LOG.writeln("/-%s-\\" % ('-'*l))
    for e in (title,devel):
        lpad = int((l-len(e))/2)
        rpad = l - lpad - len(e)
        LOG.writeln("| %s%s%s |" % (lpad*' ',e,rpad*' '))
    LOG.writeln("\\-%s-/\n" % ('-'*l))

class Driver_Default(Driver):
    def init():
        pass

    def cite():
        return GC.CITATION_VIREPORT

    def run(seqs_filename, ref_id, sample_times_filename, outgroups_filename, categories_filename):
        # set things up
        GC.VIREPORT_START_TIME = time()
        global LOG; LOG = GC.SELECTED['Logging']
        if GC.GZIP_OUTPUT:
            GC.PIGZ_COMMAND = ['pigz', '-9']
            if GC.NUM_THREADS is not None:
                GC.PIGZ_COMMAND += ['-p', str(GC.NUM_THREADS)]

        # organize citations
        GC.CITATIONS = set()
        for m in GC.SELECTED:
            cite = GC.SELECTED[m].cite()
            if isinstance(cite,str):
                GC.CITATIONS.add(cite.strip())
            elif isinstance(cite,set) or isinstance(cite,list):
                for c in cite:
                    GC.CITATIONS.add(c.strip())
        GC.CITATIONS = sorted(GC.CITATIONS)

        # print starting messages
        print_message()
        LOG.writeln("========================   Workflow Process   ========================")
        LOG.writeln("[%s] ViReport was run as follows: %s" % (GC.get_time(), GC.VIREPORT_COMMAND))
        LOG.writeln("[%s] Output directory: %s" % (GC.get_time(), GC.OUT_DIR_PRINT))
        LOG.writeln("[%s] Starting viral analysis workflow..." % GC.get_time())

        # check input files
        if not isfile(seqs_filename):
            raise ValueError("Invalid sequence file: %s" % seqs_filename)
        GC.INPUT_SEQS = seqs_filename
        GC.INPUT_REF_ID = ref_id
        if not isfile(sample_times_filename):
            raise ValueError("Invalid sample times file: %s" % sample_times_filename)
        GC.INPUT_TIMES = sample_times_filename
        if outgroups_filename is not None and not isfile(outgroups_filename):
            raise ValueError("Invalid outgroups list file: %s" % outgroups_filename)
        GC.INPUT_OUTGROUPS = outgroups_filename
        if categories_filename is not None and not isfile(categories_filename):
            raise ValueError("Invalid sample categories file: %s" % categories_filename)
        GC.INPUT_CATEGORIES = categories_filename

        # set up output and intermediate folders
        GC.OUT_DIR_OUTFILES = "%s/output_files" % GC.OUT_DIR
        makedirs(GC.OUT_DIR_OUTFILES, exist_ok=True)
        GC.OUT_DIR_TMPFILES = "%s/intermediate_files" % GC.OUT_DIR
        makedirs(GC.OUT_DIR_TMPFILES, exist_ok=True)

        # initialize module implementations
        LOG.writeln("\n[%s] Initializing module implementations..." % GC.get_time())
        for k in GC.SELECTED:
            GC.SELECTED[k].init()
        LOG.writeln("[%s] Finished initializing %d module implementations" % (GC.get_time(), len(GC.SELECTED)))

        # run preprocessing
        LOG.writeln("\n[%s] Running '%s'..." % (GC.get_time(), GC.SELECTED['Preprocessing'].__name__))
        GC.PROCESSED_SEQS, GC.PROCESSED_REF_ID, GC.PROCESSED_TIMES, GC.PROCESSED_OUTGROUPS, GC.PROCESSED_CATEGORIES = GC.SELECTED['Preprocessing'].preprocess(GC.INPUT_SEQS, GC.INPUT_REF_ID, GC.INPUT_TIMES, GC.INPUT_OUTGROUPS, GC.INPUT_CATEGORIES)
        if GC.GZIP_OUTPUT:
            LOG.writeln("[%s] Compressing preprocessed sequence(s)..." % GC.get_time())
            call(GC.PIGZ_COMMAND + [GC.PROCESSED_SEQS])
            GC.PROCESSED_SEQS += '.gz'
            LOG.writeln("[%s] Compressing preprocessed sample times..." % GC.get_time())
            call(GC.PIGZ_COMMAND + [GC.PROCESSED_TIMES])
            GC.PROCESSED_TIMES += '.gz'
            if GC.PROCESSED_OUTGROUPS is not None:
                LOG.writeln("[%s] Compressing preprocessed outgroups list..." % GC.get_time())
                call(GC.PIGZ_COMMAND + [GC.PROCESSED_OUTGROUPS])
                GC.PROCESSED_OUTGROUPS += '.gz'
            if GC.PROCESSED_CATEGORIES is not None:
                LOG.writeln("[%s] Compressing preprocessed sample categories..." % GC.get_time())
                call(GC.PIGZ_COMMAND + [GC.PROCESSED_CATEGORIES])
                GC.PROCESSED_CATEGORIES += '.gz'
        LOG.writeln("[%s] Preprocessed sequences output to: %s" % (GC.get_time(), GC.PROCESSED_SEQS))
        if GC.PROCESSED_REF_ID is not None:
            LOG.writeln("[%s] Preprocessed reference ID: %s" % (GC.get_time(), GC.PROCESSED_REF_ID))
        LOG.writeln("[%s] Preprocessed sample times output to: %s" % (GC.get_time(), GC.PROCESSED_TIMES))
        if GC.PROCESSED_OUTGROUPS is not None:
            LOG.writeln("[%s] Preprocessed outgroups list output to: %s" % (GC.get_time(), GC.PROCESSED_OUTGROUPS))
        if GC.PROCESSED_CATEGORIES is not None:
            LOG.writeln("[%s] Preprocessed sample categories output to: %s" % (GC.get_time(), GC.PROCESSED_CATEGORIES))

        # align the preprocessed sequences
        LOG.writeln("\n[%s] Running '%s'..." % (GC.get_time(), GC.SELECTED['MultipleSequenceAlignment'].__name__))
        GC.ALIGNMENT_WITH_OUTGROUP = GC.SELECTED['MultipleSequenceAlignment'].align(GC.PROCESSED_SEQS, GC.PROCESSED_REF_ID)
        GC.ALIGNMENT = GC.remove_outgroups_fasta(GC.ALIGNMENT_WITH_OUTGROUP, GC.PROCESSED_OUTGROUPS)
        if GC.GZIP_OUTPUT:
            LOG.writeln("[%s] Compressing multiple sequence alignment..." % GC.get_time())
            call(GC.PIGZ_COMMAND + [GC.ALIGNMENT_WITH_OUTGROUP, GC.ALIGNMENT])
            GC.ALIGNMENT_WITH_OUTGROUP += '.gz'
            GC.ALIGNMENT += '.gz'
        LOG.writeln("[%s] Multiple sequence alignment output to: %s" % (GC.get_time(), GC.ALIGNMENT))

        # compute pairwise sequence distances
        LOG.writeln("\n[%s] Running '%s'..." % (GC.get_time(), GC.SELECTED['PairwiseDistancesSequence'].__name__))
        GC.PAIRWISE_DISTS_SEQS = GC.SELECTED['PairwiseDistancesSequence'].pairwise_distances(GC.ALIGNMENT)
        if GC.PAIRWISE_DISTS_SEQS is not None:
            if GC.GZIP_OUTPUT:
                LOG.writeln("[%s] Compressing multiple sequence alignment..." % GC.get_time())
                call(GC.PIGZ_COMMAND + [GC.PAIRWISE_DISTS_SEQS])
                GC.PAIRWISE_DISTS_SEQS += '.gz'
            LOG.writeln("[%s] Pairwise sequence distances output to: %s" % (GC.get_time(), GC.PAIRWISE_DISTS_SEQS))

        # infer a phylogeny
        LOG.writeln("\n[%s] Running '%s'..." % (GC.get_time(), GC.SELECTED['PhylogeneticInference'].__name__))
        GC.TREE_UNROOTED_WITH_OUTGROUP = GC.SELECTED['PhylogeneticInference'].infer_phylogeny(GC.ALIGNMENT_WITH_OUTGROUP)
        GC.TREE_UNROOTED = GC.remove_outgroups_newick(GC.TREE_UNROOTED_WITH_OUTGROUP, GC.PROCESSED_OUTGROUPS)
        if GC.GZIP_OUTPUT:
            LOG.writeln("[%s] Compressing (unrooted) phylogeny..." % GC.get_time())
            call(GC.PIGZ_COMMAND + [GC.TREE_UNROOTED_WITH_OUTGROUP, GC.TREE_UNROOTED])
            GC.TREE_UNROOTED_WITH_OUTGROUP += '.gz'
            GC.TREE_UNROOTED += '.gz'
        LOG.writeln("[%s] Inferred (unrooted) phylogeny output to: %s" % (GC.get_time(), GC.TREE_UNROOTED))

        # compute pairwise phylogenetic distances
        LOG.writeln("\n[%s] Running '%s'..." % (GC.get_time(), GC.SELECTED['PairwiseDistancesTree'].__name__))
        GC.PAIRWISE_DISTS_TREE = GC.SELECTED['PairwiseDistancesTree'].pairwise_distances(GC.TREE_UNROOTED)
        if GC.PAIRWISE_DISTS_TREE is not None:
            if GC.GZIP_OUTPUT:
                LOG.writeln("[%s] Compressing pairwise phylogenetic distances..." % GC.get_time())
                call(GC.PIGZ_COMMAND + [GC.PAIRWISE_DISTS_TREE])
                GC.PAIRWISE_DISTS_TREE += '.gz'
            LOG.writeln("[%s] Pairwise phylogenetic distances output to: %s" % (GC.get_time(), GC.PAIRWISE_DISTS_TREE))

        # root the phylogeny
        LOG.writeln("\n[%s] Running '%s'..." % (GC.get_time(), GC.SELECTED['Rooting'].__name__))
        GC.TREE_ROOTED_WITH_OUTGROUP = GC.SELECTED['Rooting'].root(GC.TREE_UNROOTED_WITH_OUTGROUP)
        GC.TREE_ROOTED = GC.remove_outgroups_newick(GC.TREE_ROOTED_WITH_OUTGROUP, GC.PROCESSED_OUTGROUPS)
        if GC.GZIP_OUTPUT:
            LOG.writeln("[%s] Compressing rooted phylogeny..." % GC.get_time())
            call(GC.PIGZ_COMMAND + [GC.TREE_ROOTED_WITH_OUTGROUP, GC.TREE_ROOTED])
            GC.TREE_ROOTED_WITH_OUTGROUP += '.gz'
            GC.TREE_ROOTED += '.gz'
        LOG.writeln("[%s] Rooted phylogeny output to: %s" % (GC.get_time(), GC.TREE_ROOTED))

        # date the rooted phylogeny
        LOG.writeln("\n[%s] Running '%s'..." % (GC.get_time(), GC.SELECTED['Dating'].__name__))
        GC.TREE_DATED = GC.SELECTED['Dating'].date(GC.TREE_ROOTED, GC.PROCESSED_TIMES)
        if GC.GZIP_OUTPUT:
            LOG.writeln("[%s] Compressing dated phylogeny..." % GC.get_time())
            call(GC.PIGZ_COMMAND + [GC.TREE_DATED])
            GC.TREE_DATED += '.gz'
        LOG.writeln("[%s] Dated phylogeny output to: %s" % (GC.get_time(), GC.TREE_DATED))

        # infer ancestral sequence(s)
        LOG.writeln("\n[%s] Running '%s'..." % (GC.get_time(), GC.SELECTED['AncestralSequenceReconstruction'].__name__))
        GC.ANCESTRAL_SEQS = GC.SELECTED['AncestralSequenceReconstruction'].reconstruct(GC.TREE_ROOTED, GC.ALIGNMENT)
        if GC.ANCESTRAL_SEQS is not None:
            if GC.GZIP_OUTPUT:
                LOG.writeln("[%s] Compressing ancestral sequence(s)..." % GC.get_time())
                call(GC.PIGZ_COMMAND + [GC.ANCESTRAL_SEQS])
                GC.ANCESTRAL_SEQS += '.gz'
            LOG.writeln("[%s] Ancestral sequence(s) output to: %s" % (GC.get_time(), GC.ANCESTRAL_SEQS))

        # perform transmission clustering
        LOG.writeln("\n[%s] Running '%s'..." % (GC.get_time(), GC.SELECTED['TransmissionClustering'].__name__))
        GC.TRANSMISSION_CLUSTERS = GC.SELECTED['TransmissionClustering'].infer_transmission_clusters()
        if GC.TRANSMISSION_CLUSTERS is not None:
            if GC.GZIP_OUTPUT:
                LOG.writeln("[%s] Compressing transmission clusters..." % GC.get_time())
                call(GC.PIGZ_COMMAND + [GC.TRANSMISSION_CLUSTERS])
                GC.TRANSMISSION_CLUSTERS += '.gz'
            LOG.writeln("[%s] Transmission clusters output to: %s" % (GC.get_time(), GC.TRANSMISSION_CLUSTERS))

        # write the report
        LOG.writeln("\n[%s] Writing report using '%s'..." % (GC.get_time(), GC.SELECTED['WriteReport'].__name__))
        GC.REPORT = GC.SELECTED['WriteReport'].write_report()
        if GC.REPORT is not None:
            LOG.writeln("[%s] Report written to: %s" % (GC.get_time(), GC.REPORT))

        # print info about the run
        LOG.writeln("\n\n==========================   Information   ===========================")
        LOG.writeln("Output Size (bytes): %d" % GC.filesize(GC.OUT_DIR))
        LOG.writeln("Execution Time (seconds): %d" % (time()-GC.VIREPORT_START_TIME))

        # print citations
        LOG.writeln("\n\n===========================   Citations   ============================")
        for cite in GC.CITATIONS:
            LOG.writeln(cite)
