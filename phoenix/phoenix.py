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


# Variables
prompt_string = 'phoenix > '    # The Phoenix default prompt string
run_app = True                  # Handle the main thread to run if False the main will end





# Loading Phoenix associated modules
def load_modules():
    loader = modload.ModuleLoader() # Create a module loader
    path = os.path.join(os.getcwd(),'modules') # Create path for modules
    loader.load_modules(path) # loading the modules
    shm.loaded_modules = loader.get_modules() # Set the loaded modules into SHM (Shared Memory)
    

# interpret the given command to make the application interactive.
def command_interpreter(command):
    global run_app
    
    if command == "list modules": # list modules
        list_all_modules()
    elif command.startswith("use"): # using a module
        name = command.split(' ',1)[1]
        use_module(name)
    elif command == "help": # show the help
        show_help()
    elif command.startswith("info"): # show info for a specified module
        name = command.split(' ',1)
        show_module_info(name[1])
    elif command.startswith("search"): # search in modules
        pass
    elif command == "exit": # exit from the application
        run_app = False
        print("Exiting.. Bye!")
        
def use_module(modname):
    if is_number(modname):
        n = int(modname) # the actual number
        if n <= len(shm.loaded_modules):
            m = shm.loaded_modules[n] # the module from the SHM
            m.interactive()
    else:
        m = get_module_by_name(modname)
        if m:
            m.interactive()
    
    
# Show the help menu    
def show_help():
    help = """\n
    Help
    ----
    
    list modules\tList all available modules
    use\t\t\tUse a selected module
    info\t\tShows info for a specified module
    help\t\tShows this menu
    """
    print(help+"\n")

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

# List all available modules
def list_all_modules():
    i = 0
    print("\nAvailable Modules\n-----------------\n")
    for m in shm.loaded_modules:
        print(f"{str(i)}. {m.name}")
        i += 1
    print("\n")
    
# Check if an input is number or not
def is_number(cmd):
    try:
        num = int(cmd)
        return True
    except:
        return False
    
def main():
    global run_app
    
    load_modules() # Loading framework modules
    
    
    while run_app:
        cmd = input(prompt_string)
        command_interpreter(cmd)
        
    
if __name__ == '__main__':
    main()