from policy_mdmtsp import Policy, action_sample, get_reward
import torch
from torch_geometric.data import Data
from torch_geometric.data import Batch


def validate(instances, p_net, no_agent, device, plot=0):

    batch_size = instances.shape[0]
    adj = torch.ones([batch_size, instances.shape[1], instances.shape[1]])  # adjacent matrix

    # get batch graphs instances list
    instances_list = [Data(x=instances[i], edge_index=torch.nonzero(adj[i]).t()) for i in range(batch_size)]
    # generate batch graph
    batch_graph = Batch.from_data_list(data_list=instances_list).to(device)

    # get pi
    pi = p_net(batch_graph, n_nodes=instances.shape[1], n_batch=batch_size)

    # sample action and calculate log probs
    action, log_prob = action_sample(pi)

    # get reward for each batch
    reward = get_reward(action, instances, no_agent, plot)  # reward: tensor [batch, 1]
    print('Validation result:', format(sum(reward)/batch_size, '.4f'))

    return sum(reward)/batch_size


if __name__ == '__main__':
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    torch.manual_seed(2)

    n_agent = 5
    n_nodes = 50
    n_batch = 1

    data = torch.load('./validation_data/validation_data_' + str(n_nodes) + '_' + str(n_batch))

    policy = Policy(in_chnl=2, hid_chnl=64, n_agent=n_agent, key_size_embd=64,
                  key_size_policy=64, val_size=64, clipping=10, dev=dev)
    path = './saved_model_MDMTSP/{}.pth'.format(str(50) + '_' + str(n_agent) + '_lr' + str(0.0001) + '_cmpnn')
    policy.load_state_dict(torch.load(path, map_location=torch.device(dev)))
    validate(data, policy, n_agent, dev, plot=0)
