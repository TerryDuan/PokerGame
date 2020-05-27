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
import TexasHoldemCalculators as calc
import numpy as np
import math
from datetime import datetime
import pickle

class table():
    
    def __init__(self):
        self.buttomPosition = 0
        self.PlayersList = [] 
        self.PlayerStack = []
        self.pot = 0
        self.bb = 2
        self.sb = 1
        self.MAX_ITERATION = 50

    def addPlayer(self, newPlayer : Player, newPlayerStack : int):
        self.PlayersList.append(newPlayer)
        self.PlayerStack.append(newPlayerStack)
        
    def getPot(self):
        return self.pot
    
    def getNPlayer(self):
        return len(self.PlayersList)
    
    def getNPlayer_active(self):
        n = 0
        for i, plyr in enumerate(self.PlayersList):
            if (plyr.isActive() & (self.PlayerStack[i] > 0)):
                n = n + 1
        
        return n
    
    def getNPlayer_inGame(self):
        n = 0
        for plyr in self.PlayersList:
            if plyr.isInGame():
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
        tempBetHistory_other_street = [np.nan]*nAllPlayers
        
        while(positionCode < (nActivePlayers )): #while minused 1 before??

            if ((self.PlayersList[PlayersIndex].isActive())&(self.PlayerStack[PlayersIndex] > 0)):
                #it's still active AND have positive stack
                
                #this player is active, prepare required blinds, store currentSB if it's SB
                if positionCode == 0:
                #if we just assing SB player, update new currentSB for return
                    currentSB = PlayersIndex
                    tempBetHistory[PlayersIndex] = self.sb#to be removed
                    price2play = self.sb#to be removed
                    
                    if self.PlayerStack[PlayersIndex] >= self.sb:
                        self.PlayerStack[PlayersIndex] = self.PlayerStack[PlayersIndex] - self.sb
                        tempBetHistory[PlayersIndex] = self.sb
                        thisGameActions['Pot'] = self.pot + self.sb
                        self.pot = self.pot + self.sb
                    else:
                        price2play = self.PlayerStack[PlayersIndex]
                        tempBetHistory[PlayersIndex] = price2play
                        self.PlayerStack[PlayersIndex] = 0
                        thisGameActions['Pot'] = self.pot + price2play
                        self.pot = self.pot + price2play
                
                elif positionCode == 1:
                    tempBetHistory[PlayersIndex] = self.bb
                    price2play = self.bb
                    
                    if self.PlayerStack[PlayersIndex] >= self.bb:
                        self.PlayerStack[PlayersIndex] = self.PlayerStack[PlayersIndex] - self.bb
                        tempBetHistory[PlayersIndex] = self.bb
                        thisGameActions['Pot'] = self.pot + self.bb
                        self.pot = self.pot + self.bb
                    else:
                        price2play = self.PlayerStack[PlayersIndex]
                        tempBetHistory[PlayersIndex] = price2play
                        self.PlayerStack[PlayersIndex] = 0
                        thisGameActions['Pot'] = self.pot + price2play
                        self.pot = self.pot + price2play
                    
                else:
                    price2play = 0
                
                #prepare hands
                hand = []
                hand.append(theDeck.dealt())
                hand.append(theDeck.dealt())        
                
                #ACTIVATE the Player
                initBet = self.PlayersList[PlayersIndex].startGame(hand, positionCode, price2play) #TODO
                #Add bet to Pot (sb, bb, sttradle)

                
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
        thisGameActions['BetHistory']['Flop'] = tempBetHistory_other_street.copy()
        thisGameActions['BetHistory']['Turn'] = tempBetHistory_other_street.copy()
        thisGameActions['BetHistory']['River'] = tempBetHistory_other_street.copy()
        return currentSB
                

    
    
    def _runCurrentStreet(self, thisGameActions,theDeck, currentSB : int,file):
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
        file : os.file
            log file for history
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
            cards.append(theDeck.dealt())
            cards.append(theDeck.dealt())
            cards.append(theDeck.dealt())
            thisGameActions['CommunityCards'][thisGameActions['Street']] = cards            
        else:
            startPosition = currentSB
            playerIndex = startPosition
            maxBet = 0
            cards = []
            cards.append(theDeck.dealt())
            thisGameActions['CommunityCards'][thisGameActions['Street']] = cards
        
        
        # Start the Loop over all Players
        while True:
            print("\nCurrent street " , thisGameActions['Street'], " on Player at Index : ", playerIndex, " with Past Bet of ", thisGameActions['BetHistory'][thisGameActions['Street']][playerIndex],  file=file)
            print("Current maxBet: ", maxBet, " by Player at Index: ", startPosition, " in Game? ", self.PlayersList[playerIndex].isInGame(),  file=file)
            print("All players BetHistory so far : ", thisGameActions['BetHistory'][thisGameActions['Street']],  file=file)
            
            
            pastBet = thisGameActions['BetHistory'][thisGameActions['Street']][playerIndex]
            minInGameBet = self._minInGameBet(thisGameActions)
            
            if ((minInGameBet == maxBet) and (playerIndex == startPosition) and ( ((not math.isnan(pastBet)) and pastBet == maxBet) or self.PlayersList[playerIndex].isInGame() == False or self.PlayersList[playerIndex].isActive() == False) ):
                #END Condition:
                #All Bets from All Players are either nan (not playing) or ,at least, same as maxBet --- TRUE if all checks, all called, FALSE if no action yet (the first time playerIndex == startPosition) or not all Called or Checked
                #AND
                #Current Iteration is back to startPosition (UTG for River, SB for other Streets, or the Player with initial maxBet)
                #AND
                #Current Iteration(Player) has not null past bet in current street (action() has been called) and pastBet == maxBet , EXCEPT it's not in the game --- a sanity check, False if BetHistory, maxBet, bet are out of sync
                print("*******",  file=file)
                print("Current Street ", thisGameActions['Street'] , " Ends",  file=file)
                print("Current Pot: " , thisGameActions['Pot'],  file=file)
                print("*******",  file=file)
                
                if thisGameActions['Street'] == 'River':
                    isGameEnded = True
                elif self.getNPlayer_inGame() <= 1: #to cover every one fold (invalid)
                    isGameEnded = True
                
                break
            
            ### Checks
            #print(self.PlayersList[playerIndex].isActive())
            #print(self.PlayersList[playerIndex].isInGame())
            #print(math.isnan(thisGameActions['BetHistory'][thisGameActions['Street']][playerIndex]))
            
            
            
            if ((self.PlayersList[playerIndex].isActive()) and (self.PlayersList[playerIndex].isInGame()) ):
                
                print("Call for action on Player at Index: ", playerIndex,  file=file)
                
                action, bet = self.PlayersList[playerIndex].action(np.where(math.isnan(pastBet), maxBet, maxBet - pastBet), thisGameActions)
                maxBet = np.nanmax([maxBet, np.where(math.isnan(pastBet), 0, pastBet) + bet ]) #update maxBet
                
                print("Player at Index's Action: ", action, " with bet: ", bet,  file=file)
                
                #Check if Action Valid
                if self._actionValidation(thisGameActions, action, bet, playerIndex, file) == False:
                    print("Player at ", playerIndex, " returned an invalid action, FORCE to FOLD",  file=file)
                    self.PlayersList[playerIndex].endGame(0)
                    action = 'Forced FOLD'
                
                #record actions,BetHistory,Pot
                thisGameActions['BetHistory'][thisGameActions['Street']][playerIndex] = np.where(math.isnan(pastBet), 0, pastBet) + bet
                thisGameActions['Actions'][thisGameActions['Street']].append((self.PlayersList[playerIndex].name,(action, bet)))
                thisGameActions['Pot'] = thisGameActions['Pot'] + min(bet, self.PlayerStack[playerIndex] )
                self.pot = self.pot + min(bet, self.PlayerStack[playerIndex] )
                self.PlayerStack[playerIndex] = max(self.PlayerStack[playerIndex] - bet, 0)
                
                    
                #update startPosition if there is a Raise or ALL IN
                if ((action.upper() == 'RAISE') or (action.upper() == 'BET') or (action.upper() == 'ALL IN')):
                    startPosition = playerIndex
                    
                #if Folded, turn isInGame to False, should have been handled by PlayerClass
                elif action.upper() == 'FOLD':
                    self.PlayersList[playerIndex].endGame(0)    
                else:
                    #Call or Check, do nothing to the startPosition
                    pass
            else:
                print("current player out of game, Skip current player",  file=file)
            

                    
            #update playerIndex
            playerIndex = (playerIndex + 1)%len(self.PlayersList)
                
        
        return isGameEnded
        
    
    def _minInGameBet(self, thisGameActions):
        currentStreet = thisGameActions['Street']
        betHistory = thisGameActions['BetHistory'][currentStreet]
        inGameBetHistory = []
        for idx, plyr in enumerate(self.PlayersList):
            if ((plyr.isInGame())&(plyr.isActive())):
                inGameBetHistory.append(betHistory[idx])
        if len(inGameBetHistory) > 0:
            return np.nanmin(inGameBetHistory)
        else:
            print("Warning: Everyone Fold before game end")
            return np.nanmax(betHistory)
    
    def _actionValidation(self, thisGameActions, currentAction, currentBet, playerIndex, file):
        #check if the returned action is valid
        currentStreet = thisGameActions['Street']
        if np.isnan(currentBet):
            print("INVALID NaN Bet",  file=file)
            return False
        elif currentAction.upper() == 'FOLD':
            return not self.PlayersList[playerIndex].isInGame()  #True if the inGame flag is False
        elif currentAction.upper() == 'CALL':
            maxBet = np.where(np.isnan(np.nanmax(thisGameActions['BetHistory'][currentStreet])), 0, np.nanmax(thisGameActions['BetHistory'][currentStreet]))
            allBet = np.where(np.isnan(currentBet), 0, currentBet) + np.where(np.isnan(thisGameActions['BetHistory'][currentStreet][playerIndex]), 0, thisGameActions['BetHistory'][currentStreet][playerIndex])
            return allBet == maxBet #True if all past bet in this street match to maxBet
        elif currentAction.upper() == 'CHECK':
            maxBet = np.where(np.isnan(np.nanmax(thisGameActions['BetHistory'][currentStreet])), 0, np.nanmax(thisGameActions['BetHistory'][currentStreet]))
            allBet = np.where(np.isnan(currentBet), 0, currentBet) + np.where(np.isnan(thisGameActions['BetHistory'][currentStreet][playerIndex]), 0, thisGameActions['BetHistory'][currentStreet][playerIndex])
            return ((allBet == maxBet)&(np.where(np.isnan(currentBet), 0, currentBet) == 0)) #True if all past bet in this street match to maxBet AND current Bet is 0
        elif currentAction.upper() == 'ALL IN':
            maxBet = np.where(np.isnan(np.nanmax(thisGameActions['BetHistory'][currentStreet])), 0, np.nanmax(thisGameActions['BetHistory'][currentStreet]))
            allBet = np.where(np.isnan(currentBet), 0, currentBet) + np.where(np.isnan(thisGameActions['BetHistory'][currentStreet][playerIndex]), 0, thisGameActions['BetHistory'][currentStreet][playerIndex])
            if allBet < maxBet:
                return self.PlayersList[playerIndex].nChip == 0 #True if player bet with all remaining chips
            else:
                return True #Else True
        elif ((currentAction.upper() == 'BET') or (currentAction.upper() == 'RAISE')):
            maxBet = np.where(np.isnan(np.nanmax(thisGameActions['BetHistory'][currentStreet])), 0, np.nanmax(thisGameActions['BetHistory'][currentStreet]))
            allBet = np.where(np.isnan(currentBet), 0, currentBet) + np.where(np.isnan(thisGameActions['BetHistory'][currentStreet][playerIndex]), 0, thisGameActions['BetHistory'][currentStreet][playerIndex])
            return allBet > maxBet       
        else:
            print("INVALID ACTION CATEGORY",  file=file)
            return False
    
    def _gameValidation(self, thisGameActions):
        """
        Check if Total Chips are not changing
        Check if Players' nChip is correct after the game
        """
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
        GAME_ID = 0 #game id
        currentSB = 0 #SB marker : SB players index in PlayerList
        
        #prepare pickle file to store game history
        filename = 'history_' + datetime.today().strftime('%Y_%m_%d_%H_%M_%S') + '.pickle'
        outfile = open('../GameHistory/' + filename, 'wb')
        file=open('..\GameHistory\log.txt', 'w')
        #create a deck for following game
        theDeck = Deck(1)        
 
        #Start the 'tournament'
        while True:
            
            # EXIT Condition:
            if ((GAME_ID == self.MAX_ITERATION) or (self.getNPlayer_active() < 3)):
                print('*******ALL GAMES END**********')
                print("Summary")
                for plyr in self.PlayersList:
                    print(plyr.name, ' has remaining stack of ', str(plyr.nChip))
                    
                print('*******Save Game History******')
                outfile.close()
                file.close()
                return 0
        
            #prepare a new game :
            # make sure pot is empty
            self.pot = 0
            
            # Shuffle the deck
            seed = datetime.now().microsecond
            theDeck.shuffle(seed)
            if datetime.now().microsecond%3 == 0:
                seed = datetime.now().microsecond
                theDeck.shuffle(seed)
            if datetime.now().microsecond%7 == 0:
                seed = datetime.now().microsecond
                theDeck.shuffle(seed)
            if datetime.now().microsecond%5 == 0:
                theDeck = Deck(1) 
                seed = datetime.now().microsecond%3
                theDeck.shuffle(seed)
                
            
            #prepare an empty ActionHistory
            thisGameActions = {  'Street' : 'PreFlop',
                    'Actions' : {
                        'PreFlop' : [] ,
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
                    'Pot' : 0,
                    'NPlayers' : len(self.PlayersList),
                    'Winners' : [],
                    'PlayerStack' : self.PlayerStack
                    }
            
            print(" ",  file=file)
            print("Game ", " ", GAME_ID,  file=file)
            print("Game ", " ", GAME_ID)
            
            #print(thisGameActions)

            # Start a new Game, if active, dealt card, give a position, update position
            # dealt card to players, and 'tell them their position in this game'
            currentSB = self._prepareGame(thisGameActions, theDeck, currentSB) #returned adjusted/fixed currentSB
            # adjust currentSB to next player for next game
            #currentSB = currentSB + 1 #updated at last step
            #all plalyers have their cards, blinds are paid
            
            #Game Start:
            #while loop to ask around, move to next street until every one agree on the bet
            for street in ['PreFlop', 'Flop', 'Turn', 'River']:

                    
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
                gameEnd = self._runCurrentStreet(thisGameActions,theDeck, currentSB,file)
                
                if gameEnd:
                    #Determin Winner
                    #TODO: Some Pot are not fully distributed to Players
                    if self.getNPlayer_inGame() == 1:
                        index = 0
                        for i, plyr in enumerate(self.PlayersList):
                            if plyr.isInGame() == True:
                                index = i
                        print("All other players folded, Winner is " + self.PlayersList[index].name + ' at position ' + str(index),  file=file)
                        self.PlayersList[index].endGame(self.pot) #pay the player
                        self.PlayerStack[index] = self.PlayerStack[index] + self.pot
                        self.pot = 0
                        thisGameActions['Winners'].append((index, []))
                    elif len(thisGameActions['CommunityCards']['River']) == 0:
                        print("ERROR no enough community cards to find winner")
                    elif self.getNPlayer_inGame() < 2:
                        print("ERROR no enough remaining players")
                    elif self.getNPlayer_inGame() == 0:
                        print("ERROR ALL PLAYER FOLD")
                    else:
                        #Need to compare players hands:
                        community_card = thisGameActions['CommunityCards']['Flop'] + thisGameActions['CommunityCards']['Turn'] + thisGameActions['CommunityCards']['River']
                        players_hand = {}
                        for index, plyr in enumerate(self.PlayersList):
                            if((plyr.isInGame())&(plyr.isActive())):
                                players_hand[index] = plyr.hand
                        
                        winners_list = calc.find_winner(community_card, players_hand)
                        
                        print("Winner(s) is(are) " , winners_list,  file=file)
                        print("Community Cards: ",  file=file)
                        for i in community_card:
                            #print(i.prettyCard())
                            print(i,  file=file)
                        
                        print("----------------------",  file=file)
                        print("winner hands: ",  file=file)
                        for winner_index in winners_list:
                            
                            print("winner " + str(winner_index),  file=file)
                            #print(self.PlayersList[winner_index].hand[0].prettyCard())
                            #print(self.PlayersList[winner_index].hand[1].prettyCard())
                            print(str(self.PlayersList[winner_index].hand[0]), file=file)
                            print(str(self.PlayersList[winner_index].hand[1]), file=file)
                            print("----------------------",  file=file)
                            
                            thisGameActions['Winners'].append((winner_index, self.PlayersList[winner_index].hand))
                            
                        #chop:
                        profits = self.pot/len(winners_list)
                        
                        for player_index in winners_list:
                            self.PlayersList[player_index].endGame(profits)
                            self.PlayerStack[player_index] = self.PlayerStack[player_index] + profits
                        
                        self.pot = 0
                        
                    
                    break
                
            

            # Current Game ends
            print("game summary: ", file = file)
            for i, plyr in enumerate(self.PlayersList):
                print(plyr.name, ' has remaining stack of ', str(plyr.nChip), ' has remaining stack ON TABLE ', str(self.PlayerStack[i]), file = file)
                plyr.endGame(0) #just to make sure
            #save history
            pickle.dump(thisGameActions, outfile)
            
            #update game id
            GAME_ID = GAME_ID + 1
            #update currentSB
            currentSB = (currentSB + 1)%len(self.PlayersList) 

            
        