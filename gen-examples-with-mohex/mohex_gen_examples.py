from mohex_connecter import Mohex_Connecter
import random
from HexGame import HexGame as Game
import numpy as np
import os
from pickle import Pickler, Unpickler
import time

def getSymmetricalExample(e, PiBoard2D):
    sym_e = []
    rot_board = np.rot90(e[0],2)
    rot_PiBoard2D = np.rot90(PiBoard2D,2)
    rot_PiBoard = rot_PiBoard2D.flatten().tolist()
    sym_e.append(rot_board)
    sym_e.append(rot_PiBoard)
    sym_e.append(e[2])
    return sym_e


def getPiBoard2D(boardSize, mohex_ans):
    num_ans = len(mohex_ans)
    pi_board_2D = np.zeros((boardSize,boardSize))
    if num_ans != 0:
        pi = 1/num_ans
        for ans in mohex_ans:
            pi_board_2D[int(ans[1])-1][ord(ans[0])-97] = pi
    return pi_board_2D

def checkPiBoardCorrect(PiBoard):   #check the values of pi board
    for val in PiBoard:
        if val != 0:
            return True
    return False

def genExamples(args):
    """
    will return a list of the form (canonicalBoard, pi, v)
    """
    mohex = Mohex_Connecter(args.boardSize)
    mohex.mohex_set_dfpn_threads(args.numDfpnThreads)
    examples = []
    num_zero_pi_avoid = 0
    num_zero_pi = 0
    for i in range(args.numPlay):
        print('game:', i+1)
        mohex.board_init(args.boardSize)
        g = Game(args.boardSize)
        board = g.getInitBoard()
        #g.display(board)
        curPlayer = 'b'
        #mohex.mohex_showboard()
        while True:
            e = []
            p = 1 if curPlayer == 'b' else -1     #form of player for AZG board
            '''add canonicalBoard'''
            e.append(g.getCanonicalForm(board, p))
            '''add pi_board'''
            mohex_ans = mohex.mohex_solve(curPlayer)
            if len(mohex_ans) == 0:
                opponent = 'w' if curPlayer == 'b' else 'b' #block opponent's winning move
                mohex_ans = mohex.mohex_solve(opponent)
                #pi_board = getPiBoard2D(args.boardSize, mohex_ans)
                #print("op= ",opponent)
                #print("cur= ",curPlayer)
                #print(pi_board)
                #mohex.mohex_showboard()
                #time.sleep(10)
                num_zero_pi_avoid += 1
            #print(mohex_ans)
            pi_board_2D = getPiBoard2D(args.boardSize, mohex_ans)
            #print(pi_board_2D)
            if curPlayer=='w':
                pi_board_2D = np.fliplr(np.rot90(pi_board_2D, axes=(1, 0)))
            pi_board = pi_board_2D.flatten().tolist()
            e.append(pi_board)
            '''add v'''
            winner = mohex.mohex_solve_state()
            v = 0
            if winner == curPlayer:
                v = 1
            else:
                v = -1
            e.append(v)
            if checkPiBoardCorrect(e[1]):
                examples.append(e)
                examples.append(getSymmetricalExample(e, pi_board_2D))
            else:
                num_zero_pi+=1
            moves = mohex.mohex_all_legal_moves()
            m = random.choice(moves)
            m_for_AZG = (int(m[1])-1)*args.boardSize + (ord(m[0])-97)
            board, _ = g.getNextState(board, p, m_for_AZG)
            mohex.mohex_playmove(curPlayer, m)
            #mohex.mohex_showboard()
            #g.display(board)
            
            if g.getGameEnded(board, p) != 0:
                break

            if curPlayer=='b':
                curPlayer = 'w'
            else:
                curPlayer='b'
    mohex.kill()
    print("num_zero_pi=",num_zero_pi)
    print("num_zero_pi_avoid=",num_zero_pi_avoid)
    return examples

def saveExamples(examples, file_name):
    folder = "./examples/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, file_name + ".examples")
    with open(filename, "wb+") as f:
        Pickler(f).dump(examples)
    f.closed
