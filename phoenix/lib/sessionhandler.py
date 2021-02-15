#!/usr/bin/env python3

import socket, string, random, os, sys, readline
runpath = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
sys.path.append(os.path.join(runpath,'..'))
sys.path.append(approot)
import lib.shell as shell
import lib.shm as shm
from lib.helpmenu import HelpMenu
from lib.tabCompleter import tabCompleter

# Handles the different sessions
class sessionHandler():
    def __init__(self,tcpclient):
        self.interact = True
        self.client = tcpclient
    def interactive(self):
        try:
            while self.interact:
                cmd = input(f"phoenix({self.client.name})> ")
                cmd = cmd.rstrip(' ')
                if self.client.dead == False:
                    self.command_interpreter(cmd)
                else:
                    print("[!] The connection is semms to Dead!")
                    self.interact = False
                    break
        except KeyboardInterrupt:
            pass
        
    def command_interpreter(self,command):
        if len(command) >0:
            if command.startswith(':'):
                if command in [':bg',':exit']:
                    self.interact = False
                elif command == ':terminate':
                    self.client.client.close()
                    self.interact_module = False
                elif command == ':help':
                    self.help()
                elif command == ':info':
                    self.shell_info()              
                elif command.startswith(':'):
                    module_name = command.split(' ',1)[0].replace(':','')
                    module = self.__get_module_by_id(module_name)
                    if module:
                        if len(module_name)>1:
                            module.run(command.replace(':'+module_name,''))
                        else:
                            module.interactive()
            else:
                self.client.send(command+"\n")
                data = self.client.receive_all()
                print(data.decode())
                
    def help(self):
        h = HelpMenu()
        h.inner_heading_row_border = False
        h.title = "Show Client Help"
        h.add_item(':bg, :exit','Exit from the current interactive session')
        h.add_item(':terminate','Terminate the current session')
        h.add_item(':<module_name>','Run a specified module')
        h.add_item(':help','Show this menu')
        h.add_item(':info','Show Shell Information')
        h.print_help()
    def __get_module_by_id(self,module_id):
        for m in shm.loaded_modules:
            if m.module_id == module_id:
                return m    
    def shell_info(self):
        h = HelpMenu()
        h.title=f"Shell Information"
        sockname = self.client.client.getsockname()
        localaddress = self.client.address
        h.add_item('Name:',self.client.name)
        h.add_item("Remote:",f"{str(sockname[0])}:{str(sockname[1])}")
        h.add_item("Local:",f"{str(localaddress[0])}:{str(localaddress[1])}")
        h.add_item('Shell Type:',self.client.shelltype.name)
        h.print_help()
        