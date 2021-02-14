#!/usr/bin/env python3
import os, sys



class directory():
    def __init__(self,path=''):
        self.directory_path = path
        self.topdironly = False
        self.extensions = []
    def get_files(self,path='.',extensions="*.*",topdironly=False):
        self.directory_path = path
        self.extensions = extensions.split(',')
        self.topdironly = topdironly
        if self.is_exists(path):
            result = []
            if self.topdironly:
                for i in os.listdir(path):
                    full_path = os.path.join(path,i)
                    if os.path.isfile(full_path):
                        result.append(full_path)
            else: 
                dirs = []
                for i in os.listdir(path):
                    full_path = os.path.join(path,i)
                    if os.path.isfile(full_path):
                        result.append(full_path)
                    else:
                        dirs.append(full_path)
                for d in dirs:
                    files = self.get_files(path=d,extensions="*.*",topdironly=False)
                    result.extend(files)
            return result
        else:
            return []
    def get_directories(self,path='.',topdironly=False):
        self.directory_path = path
        self.topdironly = topdironly
        if self.is_exists(path):
            result = []
            if self.topdironly:
                for i in os.listdir(path):
                    full_path = os.path.join(path,i)
                    if os.path.isdir(full_path):
                        result.append(full_path)
            else: 
                subdirs = []
                for i in os.listdir(path):
                    full_path = os.path.join(path,i)
                    if os.path.isdir(full_path):
                        result.append(full_path)
                        subdirs.append(full_path)
                for d in subdirs:
                    files = self.get_directories(path=d,topdironly=False)
                    result.extend(files)
            return result
        else:
            return []
    def is_exists(self,path):
        return os.path.exists(path)
    
    def get_parent(self,path='.'):
        self.directory_path = path
        return os.path.abspath(os.path.join(self.directory_path, os.pardir))
        
    
    
    
    
path = '/home/venom/Data/dev/python/PythonProjects/phoenix/lib'
libpar = directory().get_parent(path)
d = directory().get_files(path,topdironly=True)
for a in d:
    a = a.replace(libpar,'').lstrip('/').replace('/','.')
    print(a)