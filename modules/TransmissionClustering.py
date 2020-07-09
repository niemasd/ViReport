#! /usr/bin/env python3
'''
"TransmissionClustering" module
'''
import abc

class TransmissionClustering(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``TransmissionClustering`` module

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
    infer_transmission_clusters()
        Infer transmission clusters using any data needed
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
    def infer_transmission_clusters():
        '''
        Infer transmission clusters using any data needed

        Returns
        -------
        transmission_clusters_filename : str
            Filename of the output transmission clusters (in the TreeCluster format)
        '''
        raise RuntimeError("Not implemented")
