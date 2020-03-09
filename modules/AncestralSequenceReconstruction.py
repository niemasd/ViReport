#! /usr/bin/env python3
'''
"AncestralSequenceReconstruction" module
'''
import abc

class AncestralSequenceReconstruction(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``AncestralSequenceReconstruction`` module

    Methods
    -------
    blurb()
        Return a string describing what was done
    cite()
        Return citation string (or None)
    reconstruct(rooted_tree_filename, aln_filename)
        Reconstruct the ancestral sequence of ``rooted_tree_filename`` using the sequences in ``aln_filename``
    init()
        Initialize the module (if need be)
    finalize()
        Finalize the module (if need be)
    '''

    @staticmethod
    @abc.abstractmethod
    def init():
        '''
        Initialize the module (if need be)
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def finalize():
        '''
        Finalize the module (if need be)
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def cite():
        '''
        Return the citation string (or None)
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def blurb():
        '''
        Return a string describing what was done

        Returns
        -------
        A string describing what was done
        '''
        raise RuntimeError("Not implemented")

    @staticmethod
    @abc.abstractmethod
    def reconstruct(rooted_tree_filename, aln_filename):
        '''
        Reconstruct the ancestral sequence of ``rooted_tree_filename`` using the sequences in ``aln_filename``

        Parameters
        ----------
        rooted_tree_filename : str
            Filename of the input rooted phylogeny (in the Newick format)
        aln_filename : str
            Filename of the input multiple sequence alignment (in the FASTA format)

        Returns
        -------
        ancestral_seqs_filename : str
            Filename of the output ancestral sequence(s) (in the FASTA format)
        '''
        raise RuntimeError("Not implemented")
