import time
from Tools import *
import numpy as np
from .Board import *


class MineSweeperGame(Board):
    '''this is a class for Minesweeper Game
    - size: size of board
    - num_mines: global constraint
    - mine_board: the real values (mine or hint 0~8) of the game
    - observed_board: if observed_board[i][j] is 1, (i, j) has been observed
    '''

    def __init__(self, size, num_mines, num_initial_safe_cells):
        '''initialize game'''
        super().__init__()
        self.size = size
        self.num_mines = num_mines
        self.mine_board = np.zeros(size, dtype=int)
        self.observed_board = np.zeros(size, dtype=int)
        self.generate_board(num_initial_safe_cells)

        return None

    def generate_board(self, num_initial_safe_cells):
        '''generate the board of the game'''
        for _ in range(self.num_mines):
            # generate mines
            while True:
                # randomly choose one block
                # if has been generated, continue and choose again
                i = np.random.randint(0, self.size[0])
                j = np.random.randint(0, self.size[1])
                if self.mine_board[i][j] == 0:
                    self.mine_board[i][j] = -1
                else:
                    continue

                # to make sure every mine has at least one hint (not mine)
                # mine: -1
                # not mine: -2
                # has not determine: 0
                neighbor_list = neighbor(self.size, (i, j))
                at_least_one_hint = False
                for (x, y) in neighbor_list:
                    if self.mine_board[x][y] == -2:
                        at_least_one_hint = True
                        break

                # if there's no not-mine block near the mine,
                # randomly generate a not-mine block
                if not at_least_one_hint:
                    zero_list = []
                    for (x, y) in neighbor_list:
                        if self.mine_board[x][y] == 0:
                            zero_list.append((x, y))
                    if len(zero_list) == 0:
                        # if we cannot generate any not-mine block
                        # near the block we're going to generate mine,
                        # continue and abondon this (i, j)
                        continue
                    elif len(zero_list) == 1:
                        # generate the only assignable block
                        (x, y) = zero_list[0]
                        self.mine_board[x][y] = -2
                    else:
                        # randomly generate a assignable block
                        randidx = np.random.randint(0, len(zero_list)-1)
                        (x, y) = zero_list[randidx]
                        self.mine_board[x][y] = -2
                # if generated successfully, break and do the next for loop
                self.mine_board[i][j] = -1
                break
        # for every block which is not mine, compute its constraint (hint)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.mine_board[i][j] != -1:
                    Count = 0
                    for (x, y) in neighbor(self.size, (i, j)):
                        if self.mine_board[x][y] == -1:
                            Count += 1
                    self.mine_board[i][j] = Count
        # generate the initial hint blocks which is different to
        # the original minesweepeer game, but required in this homework
        for _ in range(num_initial_safe_cells):
            while True:
                i = np.random.randint(0, self.size[0])
                j = np.random.randint(0, self.size[1])
                if self.mine_board[i][j] != -1 and self.observed_board[i][j] != 1:
                    self.observed_board[i][j] = 1
                    break

    def outlook(self):
        '''get the outlook of the board
        - get the board size
        - number of all mines
        - 2d nparray which shows that (x, y) has been discover when observed[x][y] == 1,
        - 2d nparray which shows that (x, y) is a mine(-1) or
            the number of the neighboring mine (0~8)
        '''
        size = self.size
        num_mines = self.num_mines
        observed = self.observed_board.copy()
        mines = np.zeros(size, dtype=int)
        for i in range(size[0]):
            for j in range(size[1]):
                if observed[i][j] == 1:
                    mines[i][j] = self.mine_board[i][j]
        return size, num_mines, observed, mines

    def query(self, x, y, mine):
        '''Player will do the same thing as 'click the board
        and get the response', when we get the wrong query
        (eg: click a mine or assign a not-mine as mine)
        I will simply raise value error because it can
        make debugging easier.
            if there's no error, just simply show the chosen block (if
        necessary) and return the value of the block to the player.
        '''
        self.observed_board[x][y] = 1
        if self.mine_board[x][y] == -1:
            if mine is True:
                return -1
            else:
                raise ValueError(x, y, 'is mine')
        else:
            if mine is False:
                return self.mine_board[x][y]
            else:
                raise ValueError(x, y, 'is not mine')
