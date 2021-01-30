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
    
    def get_html(self, url):    
        try:    
            html = requests.get(url)    
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
        li = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html)    
        for i, link in enumerate(li): 
            if not urlparse(link).netloc:
                if base.endswith("/") and link.startswith("/"):
                    link_with_base = urljoin(base.rstrip("/"),link)
                else:
                    link_with_base = urljoin(base,link)
                li[i] = link_with_base
                self.links.append(link)
        
        for s in self.get_src(html,base):
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
                        else:
                            if self.showlinks:
                                print(link)
                            self.links_found += 1
                            self.crawl(link, current_depth +1)
            
    def is_same_site(self,link):
        self_url = f"{self.url_data.scheme}://{self.url_data.netloc}"
        if link.startswith(self_url):
            return True
        else:
            return False
        
    def start(self):                     
        self.crawl(self.starting_url)  



if __name__ == '__main__':
    crawler = PyCrawler('https://pymotw.com/2/urlparse/')
    crawler.showlinks = True
    crawler.start()
    print(f"Found Links: {str(crawler.links_found)}")
    print(crawler.sources)