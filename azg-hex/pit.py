import Arena
from MCTS import MCTS
from hex.HexGame import HexGame
from hex.HexPlayers import *
from hex.pytorch.NNet import NNetWrapper as NNet


import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

human_vs_cpu = False
cpu_random_player = False


g = HexGame(8)

# all players
rp = RandomPlayer(g).play
hp = HumanHexPlayer(g).play
abp = AlphaBetaPlayer(g, 3).play


# nnet players
if not cpu_random_player:
    n1 = NNet(g)
    n1.load_checkpoint('./models/','6to8x8_method3_202.pth.tar')
    args1 = dotdict({'numMCTSSims': 3000, 'cpuct':3.0})
    mcts1 = MCTS(g, n1, args1)
    n1p = lambda x, player: np.argmax(mcts1.getActionProb(x, player, temp=0))

#human vs cpu
if human_vs_cpu:
    player2 = hp
    if cpu_random_player:   #random cpu
        n1p = rp
else:
    n2 = NNet(g)
    n2.load_checkpoint('./models/','6to8x8_method3_300.pth.tar')
    args2 = dotdict({'numMCTSSims': 3000, 'cpuct': 3.0})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x, player: np.argmax(mcts2.getActionProb(x, player, temp=0))

    player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

arena = Arena.Arena(n1p, player2, g, display=HexGame.display1)

print(arena.playGames(10, verbose=False))
