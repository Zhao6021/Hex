from hex.HexGame import HexGame as Game

class Node():
    def __init__(self,i):
        self.parent = self
        self.index = i
        self.rank = 0

class BoardDisjointSet():
    def __init__(self, board_size):
        self.nodes = []
        for i in range(board_size):
            self.nodes.append(Node(i))
        
    def find(self, index):
        n = self.nodes[index]
        visited_nodes = []
        while n.parent != n:
            visited_nodes.append(n)
            n = n.parent

        for visited in visited_nodes:
            visited.parent = n
        return n 

    def union(self, index_a, index_b):
        a_root = self.find(index_a)
        b_root = self.find(index_b)
        if a_root != b_root:
            # 把 rank(深度) 小的掛到 rank 大的下方
            if a_root.rank < b_root.rank:
                a_root.parent = b_root
            else:
                b_root.parent = a_root
            if b_root.rank == a_root.rank:
                a_root.rank += 1

    def isSameGroup(self,  index_a, index_b):
        return self.find(index_a) == self.find(index_b)


g = Game(6)
board= g.getInitBoard()
#Game.display1(board)
print(g.getBoardSize()[0] * g.getBoardSize()[1])
set = BoardDisjointSet(g.getBoardSize()[0] * g.getBoardSize()[1])
print(set.find(5).index)    #5
set.union(5,7)
print(set.find(5).index)    #5
print(set.find(7).index)    #7
set.union(6,7)
print(set.find(5).index)    #6
print(set.find(6).index)    #6
print(set.find(7).index)    #6
print(set.isSameGroup(5,6))
print(set.isSameGroup(5,7))
print(set.isSameGroup(7,6))
print(set.isSameGroup(1,6))
print(set.isSameGroup(1,5))
print(set.isSameGroup(7,1))
print(set.nodes[5].rank)
set.union(1,2)
set.union(1,3)
set.union(1,5)
print(set.find(5).rank)
