# -*- coding: utf-8 -*-
"""
Created on Thu May 14 19:31:52 2020

@author: terry
"""


import os
from deckClass import Deck
from playerClass import Player
from PokerTableClass import table

if __name__ == "__main__":
    print("TEST TEST TEST")
    
    p1 = Player(100, "p1")
    p2 = Player(100, "p2")
    p3 = Player(100, "p3")
    p4 = Player(100, "p4")
    p5 = Player(100, "p5")
    p6 = Player(100, "p6")
    
    aTable = table()
    aTable.setMaxGames(1000)
    
    aTable.addPlayer(p1)
    aTable.addPlayer(p2)
    aTable.addPlayer(p3)
    aTable.addPlayer(p4)
    aTable.addPlayer(p5)
    aTable.addPlayer(p6)
    
    print("Table Setted up with Six dummy player")
    print("Number of Players " + str(aTable.getNPlayer()))
    print("Number of Active Players " + str(aTable.getNPlayer_active()))
    print("Number of inGame Players " + str(aTable.getNPlayer_inGame()))
    
    aTable.runGame()
    