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
    align(seqs_filename, ref_id)
        Align the sequences in ``seqs_filename``
    blurb()
        Return a string describing what was done
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
    def align(seqs_filename):
        '''
        Align the sequences in ``seqs_filename``

        Parameters
        ----------
        seqs_filename : str
            Filename of the raw sequences to align (in the FASTA format)
        ref_id : str
            ID of the reference genome (should be in ``seqs_filename``)

        Returns
        -------
        aln_filename : str
            Filename of the output multiple sequence alignment (in the FASTA format)
        '''
        raise RuntimeError("Not implemented")
