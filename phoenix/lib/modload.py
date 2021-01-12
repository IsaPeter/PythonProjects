#!/usr/bin/env python3
"""
Module Loader Library

This module will load all the other modules and exploits.
"""
import os, sys
runpath = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
sys.path.append(os.path.join(runpath,'..'))
sys.path.append(approot)

import lib.phoenix_module as pm


class ModuleLoader():
    def __init__(self):
        self.modules = []
        self.listeners = []
    def load_modules(self,path):
        
        modules = self.__get_all_modules(path)
        for f in modules:
            self.__import_module(f)
        
    def __get_all_files(self,path):
        from glob import glob
        result = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.py'))]
        return result
    def __get_all_modules(self,path):
        mods = []
        files = self.__get_all_files(path)
        for f in files:
            fp = f.replace(path,'').replace('/','.').lstrip('.').replace('.py','')
            mods.append('modules.'+fp)
        return mods
    
    
    def __import_module(self,name):
        try:
            mod = __import__(name)
            components = name.split('.')
            for comp in components[1:]:
                mod = getattr(mod, comp)
            if mod.module_type:
                if mod.module_type == 'phoenix_module':
                    m = pm.phoenix_module(mod)
                    self.modules.append(m)
                    
        except Exception as x:
            print(f"[x] {x}")
        
    
    
    def get_modules(self):
        return self.modules


    


# The base_module is deprecated, use phoenix_module instead
class base_module():
    def __init__(self):
        self.name = ''
        self.description = ''
        self.module = None
        self.run_mod = True
        
    def set_module(self,mod):
        self.module = mod
        self.__get_name()
        self.__get_description()
           
    def __get_name(self):
        if self.module != None:
            self.name = self.module.info['name']
            
    def __get_description(self):
        if self.module != None:
            self.description = self.module.info['description']
            
    def run(self,*args):
        if self.module != None:
            try:
                self.module.run(*args)
            except Exception as x:
                print(f"[x] {x}")
    def use_module(self):
        self.run_mod = True
        while self.run_mod:
            command = input(f'black_claw({self.name})> ')
            self.command_interpreter(command)
    def command_interpreter(self,command):
        if command.lower() == 'options' or command.lower() == 'show options':
            self.show_module_options()
        if command.lower() == 'info':
            self.show_info()
        if command.startswith('set'):
            p = command.split(' ',2)
            variable = p[1]
            value = p[2]
            self.module.options[variable] = value
            print(f"Set {variable} => {value}")
        if command.startswith('unset'):
            p = command.split(' ',1)
            variable = p[1]
            self.module.options[variable] = ''
        if command.lower() == 'run':
            self.module.run()
        if command.lower() == 'bg':
            self.run_mod = False
            
    def show_info(self):
        if self.module != None:
            inf = self.module.info
            table_data = []
            header = ['Option Name','Value']
            table_data.append(header)
            for n, v in inf.items():
                table_data.append([n,v])
            table = AsciiTable(table_data)
            print(table.table)                
         
    def show_module_options(self):
        if self.module != None:
            opt = self.module.options
            table_data = []
            header = ['Option Name','Value']
            table_data.append(header)
            for n, v in opt.items():
                table_data.append([n,v])
            table = AsciiTable(table_data)
            print(table.table)            
            
            



    def terminate(self):
        try:
            self.module.terminate()
        except:
            pass
    def get_module_type(self):
        return self.module.info['type']
    def set_session_name(self,name):
        try:
            self.module.options['session'] = name
        except Exception as x:
            print(f"[x] {x}")
