#! /usr/bin/env python3
'''
"Logging" module
'''
import abc

class Logging(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``Logging`` module

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
    write(s)
        Write ``s`` to the log
    writeln(s)
        Write ``s`` followed by a newline character to the log
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
    def write(s):
        '''
        Write ``s`` to the log

        Parameters:
        -----------
        s : str
            The string to write
        '''
        raise RuntimeError("Not implemented")

    @staticmethod
    @abc.abstractmethod
    def writeln(s):
        '''
        Write ``s`` followed by a newline character to the log

        Parameters:
        -----------
        s : str
            The string to write
        '''
        raise RuntimeError("Not implemented")
