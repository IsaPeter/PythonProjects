#!/usr/bin/env python3
import crawler
import argparse,sys


url = ""
depth = 3
same_site = True
regex_pattern = ""
verbose = False
extensions = []
deep_crawl = False
ignore_robots = False


def parse_arguments():
    global url,depth,same_site,regex_pattern,verbose,extensions,deep_crawl,ignore_robots
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--url',dest='url',help='The crawling URL')
    parser.add_argument('-d','--depth',dest='depth',help='The depth of the crawl')
    parser.add_argument('-s','--same-site',dest="samesite",action='store_true',help='The crawl stay on site')
    parser.add_argument('-a','--all-site',dest="allsite",action='store_true',help='The crawl go to other sites too')    
    parser.add_argument('-v','--verbose',dest="verbose",action='store_true',help='Verbose output')
    parser.add_argument('-R','--regex',dest='regex',help='Extract data with regex')
    parser.add_argument('-e','--extension',dest='extension',help='Set the extension')
    parser.add_argument('-D','--deep-crawl',dest="deepcrawl",action='store_true',help='Set the deep crawl method')
    parser.add_argument('--ignore-robots',dest="ignorerobots",action='store_true',help='Ignore robots.txt')
    
    
    args = parser.parse_args()

    if args.samesite and args.allsite: 
        print("Error. Choose one only, Same site (-s) or All site (-a)")
        sys.exit(1)
    if args.url: url = args.url
    if args.depth: depth = int(args.depth)
    if args.samesite: same_site = True
    if args.allsite: same_site = False
    if args.verbose: verbose = True
    if args.regex: regex_pattern = str(args.regex)
    if args.deepcrawl: deep_crawl = True
    if args.ignorerobots: ignore_robots = True
    if args.extension:
        if "," in args.extension:
            extensions = args.extension.split(',')
        else:
            extensions.append(args.extension)
    
def extract_data(links):
    pass


def main():
    global url,depth,same_site,regex_pattern,verbose,extensions
    parse_arguments()
    crawler = crawler.PyCrawler(url)    # create an object and pass an url to it
    crawler.samesite = same_site    # set the same site
    crawler.depth = depth   # set the depth
    crawler.start() # start the crawler
    
    extract_data(crawler.get_all_links())

if __name__ == '__main__':
    main()