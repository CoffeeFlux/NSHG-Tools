import * from util # in package
import logging as log

def assets_file_info(file_handler):
	f = file_handler

	# Header - Dict
	header = {}
	header['metadata_size'] = read('>I', 4, f)
	header['file_size']     = read('>I', 4, f)
	header['version']       = read('>I', 4, f)
	header['data_offset']   = read('>I', 4, f)
	header['endianness']    = read('>?', 1, f)
	log.debug('header: %s', header)
	pad(3, f)

	# Metadata - Dict
	metadata = {}
	log.info('metadata start: %8x', f.tell())
	metadata['version']          = read_null_term_string()
	metadata['attributes']       = read_int(f)
	metadata['embedded']         = read_bool(f)
	metadata['base_class_count'] = read_int(f)
	log.debug('metadata: %s', metadata)

	# Type Tree - Dict by Class Id
	typetree = {}
	log.info('type tree start: %8x', f.tell())
	for x in range(0, metadata['base_class_count']):
	    typeroot = {}
	    typeroot['class_id']      = read_int(f)
	    if typeroot['class_id'] < 0:
	        typeroot['script_id'] = read('>16B', 16, f)
	    typeroot['old_type_hash'] = read('>16B', 16, f)
	    if False: # might have new condition attached
	        typenode = {}
	        typenode['version']     = read('<H', 2, f)
	        typenode['tree_level']  = read_byte(f)
	        typenode['is_array']    = read_bool(f)
	        typenode['type_offset'] = read_int(f)
	        typenode['name_offset'] = read_int(f)
	        typenode['size']        = read_int(f)
	        typenode['index']       = read_int(f)
	        typenode['meta_flag']   = read_int(f)
	    typetree[typeroot['class_id']] = typeroot
	log.debug('type tree: %s', typetree)
	metadata['typetree'] = typetree

	# Object Info Table - Dict by Path Id
	log.info('object info table start: %8x', f.tell())
	metadata['object_info_count'] = read_int(f)
	log.info('object info table entries: %i', metadata['object_info_count'])
	obj_info = {}
	for x in range(0, metadata['object_info_count']):
	    obj = {}
	    align(4, f)
	    path_id                  = read('<Q', 8, f)
	    obj['offset']            = read_int(f)
	    obj['size']              = read_int(f)
	    obj['type_id']           = read_int(f)
	    obj['class_id']          = read('<h', 2, f)
	    obj['script_type_index'] = read('<h', 2, f)
	    obj['is_stripped']       = read_bool(f)
	    obj_info[path_id] = obj
	log.debug('object info table: %s', obj_info)
	metadata['obj_info'] = obj_info

	# Object Id Table - List
	log.info('object id table start: %8x', f.tell())
	metadata['object_id_count'] = read_int(f)
	log.info('object id table entries: %i', metadata['object_id_count'])
	obj_ids = []
	for x in range(0, metadata['object_id_count']):
	    obj = {}
	    obj['serialized_file_index'] = read_int(f)
	    obj['identifier_in_file']    = read('<Q', 8, f)
	    obj_ids.append(obj)
	align(4, f)
	log.debug('object id table: %s', obj_ids)
	metadata['obj_ids'] = obj_ids

	# File Id Table - List
	log.info('file id table start: %8x', f.tell())
	metadata['file_id_count'] = read_int(f)
	log.info('file id table entries: %i', metadata['file_id_count'])
	file_ids = []
	for x in range(0, metadata['file_id_count']):
	    file = {}
	    file['asset_path'] = read_until_null()
	    file['guid']       = read('>16B', 16, f)
	    file['type']       = read_int(f)
	    file['path']       = read_until_null()
	    file_ids.append(file)
	log.debug('file id table: %s', file_ids)
	metadata['file_ids'] = file_ids

	# Entry Table - List
	log.info('entry table start: %8x', f.tell())
	entries = []
	for path_id, info in obj_info.items():
	    entry = {}
	    entry['offset'] = header['data_offset'] + metadata['obj_info']['offset']
	    entry['size'] = metadata['obj_info']['size']
	    entry['type_id'] = metadata['obj_info']['type_id'] # make sure this is possible/useful, consider actual type root
	    entries.append(entry)
	log.debug('entries: %s', entries)

	return header, metadata, entries

def assets_entry(file_handler, entry, duplicate=False): # duplicate option added for error recovery - what did i mean by this???
	type_id = entry['type_id']
	if duplicate:
		data = read_chunk(entry['offset'], entry['size'], file_handler)
	else:
		file_handler.seek(entry['offset'])
		data = file_handler
	node = {}

	# In lieu of a switch statement
	if type_id in (28, 213):
		node['image_name'] = read_string(data)
		align(4, data)
		log.info('%s, id %i', node['image_name'], type_id)

		if type_id == 28:
            node['x_res']      = read_int(data)
            node['y_res']      = read_int(data)
            node['size']       = read_int(data)
            node['img_format'] = read_int(data) # 3 == RGB24, 5 == ARGB32, 10 == RGB24 DXT1, 12 == ARGB32 DXT5
            node['mipmap']     = read_int(data) # mipmap data? 8 is enabled but none, 7 is enabled and generated, 1 is disabled?
            data.read(40) # unknown purpose, perhaps format-dependent image header info; largely similar
            node['offset']     = read_int(data)
            node['size2']      = read_int(data)
            node['ress_name']  = read_str(data)
            align(4, data)
            log.info('image format: %i', img_format)
    
    log.debug('entry data node: %s', node)

    return node
