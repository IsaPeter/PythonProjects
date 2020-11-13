#!/usr/bin/env python3
"""
Computer Info Module

This modul will query all the stored informations about the target
"""
import sys, os
runpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runpath,'..'))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
import lib.shm as shm


info = {'name':'target_info',
        'description':'Query gathered target information',
        'type':'post',
        'author':'Peter Isa'}

options = {'session':''}

module_session = None

def run(*args):
    global module_session
    from terminaltables import AsciiTable
    
    module_session = get_session()
    ci = get_computer_info()
    table_data =[]
    header = ['Name','Value']
    table_data.append(header)
    for n,v in ci.info.items():
        table_data.append([n,v])
    table = AsciiTable(table_data)
    print(table.table)

def get_session():
    global options
    name = options['session']
    for s in shm.sessions:
        if s.name == name:
            return s
    return None
def get_computer_info():
    global module_session
    ci = shm.get_computer(module_session.name)
    return ci
