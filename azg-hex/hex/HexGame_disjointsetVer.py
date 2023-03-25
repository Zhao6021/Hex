from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .HexLogic_disjointsetVer import Board
import numpy as np

class HexGame(Game):
    square_content = {
        -1: "X",
        +0: ".",
        +1: "O"
    }

    @staticmethod
    def getSquarePiece(piece):
        return HexGame.square_content[piece]

    def __init__(self, n):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getInitSet(self):
        # return initial disjoint set
        b = Board(self.n)
        return b.disjoint_set

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n

    def getNextState(self, board, disjoint_set, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        #print("action=",action)
        b = Board(self.n)
        b.pieces = np.copy(board)
        b.disjoint_set = disjoint_set
        move = (int(action/self.n), action%self.n)
        #print(move)
        b.execute_move(move, player)
        '''
        for i in range(self.n):
            for j in range(self.n):
                print(b.pieces[i][j], end=' ')
            print()
        '''
        return (b.pieces, b.disjoint_set, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves(player)
        if len(legalMoves)==0:
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n*x+y]=1
        return np.array(valids)

    def getGameEnded(self, board, disjoint_set, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        use_disjoint_ver = True

        if not use_disjoint_ver:
            b = Board(self.n)
            b.pieces = np.copy(board)
            if b.check_player_win_DFS(player):
                return player
            return 0
        if use_disjoint_ver:
            b = Board(self.n)
            b.pieces = np.copy(board)
            b.disjoint_set = disjoint_set
            if b.check_player_win_DisjointSet(player):
                return player
            return 0

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board
        '''
        #因不是完全對稱 所以以斜對角為軸做翻轉
        if player == 1:
            return board
        else:
            return np.fliplr(np.rot90(-1*board, axes=(1, 0)))
        '''

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2)  # 1 for pass
        pi_board = np.reshape(pi, (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s

    '''
    def getScore(self, board, player):
        b = Board(self.n)
        b.pieces = np.copy(board)
        return b.countDiff(player)
    '''

    @staticmethod
    def display(board):
        n = board.shape[0]
        print("   ", end="")
        for y in range(n):
            print(y, end=" ")
        print("")
        print("-----------------------")
        for x in range(n):
            print(x, "|", end="")    # print the row #
            for y in range(n):
                piece = board[x][y]    # get the piece to print
                print(HexGame.square_content[piece], end=" ")
            print("|")

        print("-----------------------")

    def display1(board):
        n = board.shape[0]

        print("   ", "W  " * n, "\n    ", end="")
        for y in range(n):
            print (y, "\\",end="")
        print("")
        print("", "----" * n)
        for y in range(n):
            print(" " * y, "B", y, "\\",end="")    # print the row #
            for x in range(n):
                piece = board[x][y]    # get the piece to print
                if piece == -1: print("b  ",end="")
                elif piece == 1: print("w  ",end="")
                else:
                    if x==n:
                        print("-",end="")
                    else:
                        print("-  ",end="")
            print("\\ {} B".format(y))

        print(" " * n, "----" * n)
        print("      ", " " * n, end="")
        for y in range(n):
            print (y, "\\",end="")
        print("")        
        print("      ", " " * n, "W  " * n)
