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
    blurb()
        Return a string describing what was done
    cite()
        Return citation string (or None)
    date(rooted_tree_filename, sample_times_filename)
        Date the rooted phylogeny in ``rooted_tree_filename`` using the sample times in ``sample_times_filename``
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
    def date(rooted_tree_filename, sample_times_filename):
        '''
        Date the rooted phylogeny in ``rooted_tree_filename`` using the sample times in ``sample_times_filename``

        Parameters
        ----------
        rooted_tree_filename : str
            Filename of the input rooted phylogeny (in the Newick format)
        sample_times_filename : str
            Filename of the input sample times

        Returns
        -------
        dated_tree_filename : str
            Filename of the output dated phylogeny (in the Newick format)
        '''
        raise RuntimeError("Not implemented")
