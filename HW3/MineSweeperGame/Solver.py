import numpy as np
from Tools import *
import heapq
from .KnowledgeBase import *
import matplotlib.pyplot as plt
from .Board import *


class Solver(Board):
    ''' A minesweeper game solver
    - show: whether to show the graph of the game board
    - show_steps: whether to show the steps of each dicision
    - size: board size
    - num_mines: global constraint
    - KB: knowledge base
    '''

    def __init__(self, show=False, show_steps=False):
        super().__init__()
        self.show = show
        self.show_steps = show_steps
        self.size = None
        self.num_mines = None
        self.KB = None
        return None

    def solve(self, game):
        '''solve the game'''
        self.size, self.num_mines, self.observed_board, self.mine_board = game.outlook()
        if self.show:
            # show 2 graph, the first one is the original graph
            # the second one is also the original graph, but it will
            # be updated when solving
            self.imshow()
            self.imshow(new=True)

        # initialize KB and Priority Queue
        self.KB = KnowledgeBase()
        heap = []
        heapq.heappush(heap, (float('inf'), (None, None)))
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.observed_board[i][j] == 1:
                    if self.mine_board[i][j] == 0 or self.mine_board[i][j] == 8:
                        heapq.heappush(heap, (-1, (i, j)))
                    else:
                        heapq.heappush(heap, (i + j, (i, j)))

        # when priority queue is not empty, generate the clauses
        # of a block and add it to the KB. if we get some conclusion
        # of some block, assign the value to the block and gain more information
        while len(heap):
            (dummy, (x, y)) = heapq.heappop(heap)
            if x == None and y == None:
                Unassignedlist = self.unassigned_mine()
                # when unassigned variable is small enough,
                # generate clauses and add it to KB
                if len(Unassignedlist) < 10:
                    print('It might be a stuck game')
                    print('considering the number of mines...')
                    print('(it might take some time)')
                    Count = 0
                    for i in range(self.size[0]):
                        for j in range(self.size[1]):
                            if self.mine_board[i][j] == -1:
                                Count += 1
                    self.KB.insert_clauses(Unassignedlist,
                                           self.num_mines - Count)
                    self.query_known_blocks(game, heap)
                    continue
                else:
                    break
            # generate the Unassigned variables' list and if
            # it is not an empty set,
            Unassignedlist = self.unassigned_neighbor(x, y)
            if len(Unassignedlist) == 0:
                continue
            self.KB.insert_clauses(Unassignedlist,
                                   self.mine_board[x][y] - self.assigned_mine(x, y))
            # print(len(self.KB.clauses))
            self.query_known_blocks(game, heap)
        # show final graph of board
        if self.show:
            self.imshow()
        # return 'stuck game' or 'finished''
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.observed_board[i][j] == 0:
                    return 'stuck game'
        return 'finished'

    def query_known_blocks(self, game, heap):
        '''if existing a block whose value is known,
        ask the game administrator whether it is correct and
        gain the number of hint if it is a hint'''
        clauses = self.KB.clauses
        idx = 0
        while idx < len(clauses):
            if len(clauses[idx].pliterals) == 0:
                if len(clauses[idx].nliterals) == 1:
                    for (x, y) in clauses[idx].nliterals:
                        self.observed_board[x][y] = 1
                        self.mine_board[x][y] = game.query(x, y, False)
                        if self.show and self.show_steps:
                            self.show_block(x, y, True)
                        if self.mine_board[x][y] == 0 or self.mine_board[x][y] == 8:
                            heapq.heappush(heap, (-1, (x, y)))
                        else:
                            heapq.heappush(heap, (x + y, (x, y)))
                    clauses.pop(idx)
                    continue
            if len(clauses[idx].nliterals) == 0:
                if len(clauses[idx].pliterals) == 1:
                    for (x, y) in self.KB.clauses[idx].pliterals:
                        self.observed_board[x][y] = 1
                        self.mine_board[x][y] = game.query(x, y, True)
                        if self.show and self.show_steps:
                            self.show_block(x, y, True)
                    self.KB.clauses.pop(idx)
                    continue
            idx += 1

    def unassigned_neighbor(self, i, j):
        '''get unassigned neeighboring variables'''
        Ns = neighbor(self.size, (i, j))
        Unassignedlist = []
        for (Nx, Ny) in Ns:
            if self.observed_board[Nx][Ny] == 0:
                Unassignedlist.append((Nx, Ny))

        return Unassignedlist

    def assigned_mine(self, i, j):
        '''get number of neighboring block which is 
        assigned as mine'''
        Ns = neighbor(self.size, (i, j))
        ret = 0
        for (Nx, Ny) in Ns:
            if self.observed_board[Nx][Ny] == 1:
                if self.mine_board[Nx][Ny] == -1:
                    ret += 1
        return ret

    def unassigned_mine(self):
        '''when using global constraint, get all of the 
        unassigned variable on the board'''
        ret = []
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.observed_board[i][j] == 0:
                    ret.append((i, j))
        return ret
