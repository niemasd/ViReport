#! /usr/bin/env python3
'''
"Dating" module
'''
import abc

class Dating(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``Dating`` module

    Methods
    -------
    date(rooted_tree_filename, sample_times_filename)
        Date the rooted phylogeny in ``tree_filename`` using the sample times in ``sample_times_filename``
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
    def date(rooted_tree_filename, sample_times_filename):
        '''
        Date the rooted phylogeny in ``tree_filename`` using the sample times in ``sample_times_filename``

        Parameters
        ----------
        rooted_tree_filename : str
            Filename of the input rooted phylogeny (in the Newick format)
        sample_times_filename : str
            Filename of the input sample times (in the LSD format)

        Returns
        -------
        dated_tree_filename : str
            Filename of the output dated phylogeny (in the Newick format)
        '''
        pass
