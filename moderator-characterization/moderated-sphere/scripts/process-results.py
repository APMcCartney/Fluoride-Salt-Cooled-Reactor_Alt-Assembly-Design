#!/usr/bin/env python

import os
import sys
import importlib

sys.path.append(os.path.join('..', '..', 'general-scripts', 'mcnp'))
aggregate = importlib.import_module('aggregate-output')

l = os.listdir(os.path.join('.','input-files'))
o = []
p = []

for f in l:
    o.append(os.path.join('.','output-files',f[0:-1]+'o'))
    p.append(os.path.join('.','data',f[0:-1]+'p'))

aggregate.output(output_filenames = o, pickle_filenames = p)
