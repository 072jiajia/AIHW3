import matplotlib.pyplot as plt


class Board:
    '''A class of Board which can be visualized'''

    def __init__(self):
        self.observed_board = None
        self.mine_board = None

    def imshow(self, new=False):
        '''make the initial outlook of the board and show'''
        #  use the interactive mode to show
        if new:
            plt.figure(2)
        plt.ion()
        # make sure all the blocks are on the board and draw the grids
        plt.xlim(0, self.size[0])
        plt.ylim(0, self.size[1])
        for i in range(self.size[0]+1):
            plt.axvline(i)
        for j in range(self.size[1]+1):
            plt.axhline(j)
        # make all the blocks gray since the unassigned blocks should be gray
        x = [0, self.size[0], self.size[0], 0]
        y = [0, 0, self.size[1], self.size[1]]
        plt.fill(x, y, 'gray')

        # make assigned blocks (initial safe blocks) yellow and show hints
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.observed_board[i][j] == 1:
                    self.show_block(i, j)
        # show and pause 1 second so that I can at least
        # check whether there's any bug here.
        plt.pause(1e-10)

    def show_block(self, i, j, PAUSE=False):
        '''show the block at (i, j)'''
        # show the block which is going to be chosen
        if PAUSE:
            x = [i, i+1, i+1, i]
            y = [j, j, j+1, j+1]
            plt.fill(x, y, 'red')
            plt.pause(1e-10)
        # generate the corresponse colored block
        if self.mine_board[i][j] == -1:
            x = [i, i+1, i+1, i]
            y = [j, j, j+1, j+1]
            plt.fill(x, y, 'yellow')
            # self.size * 0.01 to make sure that
            # the word is at the center of the block
            plt.text(i + 0.5 - self.size[0] * 0.01,
                     j + 0.5 - self.size[1] * 0.012,
                     'X', color='red')
        else:
            x = [i, i+1, i+1, i]
            y = [j, j, j+1, j+1]
            plt.fill(x, y, 'lime')
            # self.size * 0.01 to make sure that
            # the word is at the center of the block
            if self.mine_board[i][j]:
                plt.text(i + 0.5 - self.size[0] * 0.01,
                         j + 0.5 - self.size[1] * 0.012,
                         str(self.mine_board[i][j]), color='b')
        if PAUSE:
            # pause if necessary
            plt.pause(1e-10)
