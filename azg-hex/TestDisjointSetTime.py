from hex.HexGame_disjointsetVer import HexGame as Game
import numpy as np
import time

"Disjoint set"
num_games = 10000
g = Game(8)
time_start = time.time()
for game_count in range(num_games):
    #print(game_count)
    board = g.getInitBoard()
    disjoint_set = g.getInitSet()
    cur_player = 1
    win_player = 0
    while True:
        #print("cur player:", cur_player)
        valids = g.getValidMoves(board,cur_player)
        action = np.random.randint(g.getActionSize())
        while valids[action] != 1:
            action = np.random.randint(g.getActionSize())
        board, disjoint_set, cur_player = g.getNextState(board, disjoint_set, cur_player, action)
        #Game.display(board)
        if g.getGameEnded(board, disjoint_set, -cur_player) != 0:
            win_player = -cur_player
            #print("win:", win_player)
            break
    #a = input()
time_end = time.time()
print("disjoint:"+str(time_end-time_start))