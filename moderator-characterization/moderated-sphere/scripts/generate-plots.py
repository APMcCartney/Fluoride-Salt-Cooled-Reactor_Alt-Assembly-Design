#!/usr/bin/env python

# A python wrapper to call the R script from command line

import os

myRscript_path = os.path.join('.','scripts','generate-plots.R')
os.system('Rscript ' + myRscript_path)
