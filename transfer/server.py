#!/usr/bin/env python3
import socket, sys, json,threading
import argparse, os,time


listen_address = '0.0.0.0'
listen_port = 9999
clients_num = 10
save_directory = ''

def upload_file(client,file_data):
    global save_directory
    try:
        #print("the file name is: "+file_data['name'])
        client.send('upload ok'.encode())
        received = 0
        size = int(file_data['size'])
        remaining = size
        with open(save_directory+"/"+file_data['name'],'wb') as f:
            while remaining >0:
                recv_data = b''
                if size < 1024:
                    recv_data = client.recv(size)
                    f.write(recv_data)
                else:
                    if received < size:
                        if remaining < 1024:
                            recv_data = client.recv(remaining)
                            received += remaining
                            remaining = 0
                            f.write(recv_data)
                        else:
                            recv_data = client.recv(1024)
                            received += 1024
                            remaining -= 1024
                            f.write(recv_data)
                print("file uploading {total}/{current} ==> {savedir}/{filename}\r".format(total=str(size),current=str(received),savedir=save_directory,filename=file_data['name']),end='')
        print()
        print("Upload Successful!")
        f.close()
        client.close()
    except Exception as x:
        print("Upload Failed!")
        print(x)
        
        
def download_file(client,file_data):
    
    try:
        fname = file_data['name']
        if os.path.exists(fname):
            file_data['status'] = 'download ok'
            file_data['size'] = os.path.getsize(fname)
            header = json.dumps(file_data)
            client.send(header.encode())
            time.sleep(1)
            currentp = 0
            nextp = 1024
            remaining = int(file_data['size'])
            with open(fname,'rb') as f:
                data = f.read()
                
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
                client.send(send_data)
                print("{total}/{current}\r".format(total=str(file_data['size']),current=str(currentp)),end='')
            print()
            print("Download OK")            
        else:
            print("File Does not Exists: "+fname)
    except Exception as x:
        print(x)
    
    
def parsing_arguments():
    global listen_address, listen_port, clients_num, save_directory
    parser = argparse.ArgumentParser()
    parser.add_argument('-A','--address',help='Listening address')
    parser.add_argument('-P','--port',help='Listening port')
    parser.add_argument('-C','--clients-number',dest='clientsnumber',help='Number of concurrent clients')
    parser.add_argument('-D','--directory',help='File collecting Directory')
    
    args = parser.parse_args()
    
    if args.address: listen_address = args.address
    if args.port: listen_port = int(args.port)
    if args.clientsnumber: clients_num = int(args.clientsnumber)
    if args.directory: save_directory = args.directory

def list_files(client):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    send_data = json.dumps(files)
    client.send(send_data.encode())
    client.close()
    
def handle_client(client,address):
    global save_directory
    header = client.recv(1024).decode() # get the file_data
    file_data = json.loads(header)
    if file_data['method'] == 'upload':
        print(f"Uploading file from {str(address[0])}:{str(address[1])} [{file_data['name']}]")
        upload_file(client,file_data)
    elif file_data['method'] == 'download':
        print(f"Downloading file to {str(address[0])}:{str(address[1])} [{file_data['name']}]")
        download_file(client,file_data)
    elif file_data['method'] == 'list':
        list_files(client)
    
    



def check_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)    
def listening():
    s = socket.socket()
    s.bind((listen_address,listen_port))
    s.listen(clients_num) # Accepts up to 10 connections.
    print("Listening on {A}:{P}".format(A=listen_address,P=str(listen_port)))
    
    while True:
        sc, address = s.accept()
    
        #print("Client conencted from {A}:{P}".format(A=str(address[0]),P=str(address[1])))
        t = threading.Thread(target=handle_client,args=(sc,address,))
        t.start()
    
    s.close()    
def main():
    global save_directory
    parsing_arguments()
    if save_directory != '':
        check_dir(save_directory)
        print("Saving Directory is: "+save_directory)
    listening()

if __name__ == '__main__':
    main()