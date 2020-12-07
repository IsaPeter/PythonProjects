#!/usr/bin/env python3
import urllib.parse
import sys

in_string = sys.stdin

for line in in_string:
    print(urllib.parse.unquote(line.rstrip()))
