#!/usr/bin/env python3
import os, sys
runpath = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
sys.path.append(os.path.join(runpath,'..'))
sys.path.append(approot)
import lib.address_pool as ap
from lib.tabCompleter import tabCompleter
import readline

# Shared Variables
connected_clients = []
loaded_modules = []
addressPool = ap.addressPool() # create an adress pool
tab_complete = tabCompleter()

# Settings
readline.set_completer_delims('\t')
readline.parse_and_bind("tab: complete")   

