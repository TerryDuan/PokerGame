# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 23:33:39 2020

Table class is used to track and drive the game
pot: pot for each game, reset to zero after each game, give pot to winner by player.endGame()
PlayersList: list to store players, [SB, BB, UTG, UTG+1, HJ, CO, BTN], Player at position 0 will be moved to end of list as new BTN

while not end:
    0. Create/Shuffle the deck
    1. check if enough active player, else BREAK
    2. call startGame() on each players in the list, from 0 to END, pass hands and position to each player(agent)
    3. while no winner or before MAX_ITERATION:
        (if street == PreFlop, start from position 2, else start from position 0)
        3a. call player_i.action(), pass through latest updated thisGameActions{}
        3b. update returned tuple into thisGameActions{}
        3c. update table.pot
        3d. if all players checks/called, move to next street, or call find_winner()
        3e. if player is out and inactive, remove it from the playersList
        

@author: terry
"""
from playerClass import Player
from deckClass import Deck
import TexasHoldemCalculators_v0 as calc
import numpy as np

class table():
    
    def __init__(self):
        self.buttomPosition = 0
        self.PlayersList = [] 
        self.pot = 0
        self.bb = 2
        self.sb = 1
        self.MAX_ITERATION = 50

    def addPlayer(self, newPlayer : Player):
        self.PlayersList.append(newPlayer)
        
    def getPot(self):
        return self.pot
    
    def getNPlayer(self):
        return len(self.PlayerList)
    
    def getNPlayer_active(self):
        n = 0
        for plyr in self.PlayersList:
            if plyr.isActive():
                n = n + 1
        
        return n
    
    def getNPlayer_inGame(self):
        n = 0
        for plyr in self.PlayersList:
            if plyr[0].isInGame():
                n = n + 1
        
        return n
    
    def setBlinds(self, bb : int):
        self.bb = bb
        self.sb = int(bb/2)
        
    def setMaxGames(self, maxGames : int):
        self.MAX_ITERATION = maxGames
    
    def _prepareGame(self,thisGameActions,  theDeck, currentSB):
        """
        Go through all players in PlayersList, starting from index: currentSB, keep i++, i as position Code
        for Active Player, dealt two cards, assign i, i++
        else skip
        return the index of currentSB, no change, if currentSB is still Active, else return new currentSB for current Game

        Parameters
        ----------
        thisGameActions
            Action history to store initial bet, SB BB Straddle etc.
        theDeck : deck TYPE
            theDeck is used to dealt cards.
        currentSB : int TYPE
            index of current SB player in the PlayersList .

        Returns
        -------
        new currentSB

        """
        
        nAllPlayers = len(self.PlayersList)
        nActivePlayers = self.getNPlayer_active()
        positionCode = 0
        PlayersIndex = currentSB
        tempBetHistory = [np.nan]*nAllPlayers
        
        while(positionCode < (nActivePlayers - 1)):

            if self.PlayersList[PlayersIndex].isActive():
                #it's still active
                
                #this player is active, prepare required blinds, store currentSB if it's SB
                if positionCode == 0:
                #if we just assing SB player, update new currentSB for return
                    currentSB = PlayersIndex
                    tempBetHistory[PlayersIndex] = self.sb
                    price2play = self.sb
                elif positionCode == 1:
                    tempBetHistory[PlayersIndex] = self.bb
                    price2play = self.bb
                else:
                    price2play = 0
                
                #prepare hands
                hand = []
                hand.append(theDeck.dealt())
                hand.append(theDeck.dealt())        
                
                #ACTIVATE the Player
                initBet = self.PlayersList[PlayersIndex].startGame(hand, positionCode, price2play)
                #Add bet to Pot (sb, bb, sttradle)
                thisGameActions['Pot'] = self.pot + initBet
                self.pot = self.pot + initBet
                
                # Move to next position, and the next player
                positionCode = positionCode + 1
                PlayersIndex = PlayersIndex + 1
                if PlayersIndex == nAllPlayers:
                    PlayersIndex = 0
            else:
                #it's no longer active, need to move to next Player
                PlayersIndex = PlayersIndex + 1
                if PlayersIndex == nAllPlayers:
                    PlayersIndex = 0
        
        #store initial bet
        thisGameActions['BetHistory']['PreFlop'] = tempBetHistory
        return currentSB
                

    
    
    def _runCurrentStreet(self, thisGameActions,theDeck, currentSB : int):
        """
        int maxBet, max of bet in current street
        int[] currentBets, from thisGameAvtion[betHistory]
        startPosition = SB + 2 for Preflop or SB for else
        playerIndex = keep track of which 
        
        Dealt cards for this street
        record them to thisGameActions
        
        While Loop
            End and Break if min(currentBets) == maxBet and playerIndex == startPosition
            
            check pastBet in currentBets, calculate price to pay
            call Player's action() at playerIndex
            update self.pot
            record action to thisGameActions
            move to next playerIndex
            update startPosition and maxBet if there is a raise
        
        If game end
            Determine winner and pay winner
        
        Parameters
        ----------
        thisGameActions : dict
            History of Actions so far in this Game.
        theDeck : deck Class
            Deck to dealt card
        currentSB : int
            currentSB.

        Returns
        -------
        boolean
            Default as False for PreFlop, Flop, Turn.
            True if River, or Only one Player inGame == True

        """
        # Initialize variables:
        
        isGameEnded = False
        
        if thisGameActions['Street'] == 'PreFlop':
            startPosition = (currentSB + 2)%len(self.PlayersList)
            playerIndex = startPosition
            maxBet = self.bb 
        elif thisGameActions['Street'] == 'Flop':
            startPosition = currentSB
            playerIndex = startPosition
            maxBet = 0
            cards = []
            cards.append(theDeck.dealt)
            cards.append(theDeck.dealt)
            cards.append(theDeck.dealt)
            thisGameActions['CommunityCards'][thisGameActions['Street']] = cards            
        else:
            startPosition = currentSB
            playerIndex = startPosition
            maxBet = 0
            cards = []
            cards.append(theDeck.dealt)
            thisGameActions['CommunityCards'][thisGameActions['Street']] = cards
        
        
        # Start the Loop over all Players
        while True:
            
            if ((min(thisGameActions['BetHistory'][thisGameActions['Street']]) == maxBet) and (playerIndex == startPosition)):
                #END Condition
                #TODO: Need check if the game is ended due to all Folded
                
                if thisGameActions['Street'] == 'River':
                    isGameEnded = True
                elif self.getNPlayer_inGame() == 1:
                    isGameEnded = True
                
                break
            
            
            pastBet = thisGameActions['BetHistory'][thisGameActions['Street']][playerIndex]
            if ((self.PlayersList[playerIndex].isActive()) and (self.PlayersList[playerIndex].isInGame()) and ((pastBet < maxBet) or (pastBet == np.nan))):
                
                action, bet = self.PlayersList[playerIndex].action(np.where(pastBet == np.nan, maxBet, maxBet - pastBet), thisGameActions)
                maxBet = max(maxBet, bet) #update maxBet
                
                #record actions,BetHistory,Pot
                thisGameActions['BetHistory'][thisGameActions['Street']][playerIndex] = np.where(pastBet == np.nan, 0, pastBet) + bet
                thisGameActions['Actions'][thisGameActions['Street'].append((self.PlayersList[playerIndex].playerName,(action, bet)))
                thisGameActions['Pot'] = self.pot + bet
                self.pot = self.pot + bet
                
                #update startPosition if there is a Raise or ALL IN
                if ((action == 'Raise') or (action == 'ALL IN')):
                    startPosition = playerIndex
                    
                #if Folded, turn isInGame to False, should have been handled by PlayerClass
                elif action == 'Fold':
                    self.PlayersList[playerIndex].endGame(0)
                
                else:
                    #Call, do nothing
                    pass
                    
            #update playerIndex
            playerIndex = (playerIndex + 1)%len(self.PlayersList)
                
        
        return isGameEnded
        
    
    @staticmethod
    def actionValidation(thisGameActions, currentAction):
        #check if the returned action is valid
        pass
    
    @staticmethod
    def playerValidation(player):
        #get player's nChip to make sure it's calculated correctly
        pass
    
    
    def runGame(self):
        """
        #main function, start the Game
        #termination condition : hit MAX_ITERATION OR Only one player active
        #create dictionary to keep track of the game        
        thisGameActions : {
                            'Street' : 'PreFlop/Flop/Turn/River',
                            'Actions' : {
                                'PreFLop' : [(playerName:str, action:tuple(str, int)),... etc] ,
                                'Flop' : [] ,
                                'Turn' : [] ,
                                'River' : []
                                },
                            'CommunityCards' : {
                                'Flop' : [Card, Card, Card] ,
                                'Turn' : [] ,
                                'River' : []                                
                                },
                            'Pot' : potSize
                            }
        """
        if self.getNPlayer() < 3:
            print('not enough players')
            return 0
        
        # Control Variables for the WHILE LOOP below
        i = 0 #game id
        currentSB = 0 #SB marker : SB players index in PlayerList
        
        #create a deck for following game
        theDeck = Deck(1)        
 
        #Start the 'tournament'
        while True:
            
            # EXIT Condition:
            if ((i == self.MAX_ITERATION) or (self.getNPlayer_active() < 3)):
                print('All games end')
                return 0
        
            #prepare a new game :
            # make sure pot is empty
            self.pot = 0
            
            # Shuffle the deck
            theDeck.shuffle(3)
            #prepare an empty ActionHistory
            thisGameActions = {  'Street' : 'PreFlop',
                    'Actions' : {
                        'PreFLop' : [] ,
                        'Flop' : [] ,
                        'Turn' : [] ,
                        'River' : []
                        },
                    'BetHistory' : {
                        'PreFlop' : [],
                        'Flop' : [],
                        'Turn' : [],
                        'River' : []
                        },
                    'CommunityCards' : {
                        'Flop' : [] ,
                        'Turn' : [] ,
                        'River' : []                                
                        },
                    'Pot' : self.pot,
                    'NPlayers' : len(self.PlayersList)}
            
            print("Game ", " ", i)
            
            

            # Start a new Game, if active, dealt card, give a position, update position
            # dealt card to players, and 'tell them their position in this game'
            currentSB = self._prepareGame(thisGameActions, theDeck, currentSB) #returned adjusted/fixed currentSB
            # adjust currentSB to next player for next game
            currentSB = currentSB + 1
            #all plalyers have their cards, blinds are paid
            
            #Game Start:
            #while loop to ask around, move to next street until every one agree on the bet
            for street in ['PreFLop', 'Flop', 'Turn', 'River']:

                    
                """
                TODO: 
                1. PreFlop, force player 0 and player 1 pay SB and BB , DONE in prepareGame()
                2. Track current max bet, and ask for diff between past bet and max bet
                3. Loop all players, until all players
                    either: a. Fold and isInGame = False
                            b. past bet == max bet
                            c. ALL IN, past bet < max bet and Player's nChip = 0
                4. end this street, move to next, if street == Riever, call findWinner()
                """
                #update street to thisGameActions
                thisGameActions['Street'] = street
                #run currentStreet and return True if game ended
                gameEnd = self._runCurrentStreet(thisGameActions,theDeck, currentSB)
                
                if gameEnd:
                    #Determin Winner
                    #TODO: winner function
                    if self.getNPlayer_inGame() == 1:
                        index = 0
                        for i, plyr in enumerate(self.PlayersList):
                            if plyr.isInGame() == True:
                                index = i
                        print("All other players folded, Winner is " + self.PlayersList[index].name() + ' at position ' + index)
                        self.PlayersList[index].endGame(self.pot) #pay the player
                        self.pot = 0
                    elif len(thisGameActions['CommunityCards']['River']) == 0:
                        print("Error no enough community cards to find winner")
                    elif self.getNPlayer_inGame < 2:
                        print("Error no enough remaining players")
                    else:
                        #Need to compare players hands:
                        community_card = thisGameActions['CommunityCards']['Flop'] + thisGameActions['CommunityCards']['Turn'] + thisGameActions['CommunityCards']['River']
                        players_hand = {}
                        for index, plyr in enumerate(self.PlayersList):
                            if((plyr.isInGame())&(plyr.isActive())):
                                players_hand[index] = plyr.hand
                        
                        winners_list = calc.find_winner(community_card, players_hand)
                        
                        profits = self.pot/len(winners_list)
                        
                        for player_index in winners_list:
                            self.PlayersList[player_index].endGame(profits)
                            
                        self.pot = 0
                        
                    
                    break
                
            

            # Current Game ends
            
            #update game id
            i = i + 1
            #update currentSB
            currentSB = (currentSB + 1)%len(self.PlayersList) 

            
        