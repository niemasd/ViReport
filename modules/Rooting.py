#! /usr/bin/env python3
'''
"Rooting" module
'''
import abc

class Rooting(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``Rooting`` module

    Methods
    -------
    root(tree_filname)
        Root the phylogeny in ``tree_filename``
    cite()
        Return citation string (or None)
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
    def root(tree_filename):
        '''
        Root the phylogeny in ``tree_filename``

        Parameters
        ----------
        tree_filename : str
            Filename of the input unrooted phylogeny (in the Newick format)

        Returns
        -------
        rooted_tree_filename : str
            Filename of the output rooted phylogeny (in the Newick format)
        '''
        pass
