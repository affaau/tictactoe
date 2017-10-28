#!/usr/bin/python
# -*- coding: utf-8 -*-
"""tic-tac-toe game

@author: Affa
@date: 2017-09-07
"""
import random


class TicTacToeGame(object):
    """Play against computer program with certain intelligence & tactic"""
    def __init__(self):
        self.board = [' '] * 9
        self.sym = {'C': 'X', 'H': 'X'}
        self.next_turn = raw_input("Who starts first, 'C'omputer or 'H'uman? ").upper()
        print "Alright, first one always given 'O'."
        self.sym[self.next_turn] = 'O'
        self.start()

    def comp_move(self):
        """computer picks an empty cell in board"""
        print "Computer's turn...'%s'"%self.sym['C']
        pick = self.decision(2)
        self.board[pick] = self.sym['C']
        self.pick = pick

    def decision(self, method=1):
        """computer's decision algorithm"""
        if method == 1:
            # choose by random
            choices = [i for i in range(9) if self.board[i] == ' ']
            return random.choice(choices)
        elif method == 2:
            # by 'monte carlo' statistic
            # GOOD in predicting a WIN,
            # GOOD in defense!
            backup = self.board            # backup original board
            choices = [i for i in range(9) if self.board[i] == ' ']
            best_choice = -1
            best_score = -1

            for choice in choices:
                count_win = 0
                for trail in range(1000):  # repeat many trails
                    leave = list(choices)  # create new list
                    whose_turn = 'C'
                    self.pick = choice
                    self.board = list(backup)
                    while True:
                        self.board[self.pick] = self.sym[whose_turn]
                        if self.game() == 1:
                            if whose_turn == 'C': count_win += 1
                            break
                        elif leave == []:
                            # draw
                            break
                        else:
                            leave.remove(self.pick)
                            if leave != []:
                                self.pick = random.choice(leave)
                                whose_turn = 'C' if whose_turn=='H' else 'H'
                # end of trails
                if count_win > best_score:
                    if count_win != 1000:
                        best_score = count_win
                        best_choice = choice
                    else:
                        self.board = backup   # if sure win, WIN!
                        return choice
            #
            # check any immediate lost scenerio          
            self.board = list(backup)
            for choice in choices:
                self.pick = choice
                self.board[choice] = self.sym['H']
                if self.game() == 1:
                    self.board = backup
                    return choice             # if yes, go board it
                else:
                    self.board[choice] = ' '           
            #    
            self.board = backup   # restore board
            return best_choice    # pick the one with highest probability
        else:
            # by manual
            while True:
                pick = int(raw_input("Pick an empty cell [0-9]: "))
                if self.board[pick] == ' ':
                    return pick
                else:
                    print "Invalid cell. Try again."

    def hum_move(self):
        """human picks an empty cell in board"""
        print "Human's turn...'%s'"%self.sym['H']
        while True:
            pick = int(raw_input("Pick an empty cell [0-9]: "))
            if self.board[pick] == ' ':
                self.board[pick] = self.sym['H']
                self.pick = pick
                break
            else:
                print "Invalid cell. Try again."

    def print_board(self):
        """print the latest status of board"""
        print ""
        line = "-------------"
        print line
        print "| %s | %s | %s |" % tuple(self.board[0:3])
        print line
        print "| %s | %s | %s |" % tuple(self.board[3:6])
        print line
        print "| %s | %s | %s |" % tuple(self.board[6:9])
        print line

    def game(self):
        """if the game is done?
        return 1 if anyone wins else return 0"""
        row = self.pick // 3
        col = self.pick % 3

        if self.board[3 * row] == self.board[1 + 3 * row] and self.board[1 + 3 * row] == self.board[2 + 3 * row]: return 1
        elif self.board[0 + col] == self.board[3 + col] and self.board[3 + col] == self.board[6 + col]: return 1
        elif self.pick in [1, 3, 5, 7]: return 0
        elif self.pick in [0, 8]:
            if self.board[0] == self.board[4] and self.board[4] == self.board[8]: return 1
            else: return 0
        elif self.pick in [2, 6]:
            if self.board[2] == self.board[4] and self.board[4] == self.board[6]: return 1
            else: return 0
        elif self.board[2] == self.board[4] and self.board[4] == self.board[6]: return 1
        elif self.board[0] == self.board[4] and self.board[4] == self.board[8]: return 1
        else: return 0

    def start(self):
        """main game loop"""
        self.next_turn = 'H' if self.next_turn=='C' else 'C'
        self.print_board()
        while ' ' in self.board:
            (next_move, self.next_turn) = (self.comp_move, 'C') if self.next_turn == 'H' else (self.hum_move, 'H')
            next_move()
            self.print_board()
            if self.game() == 1:
                player = 'Human' if self.next_turn == 'H' else 'Computer'
                print "Congrats! %s won" % (player,)
                return

        print"Oh, it's a draw!"

new_game = TicTacToeGame()