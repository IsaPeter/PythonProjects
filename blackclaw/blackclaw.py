#!/usr/bin/env python3
"""
Black Claw Exploitation Framework
"""
import lib.tcp_server as server
import lib.session as session
import lib.modload as modload
from terminaltables import AsciiTable 
import lib.shm as shm
import lib.job as job

mload = modload.ModuleLoader()
mload.load_modules('/home/vanilla/Data/Dev/Python/blackclaw/modules')

# Active Sessions List
shm.modules = mload.get_modules()
run_main = True


"""
s1 = session.Session()

sessions.append(s1)
s = server.TCPServer(address='127.0.0.1',port=9001)
s.run()
s1.set_server(s)
s1.interact()
mod.set_session(s1)
"""

def handle_interact(command):
    try:
        p = command.split(' ')
        if len(p) == 1:
            print("[x] Missing Value. Cannot interact with nothing!")
        elif len(p) > 1:
            t = is_number(p[1])
            if t == True:
                n = int(p[1])
                if len(shm.sessions) >= n:
                    s = shm.sessions[n]
                    if s != None:
                        print(f"[*] Interacting with {s.name}")
                        print()                    
                        s.interact()
            else:
                s = find_session(p[1])
                print(f"[*] Interacting with {s.name}")
                print()
                s.interact()
    except Exception as x:
        print(f"[x] {x}")
        
def handle_modul_usage(command):
    try:
        p = command.split(' ')
        if len(p) == 1:
            print("[x] Missing Value. Cannot use nothing! :O")
        elif len(p) > 1:
            t = is_number(p[1])
            if t == True:
                n = int(p[1])
                if len(shm.modules) >= n:
                    m = shm.modules[n]
                    if m != None:
                        m.use_module()
            else:
                m = find_module(p[1])
                m.use_module()
    except Exception as x:
        print(f"[x] {x}")
        
def is_number(a):
    try:
        n = int(a)
        return True
    except:
        return False
def command_interpreter(command):
    global run_main
    # sessions
    # interact <session name>
    # use <module_name>
    # list modules
    # 
    # 
    if command.lower() == 'sessions':
        print_sessions()
    if command.startswith('interact'):
        handle_interact(command)
    if command.startswith('use'):
        handle_modul_usage(command)
    if command.lower() == 'list modules':
        cnt = 0
        table_data = []
        header = ['#','Name','Description']
        table_data.append(header)
        for m in shm.modules:
            mod = [str(cnt)+".",m.name,m.description]
            table_data.append(mod)
            cnt += 1
        table = AsciiTable(table_data)
        print(table.table)
    if command.lower() == 'help' or command == '?':
        print_help()
    if command.lower() == 'jobs':
        for j in shm.jobs:
            print(f"Job Name:{j.name}")
    if command.lower() == 'exit':
        run_main = False


def print_help():
    help = """
    Available Commands
    ------------------
    help, ?                 Show help
    sessions                List all available sessions
    interact <session name> Interact with available session
    use <module name>       Use a selected module
    list modules            List all Available Modules
    
    """
    print(help)


def find_module(name):
    for m in shm.modules:
        if m.name == name:
            return m
    return None

def find_session(name):
    for s in shm.sessions:
        if s.name == name:
            return s
    return None

def print_sessions():
    header = ['#','Name','Connection']
    table_data = []
    table_data.append(header)
    c = 0
    for s in shm.sessions:
        table_data.append([str(c)+".",s.name,f"{s.client_address}:{str(s.client_port)}"])
        c += 1
    table = AsciiTable(table_data)
    print(table.table)


def find_dead_connections():
    for s in shm.sessions:
        if s.check_session_alive() == False:
            shm.sessions.remove(s)
            
def print_logo():
    with open('logo','r') as l:
        logo = l.read()
    print(logo)
    

def main():
    global run_main
    print_logo()
    while run_main:
        find_dead_connections()
        print()
        command = input('black_claw> ')
        command_interpreter(command)
    
# Start the main application
main()