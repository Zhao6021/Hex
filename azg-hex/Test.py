from hex.HexGame import HexGame as Game

if __name__ == "__main__":
    g = Game(6)
    board = g.getInitBoard()
    #disjoint_set = g.getInitSet()
    player = int(1)
    while True:
        Game.display(board)
        print("cur player:", player)
        print("valids: ")
        valids = g.getValidMoves(board,player)
        for i in range(0,len(valids)):
            if valids[i]==1:
                print("[", int(i/g.n), int(i%g.n), end="] ")
        print()
        print("input action: x y")
        actionXY=[int(x) for x in input().split()]
        if actionXY[0]==-1:
            break
        action = actionXY[0] * g.getBoardSize() [0] + actionXY[1]

        board, player = g.getNextState(board, player, action)
        #board, disjoint_set, player = g.getNextState(board, disjoint_set, player, action)
        Game.display(board)
        #board = g.getCanonicalForm(board,player)
        #Game.display(board)
        end = g.getGameEnded(board, -player)
        #end = g.getGameEnded(board, disjoint_set, -player)
        if end != 0:
            print("winner=",end)
            break
    