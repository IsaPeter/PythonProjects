#!/usr/bin/env python3
import os,sys
# append base path to sys.path
runpath = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
sys.path.append(os.path.join(runpath,'..'))
sys.path.append(approot)
import lib.tcp_server as ts
import lib.shm as shm
from lib.commandparser import commandParser

module_name ="TCP Listener"
module_id = "listener/tcp_listener"
module_description="Listening for incoming connections"
module_type = 'listener'
variables = {'lhost':'0.0.0.0',
             'lport':'9002',
             'type':'reverse_python',
             'verbose':'true'}
parser = None


def parse_args(args):
    global parser
    parser = commandParser(args)
    parser.add_argument('-p','--port',name='port',help="The port to listen on")
    parser.add_argument('-H','--host',name='host',help="The address to listen on")
    parser.add_argument('-h','--help',name='help',hasvalue=False,help="The module help")
    
    args = parser.parse()
    return args

def run(arguments=''):
    try:
        if arguments == '':
            lhost = variables['lhost']
            lport = int(variables['lport'])
        
            TS = ts.TCPServer(address=lhost,port=lport)
            TS.listen()
            client = TS.get_client()
            if client:
                shm.connected_clients.append(client)
        else:
            port = 9002
            host = '0.0.0.0'
            args = parse_args(arguments)
            if parser.exists('port'): port = int(args['port'])
            if parser.exists('host'): host = args['host']
            if parser.exists('help'):
                parser.print_help()
                return None
            TS = ts.TCPServer(address=host,port=port)
            TS.listen()
            client = TS.get_client()
            if client:
                shm.connected_clients.append(client)        
            
    except:
        pass