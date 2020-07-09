#! /usr/bin/env python3
'''
"PairwiseDistancesTree" module
'''
import abc

class PairwiseDistancesTree(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``PairwiseDistancesTree`` module

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
    pairwise_distances(tree_filename)
        Compute the pairwise distances between the leaves of ``tree_filename``
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
    def pairwise_distances(tree_filename):
        '''
        Compute the pairwise distances between the trees in ``tree_filename``

        Parameters
        ----------
        tree_filename : str
            Filename of the phylogenetic tree (in the Newick format)

        Returns
        -------
        tree_dists_filename : str
            Filename of the output pairwise phylogenetic distances (in the tn93 format)
        '''
        raise RuntimeError("Not implemented")
