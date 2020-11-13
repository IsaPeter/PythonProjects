#!/usr/bin/env python3
"""
Shared Memory Class 
"""
import sys, os
runpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runpath,'..'))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
from lib.computerinfo import ComputerInfo


sessions = []
modules = []
jobs = []
computers = []



def get_computer(name):
    for c in computers:
        if c.name == name:
            return c
    return None
def add_computer(name):
    ci = ComputerInfo(name)
    computers.append(ci)
def assign_computer_info(computer_name,variable,value):
    ci = get_computer(computer_name)
    if ci != None:
        ci.set_info(variable,value)
    else:
        print(f"[!] Cannot find ComputerInfo with name: {computer_name}! :(")
def delete_computer(name):
    c = get_computer(name)
    if c != None:
        computers.remove(c)
def add_session(clienthandler):
    try:
        sessions.append(clienthandler)
    except Exception as x:
        print(f"[x] {x}")

def delete_session(clienthandler):
    try:
        sessions.remove(clienthandler)
    except Exception as x:
        print(f"[x] {x}")
def get_session(name):
    for s in sessions:
        if s.name == name:
            return s
    return None
