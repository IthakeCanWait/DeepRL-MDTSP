from policy_mdmtsp import Policy, action_sample, get_reward
import torch
from torch_geometric.data import Data
from torch_geometric.data import Batch
import numpy as np
import matplotlib.pyplot as plt
from vrp_mdtsp import entrance
from test import test


if __name__ == '__main__':

    dev = 'cuda' if torch.cuda.is_available() else 'cpu'

    n_agent = 5
    n_nodes = [100,200,300,400,500,600,700,800,900,1000]
    batch_size = 100
    seeds = [1, 2, 3]

    # load net
    policy1 = Policy(in_chnl=2, hid_chnl=64, n_agent=n_agent, key_size_embd=64,
                    key_size_policy=64, val_size=64, clipping=10, dev=dev)
    policy2 = Policy(in_chnl=2, hid_chnl=64, n_agent=n_agent, key_size_embd=64,
                    key_size_policy=64, val_size=64, clipping=10, dev=dev)
    path1 = './saved_model_MDMTSP/{}.pth'.format(str(50) + '_' + str(n_agent) + '_lr' + str(0.0001) + '_cmpnn')
    path2 = './saved_model_MDMTSP/{}.pth'.format(str(50) + '_' + str(n_agent) + '_lr' + str(0.0001) + '_cmpnn_goodData')
    
    policy1.load_state_dict(torch.load(path1, map_location=torch.device(dev)))
    policy2.load_state_dict(torch.load(path2, map_location=torch.device(dev)))

    for size in n_nodes:
        #testing_data = torch.load('./testing_data/testing_data_' + str(size) + '_' + str(batch_size))
        testing_data = torch.load('./testing_data/testing_data_Neyman_' + str(size) + '_' + str(batch_size))
        results_per_seed_model1 = []
        results_per_seed_model2 = []
        for seed in seeds:
            print('Size:', size, 'Seed:', seed)
            torch.manual_seed(seed)
            objs_model1 = []
            objs_model2 = []
            for j in range(batch_size):
                # data = torch.rand(size=[1, size, 2])  # [batch, nodes, fea], fea is 2D location
                data = testing_data[j].unsqueeze(0)
                # testing
                obj_model1 = test(policy1, data, dev, plot=0)
                objs_model1.append(obj_model1)
                print('MODEL1: Max sub-tour length for instance', j, 'is', obj_model1, 'Mean obj so far:', format(np.array(objs_model1).mean(), '.4f'))

                obj_model2 = test(policy2, data, dev, plot=0)
                objs_model2.append(obj_model2)
                print('MODEL2: Max sub-tour length for instance', j, 'is', obj_model2, 'Mean obj so far:', format(np.array(objs_model2).mean(), '.4f'), '\n')
            results_per_seed_model1.append(format(np.array(objs_model1).mean(), '.4f'))
            results_per_seed_model2.append(format(np.array(objs_model2).mean(), '.4f'))
        print('(Model1) Size:', size, results_per_seed_model1)
        print('(Model2) Size:', size, results_per_seed_model2)



