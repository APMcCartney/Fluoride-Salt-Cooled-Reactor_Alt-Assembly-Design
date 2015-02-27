#!/usr/bin/env python

import os
import sys
import importlib

sys.path.append(os.path.join('..', '..', 'general-scripts', 'mcnp'))
batch = importlib.import_module('batch-run')

i = [os.path.join('.', 'input-files', 'bare-sphere.mcnp.i')]
o = [os.path.join('.', 'output-files', 'bare-sphere.mcnp.o')]
r = [os.path.join('.', 'output-files', 'bare-sphere.mcnp.r')]
s = [os.path.join('.', 'output-files', 'bare-sphere.mcnp.s')]

batch.run(input_filenames = i, output_filenames = o, run_filenames = r, source_filenames = s, threads = 1)
