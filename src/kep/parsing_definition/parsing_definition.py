# TODO: check schema twice
# TODO: see printout
# TODO: edit comments
# TODO: tests    

"""Parsing definition to identify tables in the data source file.
    
   A defnition contains a list of nested dicts. 

   Each dict has following keys: 
   - commands, a list of dicts each with following keys:     
       - variable name ('GDP')
       - corresponding headers ('Oбъем ВВП')
       - units of measurement ('bln_rub')
   - boundaries (start and end lines of text)   
   - reader function name(string)

Create parsing instructions for an individual variable.

    Keys:
        varname (str):
            varaible name, ex: 'GDP'
        table_headers-strings (list of strings):
            header string(s) associated with variable names
            ex: ['Oбъем ВВП'] or ['Oбъем ВВП', 'Индекс физического объема произведенного ВВП']
        units (list of strings):
            required_labels unit(s) of measurement
            ex: ['bln_usd]' or ['rog', 'rub']
"""

from collections import namedtuple

import yaml
from typing import List

from kep.helper.label import make_label
from .parameters import YAML_DEFAULT, YAML_BY_SEGMENT
from .units import UNITS


def iterate(x):
    if isinstance(x, list):
        return x
    elif isinstance(x, str) or isinstance(x, dict):
        return [x]
    else:
        raise TypeError(x)
    

def make_table_header_mapper(commands):
    result = {}
    for c in iterate(commands):
        for header in iterate(c['header']):
            result[header] = c['var'] 
    return result

    
def make_required_labels(commands):
    result = []
    for c in iterate(commands):
        for unit in iterate(c['unit']):
            result.append(make_label(c['var'], unit))
    return result


DefinitionFactory = namedtuple('ParsingDefinition', 
                              ['mapper', 'required_labels', 'boundaries',
                               'units', 'reader']) 

def make_parsing_definition(commands: List[dict],
                            boundaries: List[dict] = [],
                            reader: str = '',
                            units = UNITS):
    return DefinitionFactory(mapper = make_table_header_mapper(commands),
                required_labels = make_required_labels(commands),
                boundaries = boundaries,
                reader = reader,
                units = UNITS)  

commands_default = list(yaml.load_all(YAML_DEFAULT))
instructions_by_segment = list(yaml.load_all(YAML_BY_SEGMENT))    
DEFINITION_DEFAULT = make_parsing_definition(commands_default, boundaries=[], reader='')
DEFINITIONS_BY_SEGMENT = [make_parsing_definition(**instruction) for instruction in instructions_by_segment]
