#! /usr/bin/env python3
'''
"PairwiseDistancesSequence" module
'''
import abc

class PairwiseDistancesSequence(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``PairwiseDistancesSequence`` module

    Methods
    -------
    blurb()
        Return a string describing what was done
    cite()
        Return citation string (or None)
    init()
        Initialize the module (if need be)
    finalize()
        Finalize the module (if need be)
    pairwise_distances(aln_filename)
        Compute the pairwise distances between the sequences in ``aln_filename``
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
        desc : str
            A string describing what was done
        '''
        raise RuntimeError("Not implemented")

    @staticmethod
    @abc.abstractmethod
    def pairwise_distances(aln_filename):
        '''
        Compute the pairwise distances between the sequences in ``aln_filename``

        Parameters
        ----------
        aln_filename : str
            Filename of the multiple sequence alignment (in the FASTA format)

        Returns
        -------
        seq_dists_filename : str
            Filename of the output pairwise sequence distances (in the tn93 format)
        '''
        raise RuntimeError("Not implemented")
