#!/usr/bin/env python3
from terminaltables import AsciiTable

class HelpMenu():
    def __init__(self):
        self.menuItems = []
        self.headers = []
        self.title = ""
        self.underline_title = True
        self.outer_border = False
        self.inner_row_border = False
        self.inner_column_border = False
        self.inner_heading_row_border = False
    def add_header(self,*argv):
        for arg in argv:
            self.headers.append(arg)
    def add_item(self,*args):
        itm = []
        for arg in args:
            itm.append(str(arg))
        self.menuItems.append(itm)
    def print_help(self):
        table_data = []
        table_data.append(self.headers)
        for i in self.menuItems:
            table_data.append(i)
        table = AsciiTable(table_data)
        table.outer_border = self.outer_border
        table.inner_row_border = self.inner_row_border
        table.inner_column_border = self.inner_column_border
        table.inner_heading_row_border = self.inner_heading_row_border
        if self.title != "":
            if self.underline_title: self.__set_title_underline()
            print('\n'+self.title)
        print(table.table)
        print('')
    def __set_title_underline(self):
        title_length = len(self.title)
        self.title += "\n"+('-'*title_length)
        


    
