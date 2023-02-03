import re
import sys
import time

if len(sys.argv) == 2:
    infile = sys.argv[1]
else:
    infile = 'i.txt'

output = 0
stream = ''
for l in open(infile).readlines():
    l = l.strip()
    if not l:
        continue
    stream += l


# written top-to-bottom (intuitive display)
blocks = {
    '-': [
        [2,3,4,5]
    ],
    '+': [
        [3],
        [2,3,4],
        [3],
    ], 
    'L': [
        [4],
        [4],
        [2,3,4],
    ], 
    'I': [
        [2],
        [2],
        [2],
        [2],
    ], 
    'x': [
        [2,3],
        [2,3],
    ], 
}
# reverse the blocks rows once to make adding them easier
blocks = {k: v[::-1] for k,v in blocks.items()}

order = ['-', '+', 'L', 'I', 'x']
arena_width = 7
tallest_point = -1  # floor is technically at -1 in my coord system
drop_height = tallest_point + 1 + 3  # the floor/block itself adds 1 height
filled_positions = set()  # Fixed block positions will be mapped as (x, y)
cur_block = []  # list of (x,y) points


def create_block(name):
    block_rows = blocks[name]
    cur_block = []
    for y, row in enumerate(block_rows):
        for x in row:
            cur_block.append((x, drop_height + y))
    return cur_block


def print_arena(block_coords, filled_positions):
    max_y = 0
    if block_coords:
        max_y = max(max_y, max(xy[1] for xy in block_coords))
    if filled_positions:
        max_y= max(max_y, max(xy[1] for xy in filled_positions))

    for row_y in range(max_y, -1, -1):
        row_chars = '|'
        for x in range(arena_width):
            point = (x, row_y)
            if point in filled_positions:
                row_chars += '#'
            elif point in block_coords:
                row_chars += '@'
            else:
                row_chars += '.'
        row_chars += '|'
        print(row_chars)
    print('+-------+')
    print()

    

shift_left = lambda xy: (xy[0] - 1, xy[1])
shift_right = lambda xy: (xy[0] + 1, xy[1])
shift_down = lambda xy: (xy[0], xy[1] - 1)

stream_index = 0
stream_len = len(stream)

# only need enough to show a pattern
num_rocks =  10000
top_points = []
print(f'[*] Simulating {num_rocks} blocks...')
for i in range(num_rocks):
    block_type = order[i % len(order)]
    block_coords = create_block(block_type)
    while True:
        # cycle: push, then fall down one
        push = stream[stream_index % stream_len]
        stream_index += 1

        if push == '<':
            shifted_coords = list(map(shift_left, block_coords))
            if not any(
                xy[0] < 0 or xy in filled_positions
                for xy 
                in shifted_coords
            ):
                block_coords = shifted_coords
        else:
            shifted_coords = list(map(shift_right, block_coords))
            if not any(
                xy[0] >= arena_width or xy in filled_positions
                for xy
                in shifted_coords
            ):
                block_coords = shifted_coords

        # fall
        shifted_coords = list(map(shift_down, block_coords))
        # when a rock would be blocked downwards, it stops
        if any(xy in filled_positions or xy[1] < 0 for xy in shifted_coords):
            filled_positions.update(block_coords)
            #print(f'DBG: fall is blocked')
            last_pos = block_coords[-1]
            break
        else:
            block_coords = shifted_coords
            #print(f'DBG: fall 1 unit')

    # update tallest_point
    tallest_new_point = max(xy[1] for xy in block_coords)
    if tallest_new_point > tallest_point:
        tallest_point = tallest_new_point
        drop_height = tallest_point + 1 + 3  # the floor/block itself adds 1 height
        #print(f'DBG: New drop height: {drop_height}')

    # record heights so we can calculate periods later
    block_info = {
        'x': last_pos[0],
        'y': last_pos[1],
        'i': i,
        'block_type': block_type,
        'height': tallest_point + 1,
    }
    top_points.append(block_info)


import json
outfile = 'day17.json'
with open(outfile, 'w') as f:
    json.dump(top_points, f)
    print(f'[+] Wrote JSON output to {outfile}')
# NOTE: The cycle size for this input is 1745
