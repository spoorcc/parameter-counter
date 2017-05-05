#!/usr/bin/env python


'''
Holtenizer

Script for creating digams as described by Danny Holten
'''


import argparse
import sys
from pycparser import c_parser, c_ast, parse_file
import json
import os.path
from os import sep as os_sep
import pprint

class FuncCallVisitor(c_ast.NodeVisitor):

    def __init__(self):
        self.func_defs = {}

    def visit_FuncDef(self, node):
        self.func_defs[node.decl.name] = {'location': '{loc.file}:{loc.line}'.format(loc=node.decl.coord),
                                          'number_of_parameters': len(node.decl.type.args.params) if node.decl.type.args else 0}

def show_func_calls(files, output_path):

    v = FuncCallVisitor()
    for filename in files:
        ast = parse_file(filename, use_cpp=True,
                         cpp_path='gcc',
                         cpp_args=['-E', r'-Ipycparser/utils/fake_libc_include'])
        v.visit(ast)

    output_dict(v.func_defs, output_path)

def output_dict(dictionary, output_path):
    json_output = json.dumps(dictionary, sort_keys=True, indent=4)

    if output_path:
        with open(output_path, 'w') as output_file:
            print(json_output, file=output_file)
    else:
        print(json_output)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('files', metavar='<file>', type=str, nargs='+',
                         help='c-files to parse')
    parser.add_argument('-o','--output', metavar='<path>', type=str, default=None,
                         help='Path of output file')

    args = parser.parse_args()
    show_func_calls(args.files, args.output)
