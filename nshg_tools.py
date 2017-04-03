#!/usr/bin/env python3

import argparse, os
import logging as log
from nshg import *

log.basicConfig(level=log.WARNING) # change to warning when finished

# Config

# Commented out for testing
'''
argparser = argparse.ArgumentParser(description='transform Unity assets')
argparser.add_argument('command', help='action to perform on the files',
                       choices=['header', 'metadata', 'types', 'objectinfo', 'objectids', 'fileids', 'entries', 
                       'unpack', 'unpack-raw', 'unpack-decode', 'repack', 'repack-raw'])
argparser.add_argument('files', metavar='FILE', nargs='+', help='list of source files and/or directories to act upon')
argparser.add_argument(['-d', '--dest-dir'], dest='dest_dir', default='./asset_dump', help='directory containing extracted files')

args = argparser.parse_args()
'''
# For testing purposes

args = {}

args['command'] = 'unpack-decode'

#args['files'] = [r'Q:\Ryan\Documents\Unity\TestProject\testproject_Data\sharedassets0.assets']
#args['files'] = [r'Q:\Ryan\Documents\Unity\TestProject\testproject_Data\level0', r'Q:\Ryan\Documents\Unity\TestProject\testproject_Data\sharedassets0.assets']
#args['files'] = [r'Q:\Games\NSHG_v111\NewSuperHookGirl_Data\sharedassets2.assets']
args['files'] = [r'Q:\Games\NSHG_v111\NewSuperHookGirl_Data']
#args['files'] = [r'Q:\Games\NSHG_v111\NewSuperHookGirl_Data\level0', r'Q:\Games\NSHG_v111\NewSuperHookGirl_Data\level1']

args['dest_dir'] = './asset_dump'

# Body

def process_file(file_path):
    basename = os.path.basename(file_path)
    name, extension = os.path.splitext(basename)

    if extension == '.assets' or (extension == '' and name[:5] == 'level'):
        print('Processing: ' + basename)

        with open(file_path, 'rb') as main_file:
            header, metadata, entries = parser.file_info(main_file)
            command = args['command']

            if command == 'header':
                print('Metadata Size:', header['metadata_size'])
                print('File Size:', header['file_size'])
                print('Version:', header['version'])
                print('Data Section Offset:', header['data_offset'])
                print('Endianness:', 'Big-Endian' if header['endianness'] == True else 'Little-Endian')
            elif command == 'metadata':
                print('Version:', metadata['version'])
                print('Attributes:', metadata['attributes'])
                print('Embedded:', metadata['embedded'])
                print('Base Class Count:', metadata['base_class_count'])
            elif command == 'types':
                util.print_dict(metadata['typetree'])
            elif command == 'objectinfo':
                util.print_dict(metadata['obj_info'])
            elif command == 'objectids':
                util.print_list(metadata['obj_ids'])
            elif command == 'fileids':
                util.print_list(metadata['file_ids'])
            elif command == 'entries':
                util.print_list(entries)
            elif command in ('unpack', 'unpack-raw', 'unpack-decode', 'repack', 'repack-raw'):
                asset_dir = os.path.join(args['dest_dir'], '_' + basename)
                util.ensure_dir_exists(asset_dir)

                if command[-4:] == '-raw':
                    asset_dir = asset_dir + '/_raw'
                    util.ensure_dir_exists(asset_dir)

                if command[:6] == 'unpack':
                    if os.path.isfile(os.path.join(asset_dir, '_index.json')):
                        response = input('Directory %s already exists. Empty and re-unpack? (Y/n)'.format(asset_dir))
                        if response.lower() in ('n', 'no'):
                            return
                    util.clear_dir_contents(asset_dir) # should request confirmation on this

                    nodes = []
                    for entry in entries:
                        nodes.append(parser.assets_entry(main_file, entry))

                    index = unpacker.unpack(nodes, file_path, asset_dir, command)

                    index_handler.save_index(index, asset_dir)

                else: # command[:6] == 'repack'
                    print('repack')

for path in args['files']:
    is_file = os.path.isfile(path)
    is_dir = os.path.isdir(path)
    if not (is_file or is_dir):
        log.warn('%s does not exist; skipping', path)
    elif is_file:
        process_file(path)
    else: # is_dir
        files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        print(len(files))
        for filename in files:
            process_file(filename)
