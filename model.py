import torch
import numpy as np
from tqdm import tqdm

def AF() :
    return 0

def correlation(domain, user, aux_name, sample, sample_ratio):
    device = 'cuda:0'
    total_average = domain[domain.rating != 0].rating.mean()

    user_sum = domain.groupby('user').sum()
    user_count = domain[domain.rating != 0].groupby('user').count()

    user_average = np.zeros(len(user))
    user_average[user_count.index] = user_sum.rating[user_count.index] / user_count.rating[user_count.index]

    pearson_correlation = np.zeros((len(user), len(user)))

    domain_table = domain.pivot_table(index='user', columns='item', values='rating').fillna(0).values
    user_average_expansion = user_average.reshape(len(user_average), 1) + np.zeros((1, domain_table.shape[1]))

    domain_table = torch.FloatTensor(domain_table).to(device)
    user_average_expansion = torch.FloatTensor(user_average_expansion).to(device)
    pearson_correlation = torch.FloatTensor(pearson_correlation).to(device)
    make_dim = torch.zeros(len(domain_table), 1).to(device)

    for i in tqdm(user_count.index):
        user_i = make_dim + domain_table[i]
        user_i_item = domain_table[i].nonzero()  # item num
        y = (user_i[:, user_i_item] - domain_table[:, user_i_item]) != user_i[:, user_i_item]
        user_i_average = torch.Tensor(user_average_expansion.shape).fill_(user_average[i]).to(device)
        diff_i = (user_i - user_i_average)[:, user_i_item]
        diff_j = (domain_table - user_average_expansion)[:, user_i_item]
        denom = torch.sqrt(((diff_i ** 2) * y).sum(axis=1) * ((diff_j ** 2) * y).sum(axis=1) + 1e-8)
        numer = ((diff_i * diff_j) * y).sum(axis=1)
        pearson_correlation[i] = numer.view(-1) / denom.view(-1)
        #print(i)
        #print(pearson_correlation[i])
    torch.save(pearson_correlation, f'./dataset/{aux_name}_pearson_correlation_{sample}_{sample_ratio}.pt')

def CDCF(aux_name, ) :
    arts_pearson_correlation = torch.load('./dataset/home_pearson_correlation.pt')

    arts_pearson_correlation = torch.FloatTensor(arts_pearson_correlation.cpu())

    k = 5
    arts_topk_value = torch.topk(arts_pearson_correlation, k)[0]
    arts_topk_index = torch.topk(arts_pearson_correlation, k)[1]

    pivot_table = arts_append.pivot_table(index='user', columns='item', values='rating').fillna(0)  # 4725, 74735

    difference = (pivot_table != 0).astype(float) * (pivot_table - user_average.reshape(len(user_average), 1))

    user_average[user_average == 0] = total_average
    return 0
