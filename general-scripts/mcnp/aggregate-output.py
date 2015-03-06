#!/usr/bin/env python

import os
import sys
import importlib
import pickle
import pandas

sys.path.append(os.path.join('..', '..', 'general-scripts', 'mcnp'))
distill = importlib.import_module('distill-output')

def output(output_filenames, pickle_filenames):
    data_file = open(pickle_filenames[0], 'rb+')
    inp_dict = pickle.load(data_file)
    out_dict = distill.output(output_filenames[0])
    pickle.dump(out_dict, data_file)
    data_file.truncate()
    data_file.close()
    total_dict = inp_dict.copy()
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
        total_dict.update(out_dict)
        aggregate_df.loc[i,:] = total_dict.values()
        
    aggregate_df.sort(['description', 'radius'], ascending = [True, True]).reset_index().drop('material_card', 1).to_csv('data.csv')

