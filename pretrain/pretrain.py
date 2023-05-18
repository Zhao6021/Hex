import os
from NNetForPretrain import NNetWrapper as nn
from pickle import Unpickler
from random import shuffle
import sys
import torch
import torch.nn

examples_file_name = "pretrain/6_6_13445.examples"
board_size = 6

examples=[]
#load train examples
if not os.path.isfile(examples_file_name):
    print("file not found!")
    sys.exit()
else:
    with open(examples_file_name, "rb") as f:
        print("loading...")
        examples = Unpickler(f).load()
        print("loading examples done!")
#training
nnet = nn(board_size)
shuffle(examples)
nnet.train(examples)
nnet.save_checkpoint('pretrain/pre_model','pretrain.pth.tar')

"""
nnet2 = nn(board_size)

#print(nnet.nnet.conv1.weight)
#print(nnet2.nnet.conv1.weight)
state = nnet.nnet.state_dict()
#print(state['conv1.weight'])

nnet2.load_checkpoint('pretrain/pre_model','pretrain.pth.tar')
state2 = nnet2.nnet.state_dict()



print(nnet2.nnet.fc3.weight)
nnet2.nnet.fc3 = torch.nn.Linear(512,49)
print(nnet2.nnet.fc3.weight)

print(state2['fc3.weight'].shape)
state2['fc3.weight'] = torch.rand((49,512))
print(state2['fc3.weight'].shape)
"""