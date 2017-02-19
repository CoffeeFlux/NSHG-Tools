#!/usr/bin/env python3

import argparse, os, hashlib, png
import logging as log
from nshg import *

log.basicConfig(level=log.WARNING) # change to warning when finished

# Config

# Commented out for testing
'''
argparser = argparse.ArgumentParser(description='transform Unity assets')
argparser.add_argument('command', help='action to perform on the files',
                       choices=['header', 'metadata', 'types', 'objectinfo', 'objectids', 'fileids',
                       'entries', 'unpack', 'unpack-raw', 'repack', 'repack-raw'])
argparser.add_argument('files', metavar='FILE', nargs='+', help='list of source files and/or directories to act upon')
argparser.add_argument(['-d', '--dest-dir'], dest='dest_dir', default='./asset_dump', help='directory containing extracted files')

args = argparser.parse_args()
'''
# For testing purposes

args = {}

args['command'] = 'unpack'

args['files'] = [r'Q:\Ryan\Documents\Unity\TestProject\testproject_Data\sharedassets0.assets']
#args.files = [r'Q:\Games\NSHG_v111\NewSuperHookGirl_Data\sharedassets0.assets']

args['dest_dir'] = './asset_dump'

# Body

def process_assets_file(file_path):
    basename = os.path.basename(file_path)

    with open(file_path, 'rb') as main_file:
        header, metadata, entries = parser.assets_file_info(main_file)
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
        elif command in ('unpack', 'unpack-raw', 'repack', 'repack-raw'):
            asset_dir = os.path.join(args['dest_dir'], '_' + basename)
            util.ensure_dir_exists(asset_dir)

            with open(file_path + '.resS', 'rb') as ress_file:
                if command[-4:] == '-raw':
                    asset_dir = asset_dir + '/_raw'
                    util.ensure_dir_exists(asset_dir)

                if command[:6] == 'unpack': # should be broken up into smaller functions
                    util.clear_dir_contents(asset_dir) # should request confirmation on this
                
                    nodes = []
                    for entry in entries:
                        nodes.append(parser.assets_entry(main_file, entry))
                    image_nodes = [node for node in nodes if node['type_id'] == 28]

                    index = []

                    for node in image_nodes:
                        ress_file.seek(node['offset'])
                        image_data_raw = ress_file.read(node['size'])
                        image_name = node['image_name']

                        if command == 'unpack-raw':
                            image_data = image_data_raw
                            with open(os.path.join(asset_dir, image_name), 'wb') as image_file:
                                image_file.write(image_data)

                        else: # command == 'unpack'
                            image_format = node['img_format']

                            if image_format in (3, 5): # RGB24, ARGB32
                                image_path = os.path.join(asset_dir, image_name + '.png')
                                x_res = node['x_res']
                                y_res = node['y_res']
                                alpha = True if image_format == 5 else False
                                image_data_list = convert.raw_image_to_list(image_data_raw, x_res, y_res, alpha, True)
                                with open(image_path, 'wb') as image_file:
                                    writer = png.Writer(x_res, y_res, alpha=alpha)
                                    writer.write(image_file, image_data_list)

                            elif image_format in (10, 12): # RGB24 DXT1, ARGB32 DXT5
                                print('dxt')

                            # This is sloppy and lazy, but it works
                            with open(image_path, 'rb') as image_file:
                                image_data = image_file.read()

                        data_hash = hashlib.sha256(image_data).hexdigest()
                        index.append({
                            'node': node,
                            'hash': data_hash
                        })

                    index_handler.save_index(index, asset_dir)

                else: # command[:6] == 'repack'
                    print('repack')


def process_level_file(file_path):
    print('a')

def process_file(file_path):
    basename = os.path.basename(file_path)
    name, extension = os.path.splitext(basename)

    if extension == '.assets':
        process_assets_file(file_path)
    elif extension == '' and name[:5] == 'level':
        process_level_file(file_path)

for path in args['files']:
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
