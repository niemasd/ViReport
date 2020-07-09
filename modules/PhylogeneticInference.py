#! /usr/bin/env python3
'''
"PhylogeneticInference" module
'''
import abc

class PhylogeneticInference(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``PhylogeneticInference`` module

    Methods
    -------
    blurb()
        Return a string describing what was done
    cite()
        Return citation string (or None)
    infer_phylogeny(aln_filename)
        Infer a phylogeny from the alignment in ``aln_filename``
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
        desc : str
            A string describing what was done
        '''
        raise RuntimeError("Not implemented")

    @staticmethod
    @abc.abstractmethod
    def infer_phylogeny(aln_filename):
        '''
        Infer a phylogeny from the alignment in ``aln_filename``

        Parameters
        ----------
        aln_filename : str
            Filename of the multiple sequence alignment (in the FASTA format)

        Returns
        -------
        tree_filename : str
            Filename of the output phylogeny (in the Newick format)
        '''
        raise RuntimeError("Not implemented")
