#! /usr/bin/env python3
'''
"MultipleSequenceAlignment" module
'''
import abc

class MultipleSequenceAlignment(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``MultipleSequenceAlignment`` module

    Methods
    -------
    align(seqs_filename)
        Align the sequences in ``seqs_filename``
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
    def align(seqs_filename):
        '''
        Align the sequences in ``seqs_filename``

        Parameters
        ----------
        seqs_filename : str
            Filename of the raw sequences to align (in the FASTA format)

        Returns
        -------
        aln_filename : str
            Filename of the output multiple sequence alignment (in the FASTA format)
        '''
        raise RuntimeError("Not implemented")
