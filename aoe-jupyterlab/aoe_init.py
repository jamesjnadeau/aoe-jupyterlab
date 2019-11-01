# aoe_cwd.py
# This extension will change the working directory to the parent 'notebooks' folder

import os
import warnings

# don't show deprecation warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)

def load_ipython_extension(ipython):
    # this makes debugging easier
    def display(text):
        ipython.ev("display('%s')" % text)

    currentDirectory = ''
    cwd = ipython.ev("globals()['_dh'][0]")
    while currentDirectory != 'notebooks':
        cwd = os.path.normpath(os.path.join(cwd, '..'))
        currentDirectory = os.path.basename(cwd)
        display(currentDirectory)
    
    # use the ipython %cd magic to change directories
    ipython.magic("cd -q $cwd")
    ipython.magic("run init.ipynb")

# TODO: go back to notebook directory when unloading?
# def unload_ipython_extension(ipython):
    # If you want your extension to be unloadable, put that logic here.