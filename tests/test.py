# -*- coding: utf-8 -*-
"""
Created on Thu May 14 19:31:52 2020

@author: terry
"""


import os
import sys
sys.path.append("..")
from deckClass import Deck
from playerClass import Player
from smarterPlayer import smarterPlayer
from interactivePlayer import interactivePlayer
from PokerTableClass import table

if __name__ == "__main__":
    print("TEST TEST TEST")
    
    p1 = Player("p1")
    p2 = Player("p2")
    p3 = Player("p3")
    p4 = Player("p4")
    p5 = Player("ip5")
    p6 = smarterPlayer("sp6")
    
    aTable = table()
    aTable.setMaxGames(1000)
    
    aTable.addPlayer(p1,100)
    aTable.addPlayer(p2,100)
    aTable.addPlayer(p3,100)
    aTable.addPlayer(p4,100)
    aTable.addPlayer(p5,100)
    aTable.addPlayer(p6,100)
    
    print("Table Setted up with Six dummy player")
    print("Number of Players " + str(aTable.getNPlayer()))
    print("Number of Active Players " + str(aTable.getNPlayer_active()))
    print("Number of inGame Players " + str(aTable.getNPlayer_inGame()))
    
    aTable.runGame()
    