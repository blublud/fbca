'''
Created on Mar 17, 2013

@author: fan wei fang
'''
import logging

class LoggerWriter:
    
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
    
    def write(self, msg):
        if msg != '\n':
            self.logger.log(self.level, msg)
