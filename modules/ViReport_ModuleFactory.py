#! /usr/bin/env python3
'''
Handle ViReport modules
'''
from glob import glob
from importlib import import_module
from os.path import abspath,expanduser
from sys import path

def init(mod_dir):
    '''
    Initialize ViReport modules

    Parameters
    ----------
    mod_dir : str
        The path to the modules directory
    '''

    # load list of modules
    py_files = {f for f in glob("%s/*.py" % mod_dir) if not f.split('/')[-1].startswith('ViReport')}
    global MODULES
    MODULES = {f.split('/')[-1].split('.')[0]:dict() for f in py_files if '_' not in f.split('/')[-1]}
    for f in py_files:
        module_name = f.split('/')[-1].split('.')[0]
        if not module_name.startswith('__') and '_' in module_name:
            pre,suf = module_name.split('_')
            MODULES[pre][suf] = getattr(import_module(module_name), module_name)
