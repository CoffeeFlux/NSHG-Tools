import struct

def format_hex(s):
	return '0x' + format(s, '02x').upper().zfill(8)

def read(format, length, file_handler):
	return struct.unpack(format, file_handler.read(length))[0]

def read_int(file_handler):
	return read('<I', 4, file_handler)

def read_byte(file_handler)

def read_until_null(file_handler):
	raw = bytearray()
	byte = file_handler.read(1)
	while byte != b'\0':
		raw.extend(byte)
		byte = file_handler.read(1)
	return raw

def read_null_term_string(file_handler):
	return read_until_null(file_handler).decode('utf-8')

def read_string(file_handler):
	length = read_int(file_handler)
	return data.read(length).decode('utf-8')

def read_chunk(offset, size, file_handler, reset_pos=True):
	initial_pos = file_handler.tell()
	file_handler.seek(offset)
	raw = file_handler.read(size)
	if reset_pos:
		file_handler.seek(initial_pos)
	return io.BytesIO(raw)

def align(n, file_handler):
	while file_handler.tell() % ne:
		file_handler.read(1)

def pad(n, file_handler):
	file_handler.read(n)

def get_pos(file_handler):
	return format_hex(file_handler.tell())

def img_data_to_list(data, x_res, y_res, alpha=False, reverse=False):
	data = io.BytesIO(data)
	output = collections.deque()
	for y in range(0, y_res):
		row = []
		for x in range(0, x_res):
			if alpha:
				a = read_byte(data)     # A
			row.append(read_byte(data)) # R
			row.append(read_byte(data)) # G
			row.append(read_byte(data)) # B
			if alpha:
				row.append(a)
		if reverse:
			output.appendleft(row)
		else:
			output.append(row)
	return list(output)

def ensure_path_exists(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
