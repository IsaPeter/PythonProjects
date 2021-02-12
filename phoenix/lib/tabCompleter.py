import os
import sys 
import readline
import glob

class tabCompleter(object):
    def __init__(self):
        self.wordList = []
    """ 
    A tab completer that can either complete from
    the filesystem or from a list.
    
    Partially taken from:
    http://stackoverflow.com/questions/5637124/tab-completion-in-pythons-raw-input
    """

    def pathCompleter(self,text,state):
        """ 
        This is the tab completer for systems paths.
        Only tested on *nix systems
        """
        line   = readline.get_line_buffer().split()

        return [x for x in glob.glob(text+'*')][state]

    
    def createListCompleter(self,ll):
        """ 
        This is a closure that creates a method that autocompletes from
        the given list.
        
        Since the autocomplete function can't be given a list to complete from
        a closure is used to create the listCompleter function with a list to complete
        from.
        """
        self.wordList = ll
        def listCompleter(text,state):
            line   = readline.get_line_buffer()
            
            if not line:
                return [c + " " for c in self.wordList][state]

            else:
                words = line.split(' ')
                wl = len(words)
                last_word = words[wl-1]                
                tab_word = [c + " " for c in self.wordList if c.startswith(last_word)][state]
                line = line.replace(last_word,tab_word)
                return line
    
        self.listCompleter = listCompleter

"""
if __name__=="__main__":
    t = tabCompleter()
    t.createListCompleter(["ab","aa","bcd","bdf"])

    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")

    readline.set_completer(t.listCompleter)

    ans = input("Complete from list ")
    print(ans)
    
    readline.set_completer(t.pathCompleter)
    ans = input("What file do you want? ")
    print(ans)
"""