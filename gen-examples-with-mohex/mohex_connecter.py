import subprocess
import sys
import numpy as np

class Mohex_Connecter:
    def __init__(self,board_size):
        self.p=subprocess.Popen("./mohex",shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        self.board_size=board_size
        self.board_init(board_size)
    
    def kill(self):
        self.p.kill()

    def board_init(self,board_size):
        '''
        board_size is a int
        '''
        cmd=bytes('boardsize '+str(board_size)+'\n',encoding='utf-8')
        self.p.stdin.write(cmd)
        self.p.stdin.flush()
        _=self.read_out_from_mohex()

    def read_out_from_mohex(self):
        msg=self.p.stdout.readline().decode('utf-8')
        while msg[0]!='=':
            #print('waiting')
            msg=self.p.stdout.readline().decode('utf-8')
            #print(msg)
        return msg
    
    #mohex commands
    def mohex_showboard(self):
        cmd_showboard=bytes('showboard\n',encoding='utf-8')
        self.p.stdin.write(cmd_showboard)
        self.p.stdin.flush()
        for i in range(self.board_size+6):
            print(self.p.stdout.readline())

    def mohex_undo(self):
        cmd_undo=bytes('undo\n',encoding='utf-8')
        self.p.stdin.write(cmd_undo)
        self.p.stdin.flush()
        _=self.read_out_from_mohex()

    def mohex_genmove(self, color):
        '''
        send genmove cammand to mohex
        form as 'genmove {color}'
        '''
        cmd_genmove = bytes('genmove %s\n'%color,encoding='utf-8')
        self.p.stdin.write(cmd_genmove)
        self.p.stdin.flush()
        move = self.read_out_from_mohex()[2:-1]
        move = move.split(' ')
        return move

    def mohex_playmove(self,color,pos):
        '''
        send player move cammand to mohex
        form as 'play {color} {pos}'
        '''
        #print('azg:'+pos)
        cmd_play=bytes('play %s %s\n'%(color,pos),encoding='utf-8')
        self.p.stdin.write(cmd_play)
        self.p.stdin.flush()
        _=self.read_out_from_mohex()

    def mohex_solve_state(self):
        cmd_solve_state=bytes('dfpn-solve-state\n',encoding='utf-8')
        self.p.stdin.write(cmd_solve_state)
        self.p.stdin.flush()
        answer=self.read_out_from_mohex()[2]
        #print(answer)
        return answer
    
    def mohex_solve(self,color):
        cmd_solver=bytes('dfpn-solver-find-winning '+color+'\n',encoding='utf-8')
        self.p.stdin.write(cmd_solver)
        self.p.stdin.flush()
        #print(self.mohex_showboard())
        solves=self.read_out_from_mohex()
        if len(solves)<=3:
            return []
        solves=solves[3:-1].split(' ')
        return solves

    def mohex_set_dfpn_threads(self, num):
        cmd_set_dfpn_threads=bytes('param_dfpn threads '+str(num)+'\n',encoding='utf-8')
        self.p.stdin.write(cmd_set_dfpn_threads)
        self.p.stdin.flush()
        _ = self.read_out_from_mohex()

    def mohex_vc_get_mustplay(self, color):
        cmd_vc_get_mustplay=bytes('vc-get-mustplay '+color+'\n',encoding='utf-8')
        self.p.stdin.write(cmd_vc_get_mustplay)
        self.p.stdin.flush()
        pos = self.read_out_from_mohex()
        if len(pos)<=3:
            return []
        pos=pos[3:-1].split(' ')
        pos = [i for i in pos if i!='x']
        #print(pos)
        return pos

    def mohex_all_legal_moves(self):
        cmd_legal_moves = bytes('all_legal_moves\n',encoding='utf-8')
        self.p.stdin.write(cmd_legal_moves)
        self.p.stdin.flush()
        moves = self.read_out_from_mohex()
        moves = moves[3:-1].split(' ')
        if moves[0] == 'resign':
            moves.remove('resign')
        if moves[0] == 'swap-pieces':
            moves.remove('swap-pieces')
        return moves