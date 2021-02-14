#!/usr/bin/env python3
import re
import os,sys
# append base path to sys.path
runpath = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
sys.path.append(os.path.join(runpath,'..'))
sys.path.append(approot)
from lib.helpmenu import HelpMenu

class commandParser():
    def __init__(self,command,delimeter=' '):
        self.command = command
        self.delimeter = delimeter
        self.args = {}
        self.items = []
    def add_argument(self,*args,name='',help='',action='',hasvalue=True):
        ca = commandArg()
        ca.args = [a for a in args]
        ca.help = help
        ca.name = name
        ca.hasvalue = hasvalue
        if action: ca.action = action
             
        self.items.append(ca)
            
    def parse(self,command=''):
        if command != "":
            self.command = command
        
        if len(self.items) > 0:
            for i in self.items:
                for j in i.args:
                    if i.hasvalue:
                        pattern = f'{j} ([^\s]+)'
                        m = re.search(pattern,self.command)
                        if m:
                            i.value = m.group(1)
                            self.args.update({i.name:i.value})
                    else:
                        pattern = f' {j}'
                        m = re.search(pattern,self.command)
                        if m:
                            if i.action:
                                if i.action == 'store_true':
                                    i.value = True
                                elif i.action == 'store_false':
                                    i.value = False
                            else:
                                i.value = True
                            self.args.update({i.name:i.value})                        
            return self.args
            
    def get_value(self,name):
        if self.exists(name):
            for i in self.items:
                if i.name == name:
                    return i.value
        else:
            return None
        
    def exists(self,name):
        try:
            if self.args[name]:
                return True
            else:
                return False
        except:
            return False
    
    def print_help(self):
        h = HelpMenu()
        h.inner_heading_row_border = False
        h.title="Help for Usage"
        for i in self.items:
            h.add_item(i.get_arg_string(),i.help)


        h.print_help()        
    
    
class commandArg():
    def __init__(self):
        self.name = ""
        self.args = []
        self.value = ''
        self.help = ""
        self.action = None
        self.hasvalue = True
    def get_arg_string(self):
        result = ''
        for a in self.args:
            result += a+', '
        return result.rstrip(', ')
    
"""
c = commandParser('programname -l')
c.add_argument('-p','--password',name='password')
c.add_argument('-t',name='teszt')
c.add_argument('-l',name='lista',hasvalue=False)
c.parse()
print(c.exists('lista'))
"""
