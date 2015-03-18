#!/usr/bin/env python

import os
import sys
import importlib
import pickle
import pandas
import copy
import re

sys.path.append(os.path.join('..', '..', 'general-scripts', 'mcnp'))
distill = importlib.import_module('distill-output')

def __flatten(myDict):
    flatDict = copy.deepcopy(myDict)
    for key in myDict.keys():
        if type(myDict[key]) == list:
            for i in range(len(myDict[key])):
                newKey = key + '-' + str(i)
                flatDict[newKey] = flatDict[key][i]
            del flatDict[key]
        if type(myDict[key]) == dict:
            flatDict[key] = __flatten(flatDict[key])
            for oldKey in flatDict[key]:
                newKey = key + '-' + oldKey
                flatDict[newKey] = flatDict[key][oldKey]
            del flatDict[key]
    return flatDict

def __drop_material_cards(myDict):
    card_keys = filter(lambda a: re.search(r"card", a) != None, myDict.keys())
    for key in card_keys:
        del myDict[key]

def output(output_filenames, pickle_filenames):
    data_file = open(pickle_filenames[0], 'rb+')
    inp_dict = pickle.load(data_file)
    out_dict = distill.output(output_filenames[0])
    pickle.dump(out_dict, data_file)
    data_file.truncate()
    data_file.close()
    total_dict = inp_dict.copy()
    total_dict = __flatten(total_dict)
    __drop_material_cards(total_dict)
    total_dict.update(out_dict)

    aggregate_df = pandas.DataFrame(columns = total_dict.keys())
    aggregate_df.loc[0,:] = total_dict.values()
    
    for i in range(1, len(output_filenames)):
        data_file = open(pickle_filenames[i], 'rb+')
        inp_dict = pickle.load(data_file)
        out_dict = distill.output(output_filenames[i])
        pickle.dump(out_dict, data_file)
        data_file.truncate()
        data_file.close()
        total_dict = inp_dict.copy()
        total_dict = __flatten(total_dict)
        __drop_material_cards(total_dict)
        total_dict.update(out_dict)
        aggregate_df.loc[i,:] = total_dict.values()
    
    return aggregate_df

