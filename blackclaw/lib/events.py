#!/usr/bin/env python

class EventHook(object):

    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self

    def fire(self, *args, **keywargs):
        for handler in self.__handlers:
            handler(*args, **keywargs)

    def clearObjectHandlers(self, inObject):
        for theHandler in self.__handlers:
            if theHandler.im_self == inObject:
                self -= theHandler
                
                
class pyEvent():
    def __init__(self):
        self.onChanged = EventHook()
        self.onFinished = EventHook()
    



"""  
class clild_obj:
    def __init__(self):
        self.counter = 0
        self.events = pyEvent()
        
    def run(self):
        import time
        while self.counter < 10:
            self.counter += 1
            self.events.onChange.fire(self.counter)
            time.sleep(1)
        self.events.onFinished.fire()


class parent_class:
    def __init__(self):
        self.obj = clild_obj()
    def start(self):
        self.obj.events.onChange += self.counter_changed
        self.obj.events.onFinished += self.counter_finished
        self.obj.run()
    def counter_changed(self,cnt):
        print("Parent: counter changed: "+str(cnt))
    def counter_finished(self):
        print("The counter is finished: "+str(self.obj.counter))



p = parent_class()
p.start()
"""