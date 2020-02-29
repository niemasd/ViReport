#! /usr/bin/env python3
'''
"Preprocessing" module
'''
import abc

class Preprocessing(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``Preprocessing`` module

    Methods
    -------
    cite()
        Return citation string (or None)
    init()
        Initialize the module (if need be)
    finalize()
        Finalize the module (if need be)
    preprocess(seqs_filename, sample_times_filename)
        Preprocess the sequences in ``seqs_filename`` and/or the sample times in ``sample_times_filename`` (if need be)
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
    def preprocess(seqs_filename, sample_times_filename):
        '''
        Preprocess the sequences in ``seqs_filename`` and/or the sample times in ``sample_times_filename`` (if need be)

        Parameters
        ----------
        seqs_filename : str
            Filename of the raw input sequences to preprocess (in the FASTA format)
        sample_times_filename : str
            Filename of the sample times to preprocess

        Returns
        -------
        processed_seqs_filename : str
            Filename of the output processed sequences (in the FASTA format)
        processed_sample_times_filename : str
            Filename of the output processed sample times
        '''
        raise RuntimeError("Not implemented")
