#!/usr/bin/env python

descriptions = ['Graphite', 
                'FLiBe w/ Natural Li', 
                'FLiBe w/ Enriched Li']

titles = {'Graphite' : 'graphite', 
          'FLiBe w/ Natural Li' : 'flibe-natural',
          'FLiBe w/ Enriched Li' : 'flibe-enriched'}
                
densities = {'Graphite' : -1.69 ,
             'FLiBe w/ Natural Li' : -2.1228808, 
             'FLiBe w/ Enriched Li' : -2.1228808} # taken at 750 C
                       
lithium_isotope_fractions= {'Li-6':0.0005, 'Li-7':0.9995}

material_cards = {
'Graphite' : 
'm2   6000   1   $ Elemental Carbon',

'FLiBe w/ Natural Li' : 
'm2   3006   '+ str(0.075 * 2) + '   $ Elemental Lithium \n' + \
'     3007   '+ str(0.925 * 2) + '                       \n' + \
'     4009   1   $ Elemental Beryllium \n' + \
'     9019   4   $ Elemental Fluorine',
'FLiBe w/ Enriched Li' :
'm2   3006   ' + str(lithium_isotope_fractions['Li-6'] * 2) + ' $ Lithium-6 \n' + \
'     3007   ' + str(lithium_isotope_fractions['Li-7'] * 2) + ' $ Lithium-7 \n' + \
'     4009   1   $ Elemental Beryllium \n' + \
'     9019   4   $ Elemental Fluorine'
}

radii = ['000.1',
         '000.2',
         '000.3',
         '000.4',
         '000.5', 
         '001.0',
         '001.5',
         '002.0',
         '003.0',
         '004.0', 
         '005.0', 
         '007.5', 
         '010.0', 
         '012.5',
         '015.0',
         '020.0',
         '025.0',
         '030.0',
         '040.0',
         '050.0']

import os         
import pickle
import pyexpander

input_dict = {}
for moderator in descriptions:
    for r in radii:
        handle = titles[moderator] + '-' + r + 'cm'

        input_dict['description'] = moderator
        input_dict['density'] = densities[moderator]
        input_dict['material_card'] = material_cards[moderator]
        input_dict['radius'] = r
        input_dict['particles_per_cycle'] = 75000
        input_dict['criticality_guess'] = 0.50
        input_dict['skipped_cycles'] = 50
        input_dict['total_cycles'] = 150

        data_filename = os.path.join('.','data', handle + '.mcnp.p')
        data = open(data_filename, 'wb')        
        pickle.dump(input_dict, data)
        data.close()

        input_filename = os.path.join('.','input-files', handle + '.mcnp.i')
        
        invoc = 'expander.py --eval '
        invoc += '\'data = \"' + data_filename  + '\"\''
        invoc += ' -f ./template/template.pe > ' + input_filename 
        print invoc
        os.system(invoc)
