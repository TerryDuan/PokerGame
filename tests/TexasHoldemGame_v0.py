# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:29:42 2020

@author: terry

Main Function

"""

import os
from deckClass import Deck
from playerClass import player
from PokerTableClass import table


if __name__ == "__main__":
    print('hello player')
    print('setting up a new table ...')
    thisTable = table()
    
    nPlayers = input('how many players ? ')
    