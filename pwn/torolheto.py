#!/usr/bin/env python3
import requests, re, subprocess,os

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

for s in suid_binaries:
    if s in uniq:
        print(f"[!] Privesc: {s}")