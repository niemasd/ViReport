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
    run()
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
    def run():
        '''
        Run the workflow
        '''
        pass
