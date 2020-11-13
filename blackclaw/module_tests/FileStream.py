#!/usr/bin/env python3
"""
File Stream Object to handle File reading and writing
"""
import os,sys


class FileStream:
    def __init__(self,filename = '',mode = 'r'):
        if filename != '':
            self.filename = filename
            self.path = os.path.basename(filename)
            self.file_size = os.path.getsize(filename)
        self.mode = mode
        self.current_position = 0
        self.buffer_length = 100 # 100 bytes
        self.__fs = None
        

    def open(self,filename='',mode='r'):
            try:
                if filename != '':
                    self.filename = filename
                    self.path = os.path.basename(filename)
                    self.file_size = os.path.getsize(self.filename)
                if mode != '':
                    self.mode = mode
                self.__fs = open(self.filename,self.mode)
            except Exception as x:
                print(x)
                
    def seek(self,position):
        if self.__fs.seekable():
            self.__fs.seek(position)
            self.current_position = self.__fs.tell()

    def read_range(self,start,end):
            try:
                if not self.__fs.readable():
                    raise Exception("The File stream cannot be readable")
                if end < start or end < 0:
                    raise Exception("The end number need to greater than 0 and the start number.")
                if end == start:
                    if end < self.file_size:
                        self.__fs.seek(end)
                        return self.__fs.read(1)
                    else:
                        end = self.file_size
                        self.__fs.seek(end)
                        return self.__fs.read(1)
                if start < 0:
                    raise Exception("Invalid start number. The start number need to be greater than -1.")
                else:
                    self.__fs.seek(start)
                    if end - start > self.file_size:
                        end = self.file_size
                    size = end - start
                    return self.__fs.read(size)
            except Exception as x:
                print(x)
                
    def readnum(self,num):
            try:
                if not self.__fs.readable():
                    raise Exception("The File stream cannot be readable")
                
                a = self.file_size - (self.current_position + num)
                if a > -1:
                    return self.__fs.read(num)
                else:
                    num = self.file_size - self.current_position
                    return self.__fs.read(num)
                
                self.seek(self.current_position+num)
            except Exception as x:
                print(x)
    def read(self):
            try:
                if not self.__fs.readable():
                    raise Exception("The File stream cannot be readable")
                
                a = self.file_size - (self.current_position + self.buffer_length)
                if a > -1:
                    return self.__fs.read(self.buffer_length)
                else:
                    self.buffer_length =  self.file_size - self.current_position
                    return self.__fs.read(self.buffer_length)
                self.seek(self.current_position+self.buffer_length)
            except Exception as x:
                print(x)
    def write(self,data):
            try:
                if not self.__fs.writable():
                    raise Exception("The File stream cannot be writeable.")
                
                self.__fs.write(data)
            except Exception as x:
                print(x)

    def close(self):
        if not self.__fs.closed():
            self.__fs.close()
    def read_all_bytes(self):
        try:
            if 'b' in self.__fs.mode:
                return self.__fs.read()
            else:
                raise Exception("File Stream mode need to be binary.")
            return b""
        except Exception as x:
            print(x)
    def read_all_text(self):
        try:
            if 'b' not in self.__fs.mode:
                return self.__fs.read()
            else:
                raise Exception("Binary mode doesn't allowed in text mode.")
            return ""
        except Exception as x:
            print(x)        
    def read_all_lines(self):
        try:
            if 'r' == self.__fs.mode:
                return self.__fs.readlines()
        except Exception as x:
            print(x)        
            