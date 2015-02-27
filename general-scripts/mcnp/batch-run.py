import os
import multiprocessing as mp
    
def run(input_filenames, output_filenames, run_filenames, source_filenames, threads):
    mcnp_invocations = []
    for j in range(len(input_filenames)):
        invoc = 'mcnp6'
        invoc += ' i=' + input_filenames[j] 
        invoc += ' o=' + output_filenames[j]
        invoc += ' r=' + run_filenames[j]
        invoc += ' s=' + source_filenames[j]
        mcnp_invocations.append(invoc)
        
    mcnp_instances = mp.Pool(processes=threads)
    mcnp_instances.map(os.system, mcnp_invocations)