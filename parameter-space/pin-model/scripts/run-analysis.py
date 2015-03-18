#!/usr/bin/env python

import os
import sys
import importlib

sys.path.append(os.path.join('..', '..', 'general-scripts', 'mcnp'))
batch = importlib.import_module('batch-run')

l = os.listdir(os.path.join('.','input-files', 'tier1'))
i = []
o = []
r = []
s = []

for f in l:
    i.append(os.path.join('.','input-files','tier1',f))
    o.append(os.path.join('.','output-files','tier1',f[0:-1]+'o'))
    r.append(os.path.join('.','output-files','tier1',f[0:-1]+'r'))
    s.append(os.path.join('.','output-files','tier1',f[0:-1]+'s'))
  
batch.run(input_filenames = i, output_filenames = o, run_filenames = r, source_filenames = s, threads = 4)
