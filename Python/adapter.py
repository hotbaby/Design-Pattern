# -*- coding: utf-8 -*-

import logging

_logger = logging.getLogger(__name__)


class Computer(object):
    
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return 'the {} computer'.format(self.name)
    
    def excute(self):
        return 'excute a program'


class Synthesizer(object):
    
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return 'the {} synthesizer'.format(self.name)
    
    def play(self):
        return 'is playing an electronic song'


class Human(object):
    
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return  '{} the human'.format(self.name)
    
    def speak(self):
        return 'say hello'


class Adapter(object):
    
    def __init__(self, obj, adapted_methods):
        self.obj = obj
        self.__dict__.update(adapted_methods)
        
    def __str__(self):
        return str(self.obj)
    

def main():
    objs = [Computer('Asus')]
    synth = Synthesizer('moog')
    human = Human('Bob')
    objs.append(Adapter(synth, excute=synth.play))
    objs.append(Adapter(human, excute=human.speak))
    
    for obj in objs:
        _logger.info('{} {}'.format(str(obj), obj.excute()))