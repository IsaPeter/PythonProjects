#!/usr/bin/env python3
import os
"""
fs = open('alphabet','r')
size = os.path.getsize('alphabet')
buffer_length = 5
buffer = []
position = 0
data = ""
while position < size:
    if position + buffer_length <= size:
        buffer = fs.read(buffer_length)
    else:
        buffer_length = (position + buffer_length) - size
        buffer = fs.read(buffer_length)
    data += buffer
    position = position + buffer_length
    fs.seek(position)
    print(fs.tell())

print(data)
"""
from FileStream import FileStream

fs = FileStream('almafa')
fs.open(mode='w')
fs.write('alma')

