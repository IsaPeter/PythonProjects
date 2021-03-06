#!/usr/bin/env python3
import requests
import re
from urllib.parse import urlparse
from urllib.parse import urljoin


class PyCrawler(object):
    def __init__(self, starting_url):
        self.starting_url = starting_url
        self.url_data = urlparse(starting_url)
        self.visited = set()
        self.cookie = {}
        self.crawl_depth = 3
        self.samesite = True
        self.links = []
        self.sources = []
        self.links_found = 0
        self.showlinks = True
    
    def set_cookie(self,cookies):
        if cookies == type(""):
            formatter = cookie_formatter()
            formatter.parse(cookies)
            self.cookie = formatter.cookies
        else:
            self.cookie = cookies
    def get_all_links(self):
        res = []
        for s in self.sources:
            if s not in res:
                res.append(s)
        for l in self.links:
            if l not in res:
                res.append(l)
        return res
    
    def get_html(self, url):    
        try:    
            html = requests.get(url,cookies=self.cookie)    
        except Exception as e:    
            print(e)    
            return ""    
        return html.content.decode('latin-1') 

    def get_links(self, url):    
        html = self.get_html(url)    
        parsed = urlparse(url)
        if parsed.path != "":
            base = f"{parsed.scheme}://{parsed.netloc.lstrip('/').rstrip('/')}/{parsed.path.lstrip('/')}"
        else:
            base = f"{parsed.scheme}://{parsed.netloc}"
        li = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', html)    
        for i, link in enumerate(li): 
            if not urlparse(link).netloc:
                if base.endswith("/") and link.startswith("/"):
                    link_with_base = urljoin(base.rstrip("/"),link)
                else:
                    link_with_base = urljoin(base,link)
                li[i] = link_with_base
                self.links.append(link_with_base)
        
        for s in self.get_src(html,base):
            if s not in self.sources:
                self.sources.append(s)
                if self.showlinks:
                    print(s)
        
        return sorted(li)    
    
    def get_src(self,html,base):
        #html = self.get_html(url)    
        #parsed = urlparse(url)    
        #if parsed.path != "":
        #    base = f"{parsed.scheme}://{parsed.netloc.lstrip('/').rstrip('/')}/{parsed.path.lstrip('/')}"
        #else:
        #    base = f"{parsed.scheme}://{parsed.netloc}"  
        links = re.findall('''src="([^"]*)"''', html)    
        for i, link in enumerate(links): 
            if not link.startswith('data:image'):                                    
                if not urlparse(link).netloc:
                    if base.endswith("/") and link.startswith("/"):
                        link_with_base = urljoin(base.rstrip("/"),link)
                    else:
                        link_with_base = urljoin(base,link)
                    links[i] = link_with_base     

        return set(filter(lambda x: 'mailto' not in x, links))        

    def extract_info(self, url):                                
        html = self.get_html(url)                               
        return None                  
    
    def crawl(self, url, depth=1):
        if depth <= self.crawl_depth:
            current_depth = depth
            for link in self.get_links(url):    
                if link in self.visited:        
                    continue
                else:                   
                    self.visited.add(link)            
                    #info = self.extract_info(link)
                    if 'mailto' not in link:                        
                        if self.samesite:
                            #self_url = f"{self.url_data.scheme}://{self.url_data.netloc}"
                            #if link.startswith(self_url):
                            if self.is_same_site(link):
                                if self.showlinks:
                                    print(link)
                                self.links_found += 1
                                self.crawl(link, current_depth +1)
                                # crawl parent paths as well
                                u = urlpath(link)
                                if u.depth > 1:
                                    self.crawl(u.parent,0)
                        else:
                            if self.showlinks:
                                print(link)
                            self.links_found += 1
                            self.crawl(link, current_depth +1)
                            # crawl parent paths as well
                            u = urlpath(link)
                            if u.depth > 1:
                                self.crawl(u.parent,0)                            
                        
                        
                        
            
    def is_same_site(self,link):
        self_url = f"{self.url_data.scheme}://{self.url_data.netloc}"
        if link.startswith(self_url):
            return True
        else:
            return False
        
    def start(self):                     
        self.crawl(self.starting_url)  


    




class cookie_parser():
    def __init__(self):
        self.cookies = {}
    def parse(self,cookie_string):
        # check if more cokie is given
        if ';' in cookie_string:
            cookies = cookie_string.split(';') # split them in ; character
        else:
            cookies = cookie_string.rsplit(' ').lsplit(' ') # thim the trailing and the starting spaces
        for c in cookies:
            cookie = c.split('=')
            self.cookies.update({cookie[0]:cookie[1]})
        return self.cookies
    
class urlpath():
    def __init__(self,url=''):
        if url != '':
            self.url = url
            self.current = ""
            self.protocol = self._get_protocol()
            self.parent = self._get_parent()
            self.depth = self._get_url_depth()
            self.param_string = self._get_params()
            self.parameters = {}
            self._extract_parameters()
                   
    def _get_protocol(self):
        if self.url.startswith('https://'):
            return 'https://'
        elif self.url.startswith('http://'):
            return 'http://'
        else:
            pattern = r'[a-z]+://'
            m = re.search(pattern,self.url,re.I)
            if m:
                return str(m)
            else: 
                return ""
    def _get_parent(self):
        uri = self.url.replace(self.protocol,'')
        if '/' in uri:
            parent = uri.rsplit('/',1)
            if len(parent) == 2:
                self.current = parent[1]
                return self.protocol+parent[0]
            else:
                return uri
        else:
            return uri
        
    def _get_url_depth(self):
        uri = self.url.replace(self.protocol,'')
        paths = uri.split('/')
        return len(paths)
        
    def _get_params(self):
        pattern = r'\?([\w=&]+)'
        m = re.search(pattern,self.url,re.I)
        if m:
            return m.group(1)
        else:
            return ""
        
    def _extract_parameters(self):
        if self.param_string:
            par = self.param_string.split('&')
            for p in par:
                pv = p.split('=')
                if len(pv) == 2:
                    self.parameters.update({pv[0]:pv[1]})
            
    def get_parent_path(self,url):
        self.url = url
        self.current = ""
        self.protocol = self._get_protocol()
        self.parent = self._get_parent()
        return self.protocol+self.parent
        




"""
u = urlpath('http://google.com/uploads/file/valamifile.php?var1=val1&var2=val2')
print(u.parent)
"""