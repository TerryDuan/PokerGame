# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 23:33:39 2020

@author: terry
"""
from playerClass import Player

class table():
    
    def __init__(self):
        self.buttomPosition = 0
        self.PlayersList = [] #can it contains both parent class and child class?
        self.pot = 0
        self.bb = 2
        self.sb = 1
        self._tempPosition = -2

    def addPlayer(self, newPlayer : Player):
        self.PlayerList.append((newPlayer, self._tempPosition))
        self._tempPosition = self._tempPosition + 1
        
    def getPot(self):
        return self.pot
    
    def getNPlayer(self):
        return len(self.PlayerList)