#!/usr/bin/env python3

module_name ="Name of the module"
module_description="description of the module"
variables = {}


def get_module_result():
    return None
def show_info():
    info = f"\nName: {module_name}\nDescription: {module_description}\n"
    print(info)
def show_module_options():
    print("\nOptions\n--------\n")
    for n, v in variables.items():
        print(f"{n}\t\t{v}")
    print("\n")
def interactive():
    run_interactive = True
    prompt = f"{module_name}> "
    while run_interactive:
        command = input(prompt)
        if command.lower() == 'options' or command.lower() == 'show options':
            show_module_options()
        if command.lower() == 'info' or command.lower() == 'show info':
            show_info()
        if command.startswith('set'):
            p = command.split(' ',2)
            variable = p[1]
            value = p[2]
            variables[variable] = value
            print(f"[*] Set {variable} => {value}")
        if command.startswith('unset'):
            p = command.split(' ',1)
            variable = p[1]
            variables[variable]= ''
        if command.lower() == 'run':
            try:
                run()
            except Exception as x:
                print(x)
        if command.lower() == 'bg':
            run_interactive = False        
    
def run(arguments=''):
    pass