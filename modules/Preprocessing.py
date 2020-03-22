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
    blurb()
        Return a string describing what was done
    cite()
        Return citation string (or None)
    init()
        Initialize the module (if need be)
    finalize()
        Finalize the module (if need be)
    preprocess(seqs_filename, ref_id, sample_times_filename, outgroups_filename, categories_filename)
        Preprocess the sequences in ``seqs_filename``, the reference ID ``ref_id``, the sample times in ``sample_times_filename``, the IDs in ``outgroups_filename`` (if need be), and/or the IDs/categories in ``categories_filename`` (if need be)
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
    def preprocess(seqs_filename, ref_id, sample_times_filename, outgroups_filename, categories_filename):
        '''
        Preprocess the sequences in ``seqs_filename``, the reference ID ``ref_id``, the sample times in ``sample_times_filename``, the IDs in ``outgroups_filename``, and/or the IDs/categories in ``categories_filename`` (if need be)

        Parameters
        ----------
        seqs_filename : str
            Filename of the raw input sequences to preprocess (in the FASTA format)
        ref_id : str
            ID of the reference genome (should be in ``seqs_filename``)
        sample_times_filename : str
            Filename of the sample times to preprocess
        outgroups_filename : str
            Filename of the outgroups list to preprocess
        categories_filename : str
            Filename of the sample categories to preprocess

        Returns
        -------
        processed_seqs_filename : str
            Filename of the output processed sequences (in the FASTA format)
        processed_sample_times_filename : str
            Filename of the output processed sample times
        processed_outgroups_filename : str
            Filename of the output processed outgroups list
        processed_categories_filename : str
            Filename of the output processed sample categories
        '''
        raise RuntimeError("Not implemented")
