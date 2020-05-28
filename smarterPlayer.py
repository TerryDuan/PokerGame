# -*- coding: utf-8 -*-
"""
Created on Mon May 18 18:00:57 2020

@author: terry
"""


from playerClass import Player
import TexasHoldemCalculators as calc

class smarterPlayer(Player):
    
    
    def action(self, chipsToCall : int, thisGameActions : dict):
        """
        Position based strategy, Fixed range
        """
        
        nChip = self._getCurrentStack(thisGameActions)
        
        if thisGameActions['Street'].upper() == 'PREFLOP':
            if self.position == 0:
                #Never play SB
                return 'FOLD' , 0
            elif self.position == 1:
                if (((self.hand[0] - self.hand[1]) == 0) & (chipsToCall == 0) & (nChip > thisGameActions['Pot'])):
                    #has pairs and no one raised or bet
                    return 'BET', thisGameActions['Pot']
                elif nChip > chipsToCall:
                    return 'CALL' , chipsToCall
                else:
                    return 'FOLD' , 0
            elif self.position == 2:
                if ((self.hand[0] - self.hand[1] == 0) & (chipsToCall < thisGameActions['Pot']) & (self.hand[0].rank == '1' or self.hand[0].rank == 'K')):
                    return 'BET', thisGameActions['Pot']*2
                else:
                    return 'CALL', chipsToCall
            elif chipsToCall < nChip:
                nChip = nChip - chipsToCall
                return 'CALL', chipsToCall
            else:
                return 'FOLD' , 0
        else:
            community_card = []
            community_card = thisGameActions['CommunityCards']['Flop'] + thisGameActions['CommunityCards']['Turn'] + thisGameActions['CommunityCards']['River']
            community_card.append(self.hand[0])
            community_card.append(self.hand[1])
            comboRank, Combo = calc.find_best_combo(community_card)
            #run find bestCombo, if better than two pairs, raise/bet
            if ((comboRank < 8)&(chipsToCall == 0)):
                return 'BET', thisGameActions['Pot']
            elif ((comboRank < 7)&(chipsToCall > 0)):
                if chipsToCall*3 < nChip:
                    return 'RAISE', chipsToCall*3
                else:
                    return 'ALL IN', nChip
            elif (comboRank < 8):
                if chipsToCall < nChip:
                    return 'CALL', chipsToCall
                else:
                    return 'FOLD', 0
            else:
                return 'FOLD', 0