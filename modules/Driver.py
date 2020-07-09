#! /usr/bin/env python3
'''
"Driver" module
'''
import abc

class Driver(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``Driver`` module

    Methods
    -------
    cite()
        Return citation string (or None)
    init()
        Initialize the module (if need be)
    run(seqs_filename, ref_id, sample_times_filename, outgroups_filename, categories_filename)
        Run the workflow
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
    def cite():
        '''
        Return the citation string (or None)
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def run(seqs_filename, ref_id, sample_times_filename, outgroups_filename, categories_filename):
        '''
        Run the workflow

        Parameters
        ----------
        seqs_filename : str
            Filename of the raw input sequences (in the FASTA format)
        ref_id : str
            ID of the reference genome (should be in ``seqs_filename``)
        sample_times_filename : str
            Filename of the sample times
        outgroups_filename : str
            Filename of the list of outgroups (or None)
        categories_filename : str
            Filename of the categories (or None)
        '''
        raise RuntimeError("Not implemented")
