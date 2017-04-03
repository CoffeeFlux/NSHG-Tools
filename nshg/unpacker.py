import os, png, io
from nshg import index_handler, dxt, convert
from .util import * # in package
import logging as log

def unpack(nodes, file_path, asset_dir, command):
    index = []

    # Can't find a proper flag for whether or not an external file is used...
    if os.path.isfile(file_path + '.resS'):
        file_path += '.resS'

    with open(file_path, 'rb') as source_file:
        for node in nodes:
            # Unsure how much of this is shared, so for the moment hard-code for images
            if node['type_id'] == 28: # image
                source_file.seek(node['offset'])
                data_raw = source_file.read(node['size'])
                name = node['image_name']

                if command == 'unpack_raw':
                    with open(os.path.join(asset_dir, name), 'wb') as image_file:
                        image_file.write(data_raw)
                    entry = index_handler.format_entry(node, data_raw)
                    index.append(entry)

                else: # command in ('unpack' or 'unpack-decode')
                    image_format = node['img_format']
                    image_path = ''
                    x_res = node['x_res']
                    y_res = node['y_res']

                    if image_format in (3, 5): # RGB24, ARGB32
                        image_path = os.path.join(asset_dir, name + '.png')
                        alpha = True if image_format == 5 else False
                        image_data_list = convert.raw_image_to_list(data_raw, x_res, y_res, alpha, True)

                        with open(image_path, 'wb') as image_file:
                            writer = png.Writer(x_res, y_res, alpha=alpha)
                            writer.write(image_file, image_data_list)

                    elif image_format in (10, 12): # RGB24 DXT1, ARGB32 DXT5
                        if command == 'unpack':
                            print('dxt unpack')

                        else: # command == 'unpack-decode'
                            image_path = os.path.join(asset_dir, name + '.png')

                            if image_format == 10:
                                image_data_list = dxt.decode_bc1(data_raw, x_res, y_res)
                            else: # 12
                                image_data_list = dxt.decode_bc3(data_raw, x_res, y_res, False)

                            with open(image_path, 'wb') as image_file:
                                writer = png.Writer(x_res, y_res, alpha=True)
                                writer.write(image_file, image_data_list)

                    # This is sloppy and lazy, but hey it works
                    if image_path:
                        with open(image_path, 'rb') as image_file:
                            data = image_file.read()
                            entry = index_handler.format_entry(node, data)
                            index.append(entry)

    return index
