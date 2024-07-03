from heapq import *

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

    def get_neighbors(self, pos, player, with_weights=False):   # with_weights is for alpha-beta player
        x, y = pos
        neighbors = []
        for dir_x, dir_y in self.__directions:
            nx, ny = (x + dir_x, y + dir_y)
            if self.is_valid_pos(nx, ny):
                if with_weights:
                    if self.pieces[nx][ny] != -player:
                        neighbors.append(((nx, ny), int(self.pieces[nx][ny] == 0)))
                else:
                    if self.pieces[nx][ny] == player:
                        neighbors.append((nx, ny))
        return neighbors

    def dfs_search(self, start_x, start_y, player):
        if self.pieces[start_x][start_y] != player:
            return False
        cur_x, cur_y = start_x, start_y #start
        visited = set()
        stack = []
        stack.append((cur_x, cur_y))
        visited.add((cur_x, cur_y))
        while len(stack) > 0:
            cur_x, cur_y = stack.pop()
            for neighbor in self.get_neighbors((cur_x, cur_y), player):  #檢查6方向鄰居
                if neighbor not in visited: #鄰居不在visited中
                    if (player == 1 and neighbor[0] == self.n-1) or (player == -1 and neighbor[1] == self.n-1):
                        return True
                    visited.add(neighbor) 
                    stack.append(neighbor)
        return False
    
    def count_to_connect(self):
        """ 
        from https://github.com/aebrahimian/alpha-zero-hex
        this is for alpha-beta player
        """    
        shortest = (float('inf'), None)
        for y in range(self.n):
            if self.pieces[0][y] == -1:
                continue
            cost, path = self.shortest_path((0, y))
            if cost < shortest[0]:
                shortest = (cost, path)
        
        if shortest[0] == float('inf'):
            return (self.n**2, shortest[1])

        return shortest

   
    def shortest_path(self, source):
        """ 
        from https://github.com/aebrahimian/alpha-zero-hex
        this is for alpha-beta player
        """         
        source_cost = int(self.pieces[source[0]][source[1]] == 0)
        shortest = (float("inf"), None)
        q, seen, mins = [(source_cost, source, [])], set(), {source: source_cost}
        while q:
            (cost,v1,path) = heappop(q)
            if v1 not in seen:
                seen.add(v1)
                path = [*path, v1]
                if v1[0] == self.n-1 and cost < shortest[0]:
                    shortest = (cost, path)

                for v2, c in self.get_neighbors(v1, 1, with_weights=True):
                    if v2 in seen: continue
                    prev = mins.get(v2, None)
                    next = cost + c
                    if prev is None or next < prev:
                        mins[v2] = next
                        heappush(q, (next, v2, path))

        return shortest