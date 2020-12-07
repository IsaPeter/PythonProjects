#!/usr/bin/enc python3
import socket, os, json, sys, argparse


target_address = '127.0.0.1'
target_port = 9999
file_data = {'name':'','size':'','method':''}
file_upload = False
file_download = False
file_name = ""
out_fname = ""
list_files = False
recv_len = 1024

def parsing_arguments():
    global target_address, target_port, file_upload, file_download, file_name, out_fname, list_files
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--target',help='The target host server')
    parser.add_argument('-p','--port',help='The target host port')
    parser.add_argument('-U','--upload',action='store_true',help='Upload a file')
    parser.add_argument('-D','--download',action='store_true',help='Download a file')
    parser.add_argument('-f','--file',help='file to upload of download')
    parser.add_argument('-o','--out-file',dest='outfile',help='Output file name')
    parser.add_argument('-L','--list',dest='listfiles',action='store_true',help='List Remote Files')    
    args = parser.parse_args()
    
    if args.target: target_address = args.target
    if args.port : target_port = int(args.port)
    if args.upload: file_upload = True
    if args.download: file_download = True
    if args.file: file_name = args.file
    if args.outfile: out_fname = args.outfile
    if args.listfiles: list_files = args.listfiles
    

def list_remote_files(client):
    global recv_len,file_data
    try:
        file_data['method'] = 'list'
        header = json.dumps(file_data)
        client.send(header.encode())
        r = 1
        response = b''
        while r:
            data = client.recv(recv_len)
            response += data
            r = len(data)
            if r < recv_len:
                recv_len = 0
                break  
        received_data = data.decode()
        files = json.loads(received_data)
        if len(files) > 0:
            for f in files:
                print(f)
    except Exception as x:
        print("Failed to list remote host")
        print(x)
    
def download(sock,filename):
    global file_name, out_fname, file_data
    try:
        # sending download request
        file_data['name'] = filename
        file_data['method'] = 'download'
        if out_fname == "": out_fname = filename
        header = json.dumps(file_data)
        sock.send(header.encode())
        resp = sock.recv(1024).decode()
        resp_fd = json.loads(resp)
        
        if resp_fd['status'] == 'download ok':
            size = int(resp_fd['size'])
            remaining = size
            received = 0
            with open(out_fname,'wb') as f:
                while remaining >0:
                    recv_data = b''
                    if size < 1024:
                        recv_data = sock.recv(size)
                        f.write(recv_data)
                        received = size
                        remaining = 0
                    else:
                        if received < size:
                            if remaining < 1024:
                                recv_data = sock.recv(remaining)
                                received += remaining
                                remaining = 0
                                f.write(recv_data)
                            else:
                                recv_data = sock.recv(1024)
                                received += 1024
                                remaining -= 1024
                                f.write(recv_data)
                    print("file uploading {total}/{current} ==> {filename}\r".format(total=str(size),current=str(received),filename=file_data['name']),end='')
            print()
            print("Download Successful!")
            f.close()
            sock.close()
                
        else:
            print(resp_fd['status'])
            sys.exit(1)
        
        
        
        
    except Exception as x:
        print("Download Failed")
        print(x)
    
    
    
    
def upload(sock,filename):
    try:
        file_data['size'] = os.path.getsize(filename)
        file_data['name'] = filename
        file_data['method'] = 'upload'
        header = json.dumps(file_data)
        currentp = 0
        nextp = 1024
        remaining = int(file_data['size'])
        with open(filename,'rb') as f:
            data = f.read()
        sock.send(header.encode())
        ok = sock.recv(10).decode()
        if ok.lower() != "upload ok":
            sys.exit(1)
        else:
            while remaining > 0:
                if len(data) < 1024:
                    send_data = data
                    currentp = remaining
                    remaining = 0
                else:
                    if remaining < 1024 :
                        send_data = data[currentp:currentp+remaining]
                        currentp += remaining
                        remaining = 0
                        
                    else:
                        send_data = data[currentp:nextp]
                        currentp += 1024
                        nextp += 1024
                        remaining -= 1024
                sock.send(send_data)
                print("{total}/{current}\r".format(total=str(file_data['size']),current=str(currentp)),end='')
            print()
            print("Upload OK")
    except Exception as x:
        print("Upload Failed")
        print(x)
        
def main():
    global target_address, target_port, file_upload, file_download, file_name, list_files
    parsing_arguments()
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((target_address,target_port))  
    
    if list_files:
        list_remote_files(client)
        sys.exit(0)
    if file_upload:
        upload(client,file_name)
    if file_download:
        download(client,file_name)
        
        
main()