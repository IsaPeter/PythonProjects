#!/usr/bin/env python3
"""
The System Info Gathering Module

This module will gather information about the system
"""
# import modules
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import lib.shm as shm
from lib.argumentparse import ArgumentParser


info = {'name':'sysinfo',
        'description':'system information gathering',
        'type':'post',
        'author':'Peter Isa'}

options = {'session':''}
module_session = None

def run(*args):
    global module_session
    
    
    parser = ArgumentParser()
    if len(args) > 0:
        parser.parse_command(args[0])
    
    # get the associated session by name
    module_session = get_session()
    
    try:
        if len(parser.args) == 0: 
            get_hostname()
            get_architecture()
            get_os()
            get_release()
            get_kernel_version()
            get_available_users()
        else:
            for a in parser.args:
                if a[0] == '--hostname':
                    get_hostname()
                if a[0] == '--arch':
                    get_architecture()
                if a[0] == '--os':
                    get_os()
                if a[0] == '--release':
                    get_release()
                if a[0] == '--kernel':
                    get_kernel_version()
                                                
                    
                
                
    except Exception as x:
        print(f"[x] {x}")
    
def get_session():
    global options
    name = options['session']
    for s in shm.sessions:
        if s.name == name:
            return s
    return None

def get_hostname():
    global module_session
    hostname = module_session.get_command_result('hostname')
    print(f"Hostname: "+hostname)
    shm.assign_computer_info(module_session.name,'Hostname',hostname)
def get_architecture():
    global module_session
    arch = module_session.get_command_result('uname -m')
    print(f"Arch: "+arch)
    shm.assign_computer_info(module_session.name,'Architecture',arch)
def get_os():
    global module_session
    os = module_session.get_command_result('uname -a')
    print(f"OS: "+os)
    shm.assign_computer_info(module_session.name,'OS',os)
def get_release():
    global module_session
    release = module_session.get_command_result('cat /etc/os-release')
    print(release)
    shm.assign_computer_info(module_session.name,'Release',release)
def get_kernel_version():
    global module_session
    kernel = module_session.get_command_result('hostnamectl | grep Kernel')
    print(kernel.strip())
    shm.assign_computer_info(module_session.name,'Kernel',kernel.strip())

#ez azért kell, hogy majd csekkoljam, hogy az adott adat már benne van e az adatbázisban avagy nem.
def get_computer_info():
    global module_session
    ci = shm.get_computer(module_session.name)
    return ci
def get_available_users():
    global module_session
    # Get available users with interactive shell
    payload = "cat /etc/passwd | grep -E \"/bin/bash|/bin/sh\" | cut -d':' -f1"
    shell_users = module_session.get_command_result(payload)
    print(f"Shell Users: "+shell_users)
    shm.assign_computer_info(module_session.name,'Shell Users',shell_users)