
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
        while n.parent != n:    #parent不是指向自己(不是root)
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

class Board():

    # list of all 6 directions on the board, as (x,y) offsets
    __directions = [(-1,0),(0,-1),(1,-1),(1,0),(0,1),(-1,1)]

    def __init__(self, n):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n

        # For disjoint set
        self.disjoint_set = BoardDisjointSet(n*n)

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]


    def get_legal_moves(self,player):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = list()  # stores the legal moves.

        for x in range(self.n):
            for y in range(self.n):
                if self.pieces[x][y] == 0:
                    moves.append((x, y))
        return moves

    def has_legal_moves(self):
        return len(self.get_legal_moves())>0

    def is_valid_pos(self, x, y):
        if x < 0 or y < 0 or x >= self.n or y >= self.n:
            return False
        return True

    def execute_move(self, move, color):
        """Perform the given move on the board"""
        # Add the piece to the empty square.
        x, y = move
        self.pieces[x][y] = color

        # For disjoint set
        
        action_index = x*self.n + y
        for dir_x, dir_y in self.__directions:  #檢查6方向鄰居
            nx = x+dir_x
            ny = y+dir_y
            if self.is_valid_pos(nx, ny):
                if self.pieces[nx][ny] == self.pieces[x][y]:    #此步和鄰居同色
                    neighbor_index = nx*self.n + ny
                    self.disjoint_set.union(action_index, neighbor_index)

    def check_player_win_DFS(self, player):
        visited = set()
        stack = []
        if player == 1:
            for y in range(self.n): #最上排每個位置
                if self.pieces[0][y] == player:
                    cur_x, cur_y = 0, y #start
                    stack.append((cur_x, cur_y))
                    visited.add((cur_x, cur_y))
                    while len(stack) > 0:
                        cur_x, cur_y = stack.pop()
                        for dir_x, dir_y in self.__directions:  #檢查6方向鄰居
                            nx = cur_x+dir_x
                            ny = cur_y+dir_y
                            if self.is_valid_pos(nx, ny):
                                if self.pieces[nx][ny] == player and ((nx, ny) not in visited): #鄰居不在visited中且和player同色
                                    stack.append((nx, ny))
                                    visited.add((nx, ny))
                                    if nx == self.n-1: #到最底部
                                        return True #win
            return False
        elif player == -1:
            for x in range(self.n): 
                if self.pieces[x][0] == player:
                    cur_x, cur_y = x, 0 
                    stack.append((cur_x, cur_y))
                    visited.add((cur_x, cur_y))
                    while len(stack) > 0:
                        cur_x, cur_y = stack.pop()
                        for dir_x, dir_y in self.__directions:  #檢查6方向鄰居
                            nx = cur_x+dir_x
                            ny = cur_y+dir_y
                            if self.is_valid_pos(nx, ny):
                                if self.pieces[nx][ny] == player and ((nx, ny) not in visited): #鄰居不在visited中且和player同色
                                    stack.append((nx, ny))
                                    visited.add((nx, ny))
                                    if ny == self.n-1:  #到最右
                                        return True
            return False
        else:
            print("check_player_win: invalid player!")

    def check_player_win_DisjointSet(self, player):
        if player == 1:
            for i in range(self.n):
                for j in range(self.n):
                    index_a = i
                    index_b = self.n * (self.n-1) + j
                    if self.disjoint_set.isSameGroup(index_a,index_b):
                        return True
        elif player == -1:
            for i in range(self.n):
                for j in range(self.n):
                    index_a = i * self.n
                    index_b = self.n * j + (self.n-1)
                    if self.disjoint_set.isSameGroup(index_a,index_b):
                        return True
        else:
            print("check_player_win: invalid player!")


