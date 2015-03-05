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

margins = ['0.125', 
           '0.250',
           '0.375',
           '0.500',
           '0.625',
           '0.750', 
           '0.875', 
           '1.000', 
           '1.250', 
           '1.500',
           '1.750',
           '2.000',
           '2.500',
           '3.000']

import os         
import pickle
import pyexpander

input_dict = {}
for moderator in descriptions:
    for m in margins:
        handle = titles[moderator] + '-' + m + 'cm'

        input_dict['description'] = moderator
        input_dict['density'] = densities[moderator]
        input_dict['material_card'] = material_cards[moderator]
        input_dict['margin'] = m
        input_dict['particles_per_cycle'] = 75000
        input_dict['criticality_guess'] = 1.20
        input_dict['skipped_cycles'] = 10
        input_dict['total_cycles'] = 50

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
