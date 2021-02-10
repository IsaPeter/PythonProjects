#!/usr/bin/env python3

module_name ="TCP Listener"
module_id = "listeners/tcp_listener"
module_description="Listening for incoming connections"
module_type = 'listener'
variables = {'lhost':'0.0.0.0',
             'lport':'9001',
             'type':'reverse_python'}


def run(arguments=''):
    pass
