from .util import * # in package
import io, collections, math, copy
import logging as log

# DXT-specific util functions:

def lerp(point1, point2, distance):
    return point1 * (1 - distance) + point2 * distance

def rgb565_to_rgb888(rgb565):
    return [round(((rgb565 >> 11) & 31) * (255 / 31)),
            round(((rgb565 >> 5) & 63) * (255 / 63)),
            round((rgb565 & 31) * (255 / 31))]

def interpolate_color(val1, val2, is_dxt1):
    color1 = rgb565_to_rgb888(val1)
    color1.append(255) # add alpha value
    color2 = rgb565_to_rgb888(val2)
    color2.append(255)
    if is_dxt1 and val1 <= val2:
        color3 = [round((color1[0] + color2[0]) / 2),
                  round((color1[1] + color2[1]) / 2),
                  round((color1[2] + color2[2]) / 2),
                  255]
        color4 = [0, 0, 0, 0]
    else:
        color3 = [round(lerp(color1[0], color2[0], 1 / 3)),
                  round(lerp(color1[1], color2[1], 1 / 3)),
                  round(lerp(color1[2], color2[2], 1 / 3)),
                  255]
        color4 = [round(lerp(color1[0], color2[0], 2 / 3)),
                  round(lerp(color1[1], color2[1], 2 / 3)),
                  round(lerp(color1[2], color2[2], 2 / 3)),
                  255]
    return [color1, color2, color3, color4]

def interpolate_alpha(alpha1, alpha2):
    alpha = [alpha1, alpha2]
    if alpha1 > alpha2:
        alpha.extend([math.floor(lerp(alpha1, alpha2, 1 / 7)),
                      math.floor(lerp(alpha1, alpha2, 2 / 7)),
                      math.floor(lerp(alpha1, alpha2, 3 / 7)),
                      math.floor(lerp(alpha1, alpha2, 4 / 7)),
                      math.floor(lerp(alpha1, alpha2, 5 / 7)),
                      math.floor(lerp(alpha1, alpha2, 6 / 7))])
    else:
        alpha.extend([math.floor(lerp(alpha1, alpha2, 1 / 5)),
                      math.floor(lerp(alpha1, alpha2, 2 / 5)),
                      math.floor(lerp(alpha1, alpha2, 3 / 5)),
                      math.floor(lerp(alpha1, alpha2, 4 / 5)),
                      0,
                      255])
    return alpha

def expand_clusters(clusters, reverse=False):
    output = collections.deque()
    for row in clusters:
        row1 = []
        row2 = []
        row3 = []
        row4 = []
        for cluster in row:
            for pixel in cluster[0]:
                row1.extend(pixel)
            for pixel in cluster[1]:
                row2.extend(pixel)
            for pixel in cluster[2]:
                row3.extend(pixel)
            for pixel in cluster[3]:
                row4.extend(pixel)
        if reverse:
            output.extendleft([row1, row2, row3, row4])
        else:
            output.extend([row1, row2, row3, row4])
    return list(output)

def get_color_index(indices, pixel):
    return (indices >> (2 * (15 - pixel))) & 0x03

def read_6_bytes(handler):
    num1, num2 = read('<H', 2, handler), read('<I', 4, handler)
    return (num2 << 16) | num1

# BCn Decoders

def decode_bc1(data, width, height):
    data = io.BytesIO(data)
    clusters = []

    for row_index in range(math.floor(height / 4)):
        row = []
        for column_index in range(math.floor(width / 4)):
            color_values = interpolate_color(read('<H', 2, data), read('<H', 2, data), True)
            color_indices = read('>I', 4, data)
            cluster = []

            for y in range(4):
                cluster_row = []
                for x in range(4):
                    pixel_index = 3 - x + (y * 4)
                    color_index = get_color_index(color_indices, pixel_index)
                    pixel = color_values[color_index]
                    cluster_row.append(pixel)
                cluster.append(cluster_row)
            row.append(cluster)
        clusters.append(row)

    return expand_clusters(clusters, True)

def decode_bc2(data, width, height, premultiplied):
    data = io.BytesIO(data)
    clusters = []

    for row_index in range(math.floor(height / 4)):
        row = []
        for column_index in range(math.floor(width / 4)):
            alpha_values = read('<Q', 8, data)
            color_values = interpolate_color(read('<H', 2, data), read('<H', 2, data), False)
            color_indices = read('>I', 4, data)
            cluster = []

            for y in range(4):
                cluster_row = []
                for x in range(4):
                    pixel_index = 3 - x + (y * 4)
                    color_index = get_color_index(color_indices, pixel_index)
                    alpha_value = ((alpha_values >> (4 * (15 - pixel_index))) & 0x0F) * 17
                    multiplier = 255 / alpha_value if premultiplied else 1
                    pixel = color_values[color_index]
                    pixel = [round(component * multiplier) for component in pixel]
                    cluster_row.append(pixel)
                cluster.append(cluster_row)
            row.append(cluster)
        clusters.append(row)

    return expand_clusters(clusters, True)

def decode_bc3(data, width, height, premultiplied):
    data = io.BytesIO(data)
    clusters = []

    for row_index in range(math.floor(height / 4)):
        row = []
        for column_index in range(math.floor(width / 4)):
            alpha_values = interpolate_alpha(read('<B', 1, data), read('<B', 1, data))
            alpha_indices = read_6_bytes(data)
            color_values = interpolate_color(read('<H', 2, data), read('<H', 2, data), False)
            color_indices = read('>I', 4, data)
            cluster = []

            for y in range(4):
                cluster_row = []
                for x in range(4):
                    pixel_index = 3 - x + (y * 4)
                    color_index = get_color_index(color_indices, pixel_index)
                    alpha_index = (alpha_indices >> (3 * (15 - pixel_index))) & 0x07
                    alpha_value = alpha_values[alpha_index]
                    multiplier = 255 / alpha_value if premultiplied else 1
                    pixel = color_values[color_index]
                    pixel = [round(component * multiplier) for component in pixel]
                    pixel[3] = alpha_value # Set to correct alpha value
                    cluster_row.append(pixel)
                cluster.append(cluster_row)

            # Digusting hack - no idea why this is necessary but it fixes the problem so
            cluster_copy = copy.deepcopy(cluster)
            for y in range(4):
                for x in range(4):
                    cluster[y][x][3] = cluster_copy[3 - y][x][3]

            row.append(cluster)
        clusters.append(row)

    return expand_clusters(clusters, False)
