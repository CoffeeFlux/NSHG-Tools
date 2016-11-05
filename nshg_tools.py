#!/usr/bin/env python3

import argparse
from nshg import *

# Initialization

# Commented out for testing
'''
praser = argparse.ArgumentParser(description='transform Unity assets')
parser.add_argument('file_type', help='type of file to act upon', 
	                choices=['assets','level'])
parser.add_argument('command', help='action to perform on the files', 
	                choices=['blocks', 'header', 'objectids', 'types', 'unpack', 'pack'])
parser.add_argument('files', metavar='FILE', nargs='+', help='list of files and/or directories to act upon')
parser.add_argument(['-d', '--dest-dir'], dest='dest_dir', help='directory to unpack/pack to')

args = parser.parse_args()
'''
# For testing purposes

args = []

args.file_type = 'assets'
#args.file_type = 'level'

args.command = 'header'

args.files = r'Q:\Ryan\Documents\Unity\TestProject\testproject_Data'
#args.files = r'Q:\Games\NSHG_v111\NewSuperHookGirl_Data'

# Body

