# -*- coding: utf-8 -*-
"""
Created on Mon May 18 18:00:57 2020

@author: terry
"""


from playerClass import Player

class smarterPlayer(Player):
    
    
    def action(self, chipsToCall : int, thisGameActions : dict):
        """
        Position based strategy, Fixed range
        """
        if thisGameActions['Street'].upper() == 'PREFLOP':
            if self.position == 0:
                #Never play SB
                return 'FOLD' , 0
            elif self.position == 1:
                if ((self.hand[0] - self.hand[1] == 0) & (chipsToCall == 0) & self.nChip > thisGameActions['Pot']):
                    #has pairs and no one raised or bet
                    self.nChip = self.nChip - thisGameActions['Pot']
                    return 'BET', thisGameActions['Pot']
                elif self.nChip > chipsToCall:
                    self.nChip = self.nChip - chipsToCall
                    return 'CALL' , chipsToCall
                else:
                    return 'FOLD' , 0
            elif self.position == 2:
                if ((self.hand[0] - self.hand[1] == 0) & (chipsToCall < thisGameActions['Pot']) & (self.hand[0].rank == '1' or self.hand[0].rank == 'K')):
                    return 'BET', thisGameActions['Pot']*2
                else:
                    return 'CALL', chipsToCall
            elif chipsToCall < self.nChip:
                self.nChip = self.nChip - chipsToCall
                return 'CALL', chipsToCall
            else:
                self.endGame(0)
                return 'FOLD' , 0
        else:
            pass
            #run find bestCombo, if better than two pairs, raise/bet