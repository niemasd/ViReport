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
    bullets(items)
        Write a new bulleted list containing ``items``
    cite()
        Return citation string (or None)
    close()
        Finish writing the output file and close
    init()
        Initialize the module (if need be)
    figure(filename, caption, width, keep_aspect_ratio)
        Create a figure from the image in ``filename`` such that it is ``width`` proportion of the width and with caption ``caption``
    finalize()
        Finalize the module (if need be)
    section(s)
        New section ``s``
    subsection(s)
        New subsection ``s``
    subsubsection(s)
        New subsubsection ``s``
    write(s)
        Write string ``s`` to the output file 
    writeln(s)
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
    def section(s):
        '''
        New section ``s``

        Parameters:
        -----------
        s : str
            Section title
        '''
        raise RuntimeError("Not implemented")

    @staticmethod
    @abc.abstractmethod
    def subsection(s):
        '''
        New subsection ``s``

        Parameters:
        -----------
        s : str
            Subsection title
        '''
        raise RuntimeError("Not implemented")

    @staticmethod
    @abc.abstractmethod
    def subsubsection(s):
        '''
        New subsubsection ``s``

        Parameters:
        -----------
        s : str
            Subsubsection title
        '''
        raise RuntimeError("Not implemented")

    @staticmethod
    @abc.abstractmethod
    def write(s):
        '''
        Write string ``s`` to the output file

        Parameters
        ----------
        s : str
            String to write
        '''
        raise RuntimeError("Not implemented")

    @staticmethod
    @abc.abstractmethod
    def writeln(s):
        '''
        Write string ``s`` followed by a newline to the output file

        Parameters
        ----------
        s : str
            String to write
        '''
        raise RuntimeError("Not implemented")

    @staticmethod
    @abc.abstractmethod
    def bullets(items):
        '''
        Write a new bulleted list containing ``items``

        Parameters
        ----------
        items : list of (list of ...) str
            Items to write to list
        '''
        raise RuntimeError("Not implemented")

    @staticmethod
    @abc.abstractmethod
    def figure(filename, caption=None, width=None, height=None, keep_aspect_ratio=True):
        '''
        Create a figure from the image in ``filename`` such that it is ``width`` proportion of the width and with caption ``caption``

        Parameters:
        -----------
        filename : str
            The filename of the image for the figure
        caption : str
            The caption for the figure (or ``None`` for no caption)
        width : float
            The desired width (as a proportion of total width of page)
        height : float
            The desired height (as a proportion of total height of page)
        '''
        raise RuntimeError("Not implemented")

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
        raise RuntimeError("Not implemented")
