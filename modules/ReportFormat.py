#! /usr/bin/env python3
'''
"ReportFormat" module
'''
import abc

class ReportFormat(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``ReportFormat`` module

    Methods
    -------
    cite()
        Return citation string (or None)
    close()
        Finish writing the output file and close
    init()
        Initialize the module (if need be)
    finalize()
        Finalize the module (if need be)
    write(s,type)
        Write string ``s`` to the output file 
    writeln(s,type)
        Write string ``s`` followed by a newline to the output file
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
    def write(s, text_type='normal'):
        '''
        Write string ``s`` to the output file

        Parameters
        ----------
        s : str
            String to write
        text_type : str
            Type of text (normal, header, subheader)
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def writeln(s, text_type='normal'):
        '''
        Write string ``s`` followed by a newline to the output file

        Parameters
        ----------
        s : str
            String to write
        text_type : str
            Type of text (normal, header, subheader)
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def close():
        '''
        Finish writing the output file and close

        Returns
        -------
        report_filename : str
            Filename of the report
        '''
        pass
