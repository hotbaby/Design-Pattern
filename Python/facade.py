# -*- coding: utf-8 -*-

import logging
from enum import Enum
from abc import ABCMeta, abstractmethod

_logger = logging.getLogger(__name__)
State = Enum('new', 'running', 'sleeping', 'restart', 'zombie')


class Server(object):
    __metaclass__ = ABCMeta

    def _init__(self):
        pass
    
    def __str__(self):
        return self.name
    
    @abstractmethod
    def boot(self):
        pass
    
    @abstractmethod
    def kill(self, restart=True):
        pass


class FileServer(Server):
    
    def __init__(self):
        self.name = 'FileServer'
        self.state = State.new
        
    def boot(self):
        self.state = State.running
        
    def kill(self, restart=True):
        self.state = State.restart if restart else State.zombie
        
    def create_file(self, user, name, perssions):
        _logger.info('Try to create file {} for user {}' 
                     'with perssions {}'.format(name, user, perssions))


class ProcessServer(Server):
    
    def __init__(self):
        self.name = 'ProcessServer'
        self.state = State.new
        
    def boot(self):
        self.state = State.running
        
    def kill(self, restart=True):
        self.state = State.restart if restart else State.zombie
        
    def create_process(self, user, name):
        _logger.info('Try to create the process {} for user {}'.format(name, user))


class WindowServer(Server):
    pass


class NetworkServer(Server):
    pass


class OperatingSystem(object):
    '''The Facade'''
    
    def __init__(self):
        self.fs = FileServer()
        self.ps = ProcessServer()
    
    def start(self):
        [i.boot() for i in (self.fs, self.ps)]
        
    def create_file(self, user, name, permissions):
        return self.fs.create_file(user, name, permissions)
    
    def create_process(self, user,name):
        return self.ps.create_process(user, name)
    

def main():
    os = OperatingSystem()
    os.start()
    os.create_file('foo', 'hello', '-rw-r-r')
    os.create_process('bar', 'ls /tmp')
    
if __name__ == '__main__':
    main()
