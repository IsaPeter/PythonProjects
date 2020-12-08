#!/usr/bin/python3
import socket,os, sys, argparse, queue, threading, string, random
from datetime import datetime



start_port = 1
end_port = 65535
host = 'localhost'
thread_num = 1
timeout = .5    
open_ports = []
scanned_ports = 0
total_open = 0
total_closed = 0
port_queue = queue.Queue()
thread_pool = []


def get_port_range(inaddress):
    res = []
    if '-' in inaddress:
        p = inaddress.split('-')
        res = p
    else:
        res = [int(p),int(p)]
    return res

def parsing_arguments():
    global start_port, end_port, host, thread_num
    parser = argparse.ArgumentParser()
    parser.add_argument('-H','--host',dest="host",help='The host of the scan')
    parser.add_argument('-p','--port',dest="port",help='The port (range)')
    parser.add_argument('-t','--threads',dest='threads',help='The scanning threads number')
    
    
    args = parser.parse_args()
    
    if args.port:
        r = get_port_range(args.port)
        start_port = int(r[0])
        end_port = int(r[1])
    if args.host: host = args.host
    if args.threads: thread_num = int(args.threads)
    

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



def thread_scan():
    global timeout, total_open, total_closed,port_queue,open_ports, host, scanned_ports
    #name = id_generator()
    while not port_queue.empty():
        port = port_queue.get()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            s.settimeout(timeout)
            # returns an error indicator 
            result = s.connect_ex((host, port)) 
            if result == 0:
                print("tcp/{} is open".format(port))
                total_open += 1
            else:
                #print(name+": Port closed: "+str(port))
                total_closed += 1
            s.close()
            scanned_ports += 1
    
        except:
            pass
        
def main():
    global host, start_port, end_port,thread_num,port_queue, thread_pool, scanned_ports, total_open, total_closed
        
    parsing_arguments()
    # parse given arguments
    if not host:
        print("[!] Missing target!")
        sys.exit(1)
    # get size of the range 
    if end_port-start_port < thread_num: thread_num = end_port - start_port
    start_time = datetime.now()
    # Add Banner
    print("-" * 50)
    print("Scanning Target: " + host)
    print("Scanning started at:" + str(start_time))
    print("-" * 50)
    
    # put ports to queue
    for p in range(start_port,end_port+1):
        port_queue.put(p)    
    
    for tn in range(thread_num):
        t = threading.Thread(target=thread_scan)
        thread_pool.append(t)
        t.start()
    
    for th in thread_pool:
        th.join()

    #port_queue.join()
    end_time = datetime.now()
    elapsed = end_time - start_time
    print()
    print("Total Scanned Ports Number : "+str(scanned_ports))
    print("Total Open Ports Number : "+str(total_open))
    print("Closed Ports Number : "+str(total_closed))
    print("Elapsed Time: "+str(elapsed))
    
if __name__ == '__main__':
    main()
