#!/usr/bin/env python3
import crypt
import os,sys
# append base path to sys.path
runpath = os.path.dirname(os.path.realpath(__file__))
approot = os.path.abspath(os.path.join(runpath, os.pardir))
sys.path.append(os.path.join(runpath,'..'))
sys.path.append(approot)
import lib.commandparser as cp

# python3 -c 'import crypt; print(crypt.crypt("test", crypt.mksalt(crypt.METHOD_SHA512)))'
module_name ="Make Password"
module_id = "mkpasswd"
module_description="Create UNIX like passwords"
module_type = 'module'
variables = {'password':'','type':'sha512',}
args = None
parser = None

def parse_arguments(command):
    global args, parser
    parser = cp.commandParser(command)
    parser.add_argument('-t','--type',name='hashtype',help='The type of the used HASH algo.')
    parser.add_argument('-p','--password',name='password',help='The password string')
    parser.add_argument('-l','--list',name='listtypes',hasvalue=False,help='list the available hash types')
    parser.add_argument('-h','--help',name='help',hasvalue=False,help='Show the help menu')
    
    args = parser.parse()
    return args

def help():
    pass
    
    
def run(arguments=''):
    makepass = True
    hashtype = 'sha512'
    password = ''
    if arguments == '':
        password = variables['password']
        if password != '':
            print(crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512)))
        else:
            print("Please specify a Password string")
    else:
        args = parse_arguments(arguments)
        if parser.exists('password'): password = parser.get_value('password')
        if parser.exists('hashtype'): hashtype = parser.get_value('hashtype').lower()
        if parser.exists('listtypes'):
            makepass == False
            print("Blowfish; Crypt; MD5; SHA256; SHA512")
            return None
        if parser.exists('help'):
            parser.print_help()
        
        if makepass:
            if password != '':
                if hashtype == 'blowfish':
                    print(crypt.crypt(password, crypt.mksalt(crypt.METHOD_BLOWFISH)))
                elif hashtype == 'crypt':
                    print(crypt.crypt(password, crypt.mksalt(crypt.METHOD_CRYPT)))
                elif hashtype == 'md5':
                    print(crypt.crypt(password, crypt.mksalt(crypt.METHOD_MD5)))                
                elif hashtype == 'sha256':
                    print(crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA256)))
                elif hashtype == 'sha512':
                    print(crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512)))                
                    
                    
#run('programneme --help')