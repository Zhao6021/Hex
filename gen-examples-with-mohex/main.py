from mohex_gen_examples import genExamples
from mohex_gen_examples import saveExamples
from utils import *
import time

args = dotdict({
    'boardSize' : 6,
    'numPlay' : 400, #number of mohex play to generate examples
    'numDfpnThreads' : 1,
})

time_start = time.time()
examples=genExamples(args)
time_end = time.time()
print("boardSize= ", args.boardSize)
print("numPlay= ", args.numPlay)
print("numDfpnThreads= ", args.numDfpnThreads)
print("time= ", time_end-time_start)
print("num_examples= ", len(examples))
saveExamples(examples,str(args.boardSize)+"*"+str(args.boardSize)+"_"+str(len(examples)))