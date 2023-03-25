import os
from NNetForPretrain import NNetWrapper as nn
from pickle import Unpickler
from random import shuffle
import sys

examples_file_name = "6_6_13445.examples"
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