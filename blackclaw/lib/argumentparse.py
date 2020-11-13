#!/usr/bin/env python3
"""
Argument Parser Modul

Parse arguments from get in CLI
"""
import os, sys
# Get the file current run path
runpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runpath,'..'))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
import re

class ArgumentParser:
    def __init__(self):
        self.args= []
        self.pattern = r':[a-z]+|--[a-z\-]+|-[a-z] [a-zA-Z0-9]+'
    def parse_command(self,cmd):
        matches = re.findall(self.pattern,cmd,re.I)
        for m in matches:
            if m.startswith(':'):
                #self.args.append(['name',m])
                pass
            elif m.startswith('--'):
                self.args.append([m,''])
            elif m.startswith('-'):
                p = m.split(' ',1)
                if len(p) == 1:
                    self.args.append([p,''])
                elif len(p) > 1:
                    self.args.append([p[0],p[1]])
                                     
                                     

parser = ArgumentParser()
parser.parse_command(':sysinfo --os -k 10 -k dfg')
print(parser.args)