#!/usr/bin/env python3

import argparse
import * from nshg

# Initialization

# Commented out for testing
'''
argparser = argparse.ArgumentParser(description='transform Unity assets')
argparser.add_argument('file_type', help='type of file to act upon', 
	                choices=['assets','level'])
argparser.add_argument('command', help='action to perform on the files', 
	                choices=['blocks', 'header', 'objectids', 'types', 'unpack', 'pack'])
argparser.add_argument('files', metavar='FILE', nargs='+', help='list of files and/or directories to act upon')
argparser.add_argument(['-d', '--dest-dir'], dest='dest_dir', help='directory to unpack/pack to')

args = argparser.parse_args()
'''
# For testing purposes

args = []

args.file_type = 'assets'
#args.file_type = 'level'

args.command = 'header'

args.files = r'Q:\Ryan\Documents\Unity\TestProject\testproject_Data'
#args.files = r'Q:\Games\NSHG_v111\NewSuperHookGirl_Data'

# Body

