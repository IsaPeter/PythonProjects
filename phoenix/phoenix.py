#!/usr/bin/env python3
"""
Phoe*NIX Post Exploitation Framework

"""
import os,sys
# append base path to sys.path
runpath = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
sys.path.append(os.path.join(runpath,'..'))
sys.path.append(approot)

import lib.modload as modload
import lib.shm as shm
import lib.dcfind as dc
import lib.livedebug as debug
from lib.helpmenu import HelpMenu
import lib.sessionhandler as sh
import lib.phoenixlibs as plib


# Variables
prompt_string = 'phoenix > '    # The Phoenix default prompt string
run_app = True                  # Handle the main thread to run if False the main will end
list_result = []
# The array which contains the paths of modules
module_paths = ['modules','listeners']
dcf = dc.dead_connection_finder()


# Loading Phoenix associated modules
def load_modules():
    global module_paths
    
    loader = modload.ModuleLoader() # Create a module loader
    
    for p in module_paths:
        path = os.path.join(os.getcwd(),p) # Create a joined path for actual path
        loader.load_modules(path) # loading the modules
    
    shm.loaded_modules = loader.get_modules() # Set the loaded modules into SHM (Shared Memory)

# interpret the given command to make the application interactive.
def command_interpreter(command):
    global run_app
    
    if command.startswith("list"): # list modules
        listable = command.split(' ',1)
        if len(listable) == 2:
            if listable[1] in ['modules','m']:
                list_type('module')
            elif listable[1] in ['listeners','l']:
                list_type('listener')
            elif listable[1] in ['sessions','s']:
                list_sessions()
        elif len(listable) < 2:
            print("[!] Invalid Argument.")
        
    elif command.startswith("use"): # using a module
        cmd_split = command.split(' ',1)
        if len(cmd_split) == 2:
            name = cmd_split[1]
            use_module(name)
        elif len(cmd_split) < 2:
            print("[!] Not enough parameter")
    elif command == "help": # show the help
        show_help()
    elif command.startswith("info"): # show info for a specified module
        name = command.split(' ',1)
        if len(name) == 2:
            show_module_info(name[1])
        elif len(name) < 2:
            print("[!] Not enough parameter")
    elif command.startswith("search"): # search in modules
        pass
    elif command == "exit": # exit from the application
        dcf.stop()
        run_app = False
        
        print("Exiting.. Bye!")
    elif command == "sessions":
        list_sessions()
    elif command.startswith('interact'):
        a = command.split(' ',1)
        if len(a) == 2:
            interact(a[1])
        elif len(a) < 2:
            print("[!] Missing parameter [session_name].")
    elif command == 'debug':
        debug.debugger()
    elif command.startswith('run'):
        r = command.split(' ',1)
        if len(r) > 1:
            module_parts = r[1].split(' ',1)
            if len(module_parts) > 1:
                module_name = module_parts[0]
                module_args = module_parts[1]
                rm = plib.RunModule(module_name)
                rm.run(module_args)
            else:
                module_name = module_parts[0]
                rm = plib.RunModule(module_name)
                rm.run()
        else:
            print("[!] The run module need least 1 argument")
      
def interact(session_name):
    not_found = True
    if is_number(session_name):
        num = int(session_name)
        if num <= len(shm.connected_clients) and len(shm.connected_clients) >0:
            s = shm.connected_clients[num]
            shm.current_session = s
            handler = sh.sessionHandler(s)
            handler.interactive()
        else:
            print(f"[!] {str(num)} is not a valid index!")
    else:
        for s in shm.connected_clients:
            if s.name == session_name:
                not_found = False
                shm.current_session = s
                handler = sh.sessionHandler(s)
                handler.interactive()                
        if not_found:
            print(f"[!] Does not found session with name {session_name}!")
def list_sessions():
    i = 0
    print("\nAvailable Sessions\n------------------\n")
    for s in shm.connected_clients:
        sockname = s.client.getsockname()
        localaddress = s.address
        print(f"{str(i)}.\t{s.name}\t{s.shelltype.name}\t{sockname[0]}:{str(sockname[1])} => {localaddress[0]}:{str(localaddress[1])}")
        i += 1
    print()
    
    
def use_module(modname):
    global list_result
    is_result = False
    mod_name = ''
    mod_type = ''
    
    # get the module name and type from number
    if is_number(modname):
        n = int(modname) # the actual number
        if n <= len(list_result):
            if len(list_result) > 0:
                res = list_result[n]
                mod_name = res['name']
                mod_type = res['type']
                is_result = True
            else:
                print(f"[!] No item with index {str(n)}")
        else:
            print(f"[!] {str(n)} is not a valid index number")
    else:
        
        for r in list_result:
            if r['name'] == modname or r['id'] == modname:
                res = r
                mod_name = res['name']
                mod_type = res['type']
                is_result = True
                
    if is_result == False:
        m = get_module_by_name(modname)
        if m:
            m.interactive()
        else:
            m = get_module_by_id(modname)
            if m:
                m.interactive()
            else:
                print('[!] Not found.')            
    else:
        m = get_module_by_name(mod_name)
        if m:
            m.interactive()
        else:
            m = get_module_by_id(mod_name)
            if m:
                m.interactive()
            else:
                print('[!] Not found.')    
    
# Show the help menu    
def show_help():
    
    h = HelpMenu()
    h.inner_heading_row_border = False
    h.title = "Phoenix Help Menu"
    h.add_item('list [type]','List all available [modules, listeners, sessions]')
    h.add_item('use','Use a selected mofule')
    h.add_item('info','Shows info for a specified module')
    h.add_item('sessions [name/number]','Show active sessions')
    h.add_item('interact [name/number]','Interact with active session')
    h.add_item('help','Shows this menu')
    h.add_item('exit','Exit from the application')
    h.print_help()



# Show the info for a module
def show_module_info(module_name):
    
    if is_number(module_name):
        num = int(module_name)
        if num <= len(shm.loaded_modules):
            module = shm.loaded_modules[num]
            module.show_info()
        else:
            print(f"[!] The given number is not valid!")
    else: # This means the given argument is a string
        module = get_module_by_name(module_name)
        if module:
            module.show_info()
        else:
            print(f"[!] Module with name: '{module_name}' does not exists!")

# returns back a module if name is exists
def get_module_by_name(module_name):
    for m in shm.loaded_modules:
        if m.name == module_name:
            return m
        
def get_module_by_id(module_id):
    for m in shm.loaded_modules:
        if m.module_id == module_id:
            return m
def list_type(type_name):
    global list_result
    i = 0
    list_result.clear()
    h = HelpMenu()
    h.title=f"\nAvailable {type_name}s\n-----------------\n"
    
    for m in shm.loaded_modules:
        if m.module_type == type_name:
            list_result.append({'name':m.name,'id':m.module_id,'number':i,'type':type_name})
            h.add_item(str(i)+'.',m.module_id,m.name)
            #print(f"{str(i)}. {m.module_id}\t{m.name}")
            i += 1
    h.print_help()
    print("\n")
def __get_autocomplete_names():
    lista = ['list','modules','sessions','interact']
    if len(shm.connected_clients) > 0:
        for s in shm.connected_clients:
            lista.append(s.name)
    return lista
# Check if an input is number or not
def is_number(cmd):
    try:
        num = int(cmd)
        return True
    except:
        return False
    

def main():
    global run_app, dcf
    
    load_modules() # Loading framework modules
    dcf.start()
    
    shm.tab_complete.createListCompleter(__get_autocomplete_names())
    shm.readline.set_completer(shm.tab_complete.listCompleter) 
    
    while run_app:
        cmd = input(prompt_string)
        cmd = cmd.rstrip(' ')
        command_interpreter(cmd)
        
    
if __name__ == '__main__':
    main()