#!/usr/bin/env python

import os
import sys
import importlib

sys.path.append(os.path.join('..', '..', 'general-scripts', 'mcnp'))
aggregate = importlib.import_module('aggregate-output')

l = os.listdir(os.path.join('.','input-files','tier1'))
o = []
p = []

for f in l:
    o.append(os.path.join('.','output-files','tier1',f[0:-1]+'o'))
    p.append(os.path.join('.','data','tier1',f[0:-1]+'p'))

data_df = aggregate.output(output_filenames = o, pickle_filenames = p)
data_df.to_csv(os.path.join('.','data','tier1','data.csv'))
