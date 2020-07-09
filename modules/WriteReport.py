#! /usr/bin/env python3
'''
"WriteReport" module
'''
import abc

class WriteReport(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``WriteReport`` module

    Methods
    -------
    cite()
        Return citation string (or None)
    init()
        Initialize the module (if need be)
    finalize()
        Finalize the module (if need be)
    write_report()
        Write the report
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
    def write_report():
        '''
        Write the report

        Returns
        -------
        report_filename : str
            Filename of the report
        '''
        raise RuntimeError("Not implemented")
