#!/usr/bin/env python

import re
import collections

__line_pattern = collections.OrderedDict()
__line_pattern['entropy'] = r"[ ]*comment.[ ]+H=[ ]+[0-9]+.[0-9]+(E[\+\-]?[0-9]+)[ ]+with[ ]+population[ ]+std.dev.=[ ]+[0-9]+.[0-9]+(E[\+\-]?[0-9]+)[ ]*"
__line_pattern['stable-fission-dist-cycle'] = r"[ ]*comment.[ ]+Cycle[ ]+[0-9]+ is the first cycle having fission-source[ ]*"
__line_pattern['criticality'] = r"[ ]*\|[ ]+the final estimated combined collision/absorption/track-length keff = [0-9]+.[0-9]+(E[\-\+]?[0-9]+)? with an estimated standard deviation of [0-9]+.[0-9]+(E[\-\+]?[0-9]+)?[ ]*[\|][ ]*"
__line_pattern['prompt-removal-lifetime'] = r"[ ]*\|[ ]+the final combined \(col/abs/tl\) prompt removal lifetime = [0-9]+.[0-9]+(E[\-\+]?[0-9]+)? seconds with an estimated standard deviation of [0-9]+.[0-9]+(E[\-\+]?[0-9]+)?[ ]*[\|][ ]*"
__line_pattern['avg-energy-of-neutrons-causing-fission'] = r"[ ]*\|[ ]+the average neutron energy causing fission = [0-9]+.[0-9]+(E[\-\+]?[0-9]+)?[ ]*mev[ ]*[\|][ ]*"
__line_pattern['avg-lethargy-of-neutrons-causing-fission'] = r"[ ]*\|[ ]*the energy corresponding to the average neutron lethargy causing fission = [0-9]+.[0-9]+(E[\-\+]?[0-9]+)?[ ]*mev[ ]*[\|][ ]*"
__line_pattern['energy-bins'] = r"[ ]*\|[ ]*\(<0.625 ev\):[ ]*[0-9]+.[0-9]+%[ ]+\(0.625 ev - 100 kev\):[ ]*[0-9]+.[0-9]+%[ ]+\(>100 kev\):[ ]*[0-9]+.[0-9]+%[ ]+[\|][ ]*"
__line_pattern['neutrons-per-fission'] = r"[ ]*\|[ ]*the average number of neutrons produced per fission = [0-9]+.[0-9]+[ ]*[\|][ ]*"

__line_info = {}
__line_info['entropy'] = ['source-entropy', 'source-entropy-std']
__line_info['stable-fission-dist-cycle'] = ['source-entropy-stable-cycle']
__line_info['criticality'] = ['criticality', 'criticality-std']
__line_info['prompt-removal-lifetime'] = ['prompt-removal-lifetime', 'prompt-removal-lifetime-std']
__line_info['avg-energy-of-neutrons-causing-fission'] = ['energy-fission-causing-neutrons']
__line_info['avg-lethargy-of-neutrons-causing-fission'] = ['lethargy-fission-causing-neutrons']
__line_info['energy-bins'] = ['thermal-fission', 'epithermal-fission', 'fast-fission']
__line_info['neutrons-per-fission'] = ['neutrons-per-fission']

__regex_chain = {}
__regex_chain['source-entropy'] = [r"H=[ ]+[0-9]+.[0-9]+(E[\+\-]?[0-9]+)", 
                                   r"[0-9]+.[0-9]+(E[\+\-]?[0-9]+)"]
__regex_chain['source-entropy-std'] = [r"std.dev.=[ ]+[0-9]+.[0-9]+(E[\+\-]?[0-9]+)[ ]*", 
                                       r"[0-9]+.[0-9]+(E[\+\-]?[0-9]+)"]
__regex_chain['source-entropy-stable-cycle'] = [r"[0-9]+"]
__regex_chain['criticality'] = [r"keff = [0-9]+.[0-9]+(E[\-\+]?[0-9]+)?",
                                r"[0-9]+.[0-9]+(E[\-\+]?[0-9]+)?"]
__regex_chain['criticality-std'] = [r"estimated standard deviation of [0-9]+.[0-9]+(E[\-\+]?[0-9]+)?",
                                    r"[0-9]+.[0-9]+(E[\-\+]?[0-9]+)?"]
__regex_chain['prompt-removal-lifetime'] = [r"prompt removal lifetime = [0-9]+.[0-9]+(E[\-\+]?[0-9]+)? seconds",
                                            r"[0-9]+.[0-9]+(E[\-\+]?[0-9]+)?"]
__regex_chain['prompt-removal-lifetime-std'] = [r"estimated standard deviation of [0-9]+.[0-9]+(E[\-\+]?[0-9]+)?", 
                                                r"[0-9]+.[0-9]+(E[\-\+]?[0-9]+)?"]
__regex_chain['energy-fission-causing-neutrons'] = [r"[0-9]+.[0-9]+(E[\-\+]?[0-9]+)?"]
__regex_chain['lethargy-fission-causing-neutrons'] = [r"[0-9]+.[0-9]+(E[\-\+]?[0-9]+)?"]
__regex_chain['thermal-fission'] = [r"\(<0.625 ev\):[ ]*[0-9]+.[0-9]+%", 
                                    r"[0-9]+.[0-9]+%",
                                    r"[0-9]+.[0-9]+"]
__regex_chain['epithermal-fission'] = [r"\(0.625 ev - 100 kev\):[ ]*[0-9]+.[0-9]+%",
                                       r"[0-9]+.[0-9]+(E[\-\+]?[0-9]+)?%",
                                       r"[0-9]+.[0-9]+(E[\-\+]?[0-9]+)?"]
__regex_chain['fast-fission'] = [r"\(>100 kev\):[ ]*[0-9]+.[0-9]+%", 
                                 r"[0-9]+.[0-9]+(E[\-\+]?[0-9]+)?%",
                                 r"[0-9]+.[0-9]+(E[\-\+]?[0-9]+)?"]
__regex_chain['neutrons-per-fission'] = [r"[0-9]+.[0-9]"]

def __get_value(string, regex_chain):
    val = string
    for pattern in regex_chain:
        val = re.search(pattern, val).group()
    return float(val)

def __parse_line(value, line, line_type):
    global __line_info
    global __regex_chain
    for info in __line_info[line_type]:
        value[info] = __get_value(line, __regex_chain[info])

def output(filename):
    global __line_pattern
    value = {}
    output_file = open(filename, 'r')
    for line_type in __line_pattern.keys():
        while True:
            line = output_file.readline()
            #assert not line
            found = re.match(__line_pattern[line_type], line) != None
            if found:
                break
        __parse_line(value, line, line_type)
    output_file.close()
    return value
                

    
