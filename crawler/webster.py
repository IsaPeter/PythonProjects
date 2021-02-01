#!/usr/bin/env python3
import crawler
import argparse,sys
from robotsextractor import robotsextractor


url = ""
depth = 3
same_site = True
regex_pattern = ""
verbose = False
extensions = []
deep_crawl = False
ignore_robots = False
extract_data = False
output_file=""
grepable_output_file= ""
crawl_robots= False
check_robots = False



def parse_arguments():
    global url,depth,same_site,regex_pattern,verbose,extensions,deep_crawl,ignore_robots,extract_data, output_file,crawl_robots,check_robots, grepable_output_file
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--url',dest='url',help='The crawling URL')
    parser.add_argument('-d','--depth',dest='depth',help='The depth of the crawl')
    parser.add_argument('-s','--same-site',dest="samesite",action='store_true',help='The crawl stay on site')
    parser.add_argument('-a','--all-site',dest="allsite",action='store_true',help='The crawl go to other sites too')    
    parser.add_argument('-v','--verbose',dest="verbose",action='store_true',help='Verbose output')
    parser.add_argument('-R','--regex',dest='regex',help='Extract data with regex')
    parser.add_argument('-e','--extension',dest='extension',help='Set the extension')
    parser.add_argument('-D','--deep-crawl',dest="deepcrawl",action='store_true',help='Set the deep crawl method')
    parser.add_argument('-E','--extract-data',dest='extractdata',action='store_true',help='Extract data from sources')
    parser.add_argument('-oN','--normal-output',dest='normaloutput',help='Write Normal result into file')
    parser.add_argument('-oG','--grepable-output',dest='grepableoutput',help='Write Grepable result into file')
    parser.add_argument('--crawl-robots',dest='crawlrobots',action='store_true',help='Crawling the robots file')
    parser.add_argument('--check-robots',dest='checkrobots',action='store_true',help='Checking the existence of the robots file')
    parser.add_argument('--extract-forms',dest='extractforms',action='store_true',help='Extracting Forms')
    
    
    args = parser.parse_args()

    if args.samesite and args.allsite: 
        print("Error. Choose one only, Same site (-s) or All site (-a)")
        sys.exit(1)
    if args.url: url = args.url
    if args.depth: depth = int(args.depth)
    if args.samesite: same_site = True
    if args.crawlrobots: crawl_robots = args.crawlrobots
    if args.checkrobots: check_robots = args.checkrobots
    if args.allsite: same_site = False
    if args.verbose: verbose = True
    if args.regex: regex_pattern = str(args.regex)
    if args.deepcrawl: deep_crawl = True
    if args.ignorerobots: ignore_robots = True
    if args.extractdata: extract_data = True
    if args.normaloutput: output_file = args.normaloutput
    if args.grepableoutput: grepable_output_file = args.grepableoutput
    if args.extension:
        if "," in args.extension:
            extensions = args.extension.split(',')
        else:
            extensions.append(args.extension)
    
def extract_data(links):
    pass

def deep_crawl_uris(uris,cr):
    for u in uris:
        try:
            cr.crawl(u,depth=cr.crawl_depth)
        except Exception as x:
            print(x)
def write_normal_output(fname,cr):
    with open(fname,'w') as no:
        for l in cr.get_all_links():
            no.write(l)
def write_greppable_output(fname,cr):
    with open(fname,'w') as no:
        for l in cr.links:
            no.write("HREF\t"+l)
        for s in cr.sources:
            no.write("SRC\t"+l)
            
def main():
    global url,depth,same_site,regex_pattern,verbose,extensions,extract_data,deep_crawl,check_robots,crawl_robots
    parse_arguments()
    c = crawler.PyCrawler(url)    # create an object and pass an url to it
    c.samesite = same_site    # set the same site
    c.depth = depth   # set the depth
    c.start() # start the crawler
    
    if check_robots:
        r = robotsextractor(url)
        r.check()
    if crawl_robots:
        r = robotsextractor(url)
        r.extract()
        c.links.append(r.get_links())
        
    if deep_crawl:
        deep_crawl_uris(c.get_all_links()) # perform a deep crawling
        
    
    if extract_data:
        extract_data(c.get_all_links()) # Get all links and extract the desired data

if __name__ == '__main__':
    main()
