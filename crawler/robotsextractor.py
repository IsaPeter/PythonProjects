#!/usr/bin/env python3
"""
Python Robots Extractor
"""
import requests,re

class robotsextractor():
    def __init__(self,url):
        self.url = url
        self.disallows = []
        self.allows = []
        self.sitemaps = []
    def check(self):
        if self.url.endswith('/'):
            roboturl = self.url+"robots.txt"
        else:
            roboturl = self.url+"/robots.txt"
        resp = requests.get(roboturl)
        if resp.status_code == 200:
            print(f"[+] Robots Found [{str(resp.status_code)}]")
        else:
            print(f"[!] Response [{str(resp.status_code)}]")

    def __extract_disallows(self,data):
        pattern = r'Disallow: (/.*)'
        match = re.findall(pattern,data,re.I)
        for m in match:
            if self.url.endswith("/"):
                p = self.url+m.lstrip('/')
            else:
                p = self.url+"/"+m
            self.disallows.append(p)
                
    def __extract_allows(self,data):
        pattern = r"Allow:.*(/.*)"
        match = re.findall(pattern,data,re.I)
        for m in match:
            if self.url.endswith("/"):
                p = self.url+m.lstrip('/')
            else:
                p = self.url+"/"+m
            self.allows.append(p)
            
    def __extract_sitemaps(self,data):
        pattern = r'sitemap:.*(\/.*)'
        match = re.findall(pattern,data,re.I)
        for m in match:
            if not m.startswith(self.url):
                if self.url.endswith("/"):
                    p = self.url+m.lstrip('/')
                else:
                    p = self.url+"/"+m
            else:
                p = m
            self.sitemaps.append(p)
            
    def extract(self, uri=""):
        if uri == "":
            roboturl = self.url
            if 'robots.txt' not in roboturl:
                if roboturl.endswith('/'):
                    roboturl = roboturl + "robots.txt"
                else:
                    roboturl = roboturl + "/robots.txt"
        else:
            roboturl = uri
            if 'robots.txt' not in roboturl:
                if roboturl.endswith('/'):
                    roboturl = roboturl + "robots.txt"
                else:
                    roboturl = roboturl + "/robots.txt"            
            
        resp = requests.get(roboturl)
        if resp.status_code == 200:
            robotsdata = resp.text
            self.__extract_disallows(robotsdata)
            self.__extract_allows(robotsdata)
            self.__extract_sitemaps(robotsdata)
        else:
            print("[X] Failed to extract robots Data")
        


    def get_links(self):
        return self.disallows+self.allows+self+self.sitemaps