
import numpy as np
import torch
from utils.posdict import PosDict
import bitstruct

def pos_list_to_tensor(pos_list: list) -> torch.tensor:
    res = np.array([pos_list[0].get_as_vector()], dtype='float32')
    for i in range(1,len(pos_list)):
        nexti = np.array([pos_list[i].get_as_vector()], dtype='float32')
        res = np.vstack((res, nexti))
    res = torch.from_numpy(res)
    return res


def pos_dict_to_prob_dict(pos_dict: PosDict):
    prob_dict = {}
    for key, arr in pos_dict.get_dict().items():
        prob_dict[key] = arr[0]/arr[1]
    return prob_dict


def pos_vec_turn_normal_to_bias(pos_vec):
    pos_vec[0] = pos_vec[0]*2 - 1
    return pos_vec


def pos_biased_tup_to_byte_arr(pos_tup):
    return bitstruct.pack('s3' * len(pos_tup), *pos_tup)


def byte_arr_to_pos_biased_tup(byte_arr):
    return bitstruct.unpack('s3' * 33, * byte_arr)