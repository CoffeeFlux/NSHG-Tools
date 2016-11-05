import * from util # in package
import io, collections

def raw_image_to_list(data, x_res, y_res, alpha=False, reverse=False):
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