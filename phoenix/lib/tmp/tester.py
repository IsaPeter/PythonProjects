import os
import pty
import socket
import shell
import tcp_server as ts
import address_pool as ap
import importlib
import sys
import lib.modload as ml


module = ml.ModuleLoader()
module.load_modules('/home/venom/Data/dev/python/PythonProjects/phoenix/modules/')
for m in module.get_modules():
    print(m.name)


"""
import pkgutil
search_path = ['/home/venom/Data/dev/python/PythonProjects/phoenix/modules/'] # set to None to see all modules importable from sys.path
all_modules = [x[1] for x in pkgutil.walk_packages(path=search_path)]
print(all_modules)
"""




"""
address = ('127.0.0.1',4445)
s = shell.Shell(addr=address,bind=False)
s.handle()
"""

"""
server = ts.TCPServer(port=9004)
server.listen()
client = server.get_client()
client.interactive_module()
#intshell = shell.InteractiveShell(client)
#intshell.handle()
#print("Handle again..")
#intshell.handle()
"""
"""
a = ap.addressPool()
for _ in range(0,30):
    print(a.get_address())
"""