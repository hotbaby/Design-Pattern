'''
Created on Sep 18, 2016

@author: yy
'''

import logging
from enum import Enum
from __main__ import time

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

STEP_DELAY = 1

PizzaProgress = Enum('queued', 'preparation', 'baking', 'ready')
PizzaDough = Enum('thin','thick')
PizzaSauce = Enum('tomato', 'creme_fraiche')
PizzaTopping = Enum('mozzarella', 'double_mozzarella', 'bacon', 'ham', 'mushrooms', 'red_onion', 'oregano')


class Pizza(object):
    
    def __init__(self, name):
        self.name = name
        self.dough = None
        self.sauce = None
        self.topping = []
        
    def __str__(self):
        return self.name
    
    def prepare_dough(self, dough):
        self.dough = dough
        _logger.debug('Preparing the {} dough'.format(self.dough.name))


class MargaritaBuilder(object):
    
    def __init__(self):
        self.pizza = Pizza('mrgarita')
        self.process = '' #TODO
        self.baking_time = 5
        
    def prepare_dough(self):
        self.progress = PizzaProgress.preparation
        self.pizza.prepare_dough(PizzaDough.thin)
        
    def add_sauce(self):
        self.pizza.sauce = PizzaSauce.tomato
        
    def add_topping(self):
        self.pizza.topping.append([i for i in (PizzaTopping.double_mozzarella, PizzaTopping.oregano)])
        
    def bake(self):
        self.progress = PizzaProgress.baking
        _logger.debug('baking your magarita for {} seconds'.format(self.baking_time))
        time.sleep(self.baking_time)
        self.progress = PizzaProgress.ready
        _logger.debug('your margarita is ready')
        
class CreamyBaconBuilder(object):
    
    def __init__(self):
        self.pizza = Pizza('creamy bacon')
        self.progress = PizzaProgress.queued
        self.baking_time = 7
        
    def prepare_dough(self):
        self.progress = PizzaProgress.preparation
        self.pizza.prepare_dough(PizzaDough.thick)
        
    def add_sauce(self):
        _logger.debug('adding the creme fraiche sauce to your creamy bacon')
        self.pizza.sauce = PizzaSauce.creme_fraiche
        time.sleep(STEP_DELAY)
        _logger.debug('done with the creme fraiche sauce')
        
    def add_topping(self):
        _logger.debug('add the topping to your creamy bacon')
        self.pizza.topping.append([t for t in (PizzaTopping.mozzarella, PizzaTopping.bacon,
                                               PizzaTopping.ham, PizzaTopping.mushrooms,
                                               PizzaTopping.red_onion, PizzaTopping.oregano)])
        time.sleep(STEP_DELAY)
        _logger.debug('done with the topping')
    
    def bake(self):
        self.progress = PizzaProgress.baking
        _logger.debug('baking your creamy bacon for {} seconds'.format(self.baking_time))
        time.sleep(self.baking_time)
        self.progress = PizzaProgress.ready
        _logger.debug('your creamy bacon is ready')
        

'''
The director in this example is the waiter. The core of the Waiter class is the 
custruct_pizza() method, which accepts a builder as a parameter and excutes all
the pizza preparation steps in the right order.
'''
class Waiter(object):
    
    def __init__(self):
        self.builder = None
        
    def construct_pizza(self, builder):
        self.builder = builder
        [step() for step in (builder.prepare_dough, builder.add_sauce,
                             builder.add_topping, builder.bake)]
    
    @property
    def pizza(self):
        return self.builder.pizza
    

def validate_style(builders):
    try:
        pizza_style = input('What pizza would you like , [m]argarita or [c]remay bacon?')
        builder = builders[pizza_style]()
    except KeyError as exc:
        _logger.exception(exc)
        return (False, None)
    return (True, builder)

def main():
    builders = dict(m=MargaritaBuilder, c=CreamyBaconBuilder)
    valid_input=False
    while not valid_input:
        valid_input, builder = validate_style(builders)
    waiter = Waiter()
    waiter.construct_pizza(builder)
    pizza =waiter.pizza
    _logger.debug('Enjoy your {}!'.format(pizza))
