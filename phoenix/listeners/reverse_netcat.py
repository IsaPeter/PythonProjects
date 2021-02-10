#!/usr/bin/env python3
import os


module_name ="Reverse Netcat listener"
module_description="Listening for incoming connections"
module_type = 'listener'
module_id = 'listener/reverse_netcat'
variables = {'lhost':'0.0.0.0',
             'lport':'9001',
             'type':'reverse_netcat'}

def run(arguments=''):
    global variables
    
    command = 'nc -lvnp '+str(variables['lport'])
    os.system(command)
    
    
