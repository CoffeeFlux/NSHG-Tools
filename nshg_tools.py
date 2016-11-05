#!/usr/bin/env python3

import argparse, os
import logging as log
import * from nshg

# Config

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

args.files = [r'Q:\Ryan\Documents\Unity\TestProject\testproject_Data\sharedassets0.assets']
#args.files = [r'Q:\Games\NSHG_v111\NewSuperHookGirl_Data\sharedassets0.assets']

# Body

def process_file(filename):
	# shit

for name in args.files:
	is_file = os.path.isfile(name)
	is_dir = os.path.isdir(name)
	if not (is_file or is_dir):
		log.warn('%s does not exist; skipping', name)
	elif is_file
