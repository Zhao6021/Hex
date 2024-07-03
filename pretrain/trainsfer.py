from NNetForPretrain import NNetWrapper as nn
import torch
import torch.nn
import math

ori_size = 6
tar_size = 7
method = 1

p_nnet = nn(ori_size)
p_nnet.load_checkpoint('pretrain/models',str(ori_size)+'_pretrain.pth.tar')
p_state = p_nnet.nnet.state_dict()
n_state = p_nnet.nnet.state_dict()

if method == 1: #大小不同的層不做transfer
    print('Transfering "fc3.weight"...')
    n_state['fc3.weight'] = torch.FloatTensor(tar_size*tar_size, 512).uniform_(-1*math.sqrt(1/512), math.sqrt(1/512))
    print('Transfering "fc3.bias"...')
    n_state['fc3.bias'] = torch.FloatTensor(tar_size*tar_size).uniform_(-1*math.sqrt(1/512), math.sqrt(1/512))
    print('Transfering "fc1.weight"...')
    n_state['fc1.weight'] = torch.FloatTensor(1024,(tar_size-4)*(tar_size-4)*512).uniform_(-1*math.sqrt(1/((tar_size-4)*(tar_size-4)*512)), math.sqrt(1/((tar_size-4)*(tar_size-4)*512)))

elif method == 2:   #將source中的參數transfer到相似的對應位置(左上)
    print('Transfering "fc3.weight"...')
    n_state['fc3.weight'] = torch.FloatTensor(tar_size*tar_size, 512).uniform_(-1*math.sqrt(1/512), math.sqrt(1/512))
    for i in range(p_state['fc3.weight'].shape[0]):
        dif = tar_size - ori_size
        row = int(i/ori_size)
        add = dif*row
        n_state['fc3.weight'][i+add] = p_state['fc3.weight'][i]

    print('Transfering "fc3.bias"...')
    n_state['fc3.bias'] = torch.FloatTensor(tar_size*tar_size).uniform_(-1*math.sqrt(1/512), math.sqrt(1/512))
    for i in range(p_state['fc3.bias'].shape[0]):
        dif = tar_size - ori_size
        row = int(i/ori_size)
        add = dif*row
        n_state['fc3.bias'][i+add] = p_state['fc3.bias'][i]

    print('Transfering "fc1.weight"...')
    n_state['fc1.weight'] = torch.FloatTensor(1024,(tar_size-4)*(tar_size-4)*512).uniform_(-1*math.sqrt(1/((tar_size-4)*(tar_size-4)*512)), math.sqrt(1/((tar_size-4)*(tar_size-4)*512)))
    for i in range(p_state['fc1.weight'].shape[0]):
        for j in range(p_state['fc1.weight'].shape[1]): #j=9    11  6
            dif = tar_size - ori_size   #dif= 2  2  1
            nth_element = j%((ori_size-4)*(ori_size-4)) #nth_element = 1    3   2
            nth_group = int(j/((ori_size-4)*(ori_size-4)))  #nth_group = 2     2    1
            tar = (nth_group*((tar_size-4)*(tar_size-4)))+nth_element+(dif*int(nth_element/(ori_size-4)))   #2*16+1+2*0  2*16+3+2*1  1*9+2+1*1
            n_state['fc1.weight'][i][tar] = p_state['fc1.weight'][i][j]

elif method == 3:   #將source中的參數transfer到相似的對應位置(中央)
    print('Transfering "fc3.weight"...')
    n_state['fc3.weight'] = torch.FloatTensor(tar_size*tar_size, 512).uniform_(-1*math.sqrt(1/512), math.sqrt(1/512))
    for i in range(p_state['fc3.weight'].shape[0]):
        dif = tar_size - ori_size
        row = int(i/ori_size)
        add = dif*row
        move = int(dif/2) + (tar_size*int(dif/2))
        n_state['fc3.weight'][i+add+move] = p_state['fc3.weight'][i]

    print('Transfering "fc3.bias"...')
    n_state['fc3.bias'] = torch.FloatTensor(tar_size*tar_size).uniform_(-1*math.sqrt(1/512), math.sqrt(1/512))
    for i in range(p_state['fc3.bias'].shape[0]):
        dif = tar_size - ori_size
        row = int(i/ori_size)
        add = dif*row
        move = int(dif/2) + (tar_size*int(dif/2))
        n_state['fc3.bias'][i+add+move] = p_state['fc3.bias'][i]

    print('Transfering "fc1.weight"...')
    n_state['fc1.weight'] = torch.FloatTensor(1024,(tar_size-4)*(tar_size-4)*512).uniform_(-1*math.sqrt(1/((tar_size-4)*(tar_size-4)*512)), math.sqrt(1/((tar_size-4)*(tar_size-4)*512)))
    for i in range(p_state['fc1.weight'].shape[0]):
        for j in range(p_state['fc1.weight'].shape[1]): 
            dif = tar_size - ori_size   
            nth_element = j%((ori_size-4)*(ori_size-4)) 
            nth_group = int(j/((ori_size-4)*(ori_size-4)))  
            tar = (nth_group*((tar_size-4)*(tar_size-4)))+nth_element+(dif*int(nth_element/(ori_size-4)))   
            move = int(dif/2) + ((tar_size-4)*int(dif/2))
            n_state['fc1.weight'][i][tar+move] = p_state['fc1.weight'][i][j]

elif method == 4:   #不按照對應位置轉移
    print('Transfering "fc3.weight"...')
    n_state['fc3.weight'] = torch.FloatTensor(tar_size*tar_size, 512).uniform_(-1*math.sqrt(1/512), math.sqrt(1/512))
    for i in range(p_state['fc3.weight'].shape[0]):
        n_state['fc3.weight'][i] = p_state['fc3.weight'][i]

    print('Transfering "fc3.bias"...')
    n_state['fc3.bias'] = torch.FloatTensor(tar_size*tar_size).uniform_(-1*math.sqrt(1/512), math.sqrt(1/512))
    for i in range(p_state['fc3.bias'].shape[0]):
        n_state['fc3.bias'][i] = p_state['fc3.bias'][i]

    print('Transfering "fc1.weight"...')
    n_state['fc1.weight'] = torch.FloatTensor(1024,(tar_size-4)*(tar_size-4)*512).uniform_(-1*math.sqrt(1/((tar_size-4)*(tar_size-4)*512)), math.sqrt(1/((tar_size-4)*(tar_size-4)*512)))
    for i in range(p_state['fc1.weight'].shape[0]):
        for j in range(p_state['fc1.weight'].shape[1]): 
            n_state['fc1.weight'][i][j] = p_state['fc1.weight'][i][j]

torch.save({'state_dict': n_state,},'pretrain/models/'+str(ori_size)+'to'+str(tar_size)+'transfer_method'+str(method)+'.pth.tar')

'''
nnet2 = nn(tar_size)
nnet2.load_checkpoint('pretrain/models',str(ori_size)+'to'+str(tar_size)+'transfer.pth.tar')
state2 = nnet2.nnet.state_dict()
print(p_state['fc3.weight'].shape)
print(p_state['fc3.bias'].shape)
print(p_state['fc1.weight'].shape)
print("-----------------------------")
print(state2['fc3.weight'].shape)
print(state2['fc3.bias'].shape)
print(state2['fc1.weight'].shape)
print("-----------------------------")
print(p_state['fc1.weight'][0][0])
print(state2['fc1.weight'][0][5])
print()
print(p_state['fc1.weight'][0][3])
print(state2['fc1.weight'][0][10])
print()
print(p_state['fc1.weight'][0][4])
print(state2['fc1.weight'][0][21])
print()
print(p_state['fc1.weight'][2][7])
print(state2['fc1.weight'][2][26])
print()
print(p_state['fc1.weight'][1023][11])
print(state2['fc1.weight'][1023][42])
print()
print("-----------------------------")
print(p_state['fc3.weight'][0][0])
print(state2['fc3.weight'][9][0])
print()
print(p_state['fc3.weight'][15][50])
print(state2['fc3.weight'][28][50])
print()
print(p_state['fc3.weight'][35][510])
print(state2['fc3.weight'][54][510])
print()'''