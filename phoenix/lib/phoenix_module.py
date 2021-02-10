#!/usr/bin/env python3


# The Phoenix Module Class
class phoenix_module:
    def __init__(self,module):
        self.module = module                            # The module instance
        self.name = module.module_name                  # The name of the loaded module
        self.description = module.module_description    # The Description of the loaded module
        self.interact = False                           # When interact the module this variable handle the while loop
        self.module_type = module.module_type
        self.module_id = module.module_id
        
    def __set_module(self,mod):
        self.module = mod
        self.__get_name()
        self.__get_description()
        self.__get_type()
        self.__get_module_id()
        
    def __get_name(self):
        if self.module != None:
            self.name = self.module.module_name
            
    def __get_type(self):
        if self.module != None:
            self.module_type = self.module.module_type
    def __get_module_id(self):
        if self.module != None:
            self.module_id = self.module.module_id
            
    def __get_description(self):
        if self.module != None:
            self.description = self.module.module_description
    def run(self,arguments):
        if self.module != None:
            try:
                self.module.run(arguments)
            except Exception as x:
                print(f"[x] {x}")
        else:
            print(f"[x] The module is Empty!")
    def interactive(self):
        if self.module != None:
            self.interact = True
            try:
                while self.interact:
                    cmd = input(f"phoenix({self.name}) > ")
                    self.command_interpreter(cmd)
                    
            except Exception as x:
                print(f"[x] {x}")
        else:
            print(f"[x] The module is Empty!")  
            
    def show_info(self):
        if self.module != None:
            try:
                info = f"\nName: {self.module.module_name}\nDescription: {self.module.module_description}\n"
                print(info)                
            except Exception as x:
                print(f"[x] {x}")
        else:
            print(f"[x] The module is Empty!")
    def show_module_options(self):
        if self.module != None:
            try:
                print("\nOptions\n--------\n")
                for n, v in self.module.variables.items():
                    print(f"{n}\t\t{v}")
                print("\n")
            except Exception as x:
                print(f"[x] {x}")
        else:
            print(f"[x] The module is Empty!")
    def show_help(self):
        print("\nCommands\n--------\n")
        print("bg, exit\tExit from the module")
        print("(show) options\tShow available module options")
        print("(show) info\tShow information about the module")
        print("set\t\tSet value for a module variable")
        print("unset\t\tUnset value for a module variable")
        print("help\t\tShow this menu")
        print()
    
    def command_interpreter(self,command):
        if command == 'bg' or command == 'exit':
            self.interact = False
        elif command == 'options' or command == 'show options':
            self.show_module_options()
        elif command in ['info','show info']:
            self.show_info()
        elif command.startswith('set'):
            try:
                p = command.split(' ',2)
                variable = p[1]
                value = p[2]
                self.module.variables[variable] = value
                print(f"[*] Set {variable} => {value}")
            except Exception as x:
                print(f"[x] {x}")
                
        elif command.startswith('unset'):
            p = command.split(' ',1)
            v = p[1]
            variables[v]= ''        
        elif command == 'help':
            self.show_help()