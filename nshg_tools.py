#!/usr/bin/env python3

import argparse, os
import logging as log
import * from nshg

logging.basicConfig(level=logging.INFO) # change to warning when finished

# Config

# Commented out for testing
'''
argparser = argparse.ArgumentParser(description='transform Unity assets')
argparser.add_argument('file_type', help='type of file to act upon',
                       choices=['assets','level'])
argparser.add_argument('command', help='action to perform on the files',
                       choices=['header', 'metadata', 'types', 'objectinfo', 'objectids', 'fileids',
                       'entries', 'unpack', 'unpack-raw', 'repack', 'repack-raw'])
argparser.add_argument('files', metavar='FILE', nargs='+', help='list of source files and/or directories to act upon')
argparser.add_argument(['-d', '--dest-dir'], dest='dest_dir', default='./', help='directory containing extracted files')

args = argparser.parse_args()
'''
# For testing purposes

args = []

args.file_type = 'assets'
#args.file_type = 'level'

args.command = 'header'

args.files = [r'Q:\Ryan\Documents\Unity\TestProject\testproject_Data\sharedassets0.assets']
#args.files = [r'Q:\Games\NSHG_v111\NewSuperHookGirl_Data\sharedassets0.assets']

dest_dir = './'

# Body

def process_assets_file(file_path):
	main_file = open(file_path)
	header, metadata, entries = parser.assets_file_info(main_file)
	command = args.command
	if command == 'header':
		print('Metadata Size:', header['metadata_size'])
		print('File Size:', header['file_size'])
		print('Version:', header['version'])
		print('Data Section Offset:', header['data_offset'])
		print('Endianness:', if header['endianness'] == True then 'Big-Endian' else 'Little-Endian')
	elif command == 'metadata':
		print('Version:', metadata['version'])
		print('Attributes:', metadata['attributes'])
		print('Embedded:', metadata['embedded'])
		print('Base Class Count:', metadata['base_class_count'])
	elif command == 'types':
		print(*metadata['typetree'], sep='\n')
	elif command == 'objectinfo':
		print(*metadata['obj_info'], sep='\n')
	elif command == 'objectids':
		print(*metadata['obj_ids'], sep='\n')
	elif command == 'fileids':
		print(*metadata['file_ids'], sep='\n')
	elif command == 'entries':
		print(*entries, sep='\n')
	elif command in ('unpack', 'unpack-raw', 'repack', 'repack-raw'):
		for entry in entries:
			node = parser.assets_entry(main_file, entry)
			#if command == 


def process_level_file(file_path):
	print('a')

def process_file(file_path):
	basename = os.path.basename(file_path)
	name, extension = os.path.splitext(basename)
	if extension == '.assets':
		process_assets_file(file_path)
	elif extension == '' and name[:5] == 'level':
		process_level_file(file_path)

for path in args.files:
	is_file = os.path.isfile(path)
	is_dir = os.path.isdir(path)
	if not (is_file or is_dir):
		log.warn('%s does not exist; skipping', path)
	elif is_file:
		process_file(path)
	else: # is_dir
		files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(f)]
		for filename in files:
			process_file(filename)
