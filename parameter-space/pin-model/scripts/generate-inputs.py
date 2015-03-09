#!/usr/bin/env python

import numpy as np
import pickle
import os

__test_height = 3.0 # cm

__fuel = ['uranium-oxide',
        'uranium-carbide',
        'uranium-nitride']

__abrev = {'uranium-oxide':'UO2',
           'uranium-carbide':'UC',
           'uranium-nitride':'UN'}

__poison = [None]

__density = {'uranium-oxide' : -10.86583,
             'uranium-carbide' : -13.43672,
             'uranium-nitride' : -14.16122,
             'helium' : -0.000041031,
             'SiC-SiC' : -2.8,
             'flibe' : -2.1228808,
             'air' : -0.0001
             }

__card = {'uranium-oxide' :   '  92238 0.94939273  $ Uranium-238 \n' + \
                           '        92235 0.05060727  $ Uranium-235 \n' + \
                           '         8000 2.00000000  $ Natural Oxygen' ,
          'uranium-carbide' :   '  92238 0.94939273  $ Uranium-238 \n' + \
                             '        92235 0.05060727  $ Uranium-235 \n' + \
                             '         6000 1.00000000  $ Natural Carbon' ,
          'uranium-nitride' :   '  92238 0.94939273  $ Uranium-238 \n' + \
                             '        92235 0.05060727  $ Uranium-235 \n' + \
                             '         7000 1.00000000  $ Natural Nitrogen' ,
          'helium' : '   2004 1.00000000  $ Natural Helium',
          'SiC-SiC' :   '  14000 1.00000000  $ Natural Silicon \n' + \
                     '         6000 1.00000000  $ Natural Carbon',
          'flibe' :   '   3006 0.001  $ Lithium-6 \n' + \
                   '         3007 1.999 $ Lithium-7 \n' + \
                   '         4009 1   $ Elemental Beryllium \n' + \
                   '         9019 4   $ Elemental Fluorine',
          'air' :   '    7000  1.56168  $ Natural Nitrogen \n' + \
                 '          8000  0.41892  $ Natural Oxygen \n' + \
                 '        18040  0.00934  $ Almost Natural Argon'
          }

__mat = {}
__mat['fuel'] = {}
__mat['fuel']['ID'] = ['0001']
__mat['gap'] = {}
__mat['gap']['ID'] = ['0011']
__mat['gap']['density'] = __density['helium']    
__mat['gap']['card'] = __card['helium']    
__mat['clad'] = {}
__mat['clad']['ID'] = ['0012']
__mat['clad']['density'] = __density['SiC-SiC']
__mat['clad']['card'] = __card['SiC-SiC']        

def __rot(angle, magnitude):
    o = magnitude * np.array([1.0, 0.0, 0.0])
    rad = angle / 180.0 * np.pi
    Rot = np.array([[np.cos(rad), -np.sin(rad), 0.0],
                       [np.sin(rad),  np.cos(rad), 0.0],
                       [0.0, 0.0, 0.0]])
    rot = np.dot(Rot,o)
    out = ''
    for i in rot:
        out += str(i) + '  '
    return out

def build_dictionary(fuel, radius, margin,
           poison = None,
           poison_thickness = 0.00, 
           gap_width = 0.04, 
           clad_thickness = 0.1, 
           coolant = True):

    global __fuel
    global __abrev
    global __poison
    global __density
    global __card
    global __mat
    global __test_height

    assert fuel in __fuel
    assert poison in __poison
    if poison == None: 
        assert poison_thickness == 0.00
    assert radius > 0
    assert margin > 0
    assert type(coolant) == bool

    inp_dict = {}

    description = __abrev[fuel] 
    description += ' - ' + str(poison) 
    description += ' - ' + format(radius, '.3f') + ' cm radius'
    description += ' - ' + format(margin, '.3f') + ' cm margin'
    if (not coolant):
        description += ' - ' + 'void'

    mat = __mat.copy()
    mat['fuel']['density'] = __density[fuel]
    mat['fuel']['card'] = __card[fuel]
    if not(poison == None):
        mat['poison']['ID'] = ['0010']
        mat['poison']['density'] = __density[fuel]
        mat['poison']['card'] = __card[fuel]
    if (coolant):
        mat['coolant'] = {}
        mat['coolant']['ID'] = ['0013']
        mat['coolant']['density'] = __density['flibe']    
        mat['coolant']['card'] = __card['flibe']    

    base = '0.0  0.0  ' + str(-__test_height/2.0)
    height = '0.0  0.0  ' + str(__test_height)
    apothem = radius + poison_thickness + gap_width + clad_thickness + margin
    facet1 = __rot(0.0, apothem)
    facet2 = __rot(-60.0, apothem)
    facet3 = __rot(-120.0, apothem)

    geom = {'fuel-radius' : radius,
            'poison-radius' : radius + poison_thickness,
            'gap-radius' : radius + poison_thickness + gap_width,
            'clad-radius' : radius + poison_thickness + gap_width + clad_thickness,
            'hex':{'base': base,
                   'height' : height,
                   'facet':[facet1, facet2, facet3]}
            }

    
    crit = {'ksrc' : '0.0  0.0  0.0',
            'particles-per-cycle' : 80000,
            'criticality-guess' : 1.0,
            'skipped-cycles' : 10,
            'total-cycles' : 60
            }
    
    has = {'poison' : not (poison == None),
           'coolant' : coolant
           }

    inp_dict['description'] = description
    inp_dict['material-dict'] = mat
    inp_dict['geometry-dict'] = geom
    inp_dict['criticality-dict'] = crit
    inp_dict['condition-dict'] = has
    
    return inp_dict

def build_input(fuel, radius, margin):
    assert np.all(radius > 0)
    assert np.all(margin > 0)
    
    input_dict = build_dictionary(fuel, radius, margin)
    handle = __abrev[fuel] 
    handle += '-' + str(radius) 
    handle += '-' + str(margin) 
    
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

    input_dict = build_dictionary(fuel, radius, margin, coolant = False)
    handle = __abrev[fuel] 
    handle += '-' + str(radius) 
    handle += '-' + str(margin)
    handle += '-void'
    
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


def build_inputs(fuel, radius_range, mrr_range, step, max_step):
    global __abrev
    global __fuel

    assert fuel in __fuel
    assert step >= 0
    assert max_step >= step
 
    radius = np.mean(radius_range)
    margin = radius * np.mean(mrr_range)
    build_input(fuel, radius, margin)

    if step == 0:
        build_input(fuel, radius_range[0], radius_range[0] * mrr_range[0])
        build_input(fuel, radius_range[0], radius_range[0] * mrr_range[1])
        build_input(fuel, radius_range[1], radius_range[1] * mrr_range[0])
        build_input(fuel, radius_range[1], radius_range[1] * mrr_range[1])
    
    new_step = step + 1
    if new_step <= max_step:
        build_inputs(fuel,
                     np.array([radius_range[0], radius]),
                     np.array([mrr_range[0], np.mean(mrr_range)]),
                     new_step,
                     max_step)
        build_inputs(fuel,
                     np.array([radius, radius_range[1]]),
                     np.array([mrr_range[0], np.mean(mrr_range)]),
                     new_step,
                     max_step)
        build_inputs(fuel,
                     np.array([radius_range[0], radius]),
                     np.array([np.mean(mrr_range), mrr_range[1]]),
                     new_step,
                     max_step)
        build_inputs(fuel,
                     np.array([radius, radius_range[1]]),
                     np.array([np.mean(mrr_range), mrr_range[1]]),
                     new_step,
                     max_step)

build_inputs('uranium-carbide', np.array([0.1, 0.6]), np.array([0.5, 3.0]), 0, 1)
