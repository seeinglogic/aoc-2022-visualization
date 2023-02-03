'''
Step 1. Networkx solution
Turned the original solution into a networkx solution
'''
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time

if len(sys.argv) == 2:
    infile = sys.argv[1]
else:
    infile = 'i.txt'

grid = []

for l in open(infile).readlines():
    l = l.strip()
    if not l:
        continue
    grid.append(list(l))
    
width = len(grid[0])
height = len(grid)


def can_move (cur, dst):
    aliases = {
        'S': 'a',
        'E': 'z'
    }
    if cur in aliases:
        cur = aliases[cur]
    if dst in aliases:
        dst = aliases[dst]

    diff = ord(dst) - ord(cur)
    # invalid move
    # RIGHT
    if diff > 1:
        return False
    # WRONG
    #if abs(diff) > 1:
    #    return False
    return True


def get_height(pos):
    x, y = pos
    return grid[y][x]



directions = [
    (-1,  0),
    ( 1,  0),
    ( 0, -1),
    ( 0,  1),
]

# Build the graph
print('[*] Building graph...')
g = nx.DiGraph()
for y in range(height):
    for x in range(width):
        # record
        if grid[y][x] == 'S':
            start_pos = (x, y)
        if grid[y][x] == 'E':
            end_pos = (x, y)

        # check in each of the four directions and add edges for valid moves
        for (dx, dy) in directions:
            other_pos = (x + dx, y + dy)
            ox, oy = other_pos
            if ox < 0 or ox >= width or oy < 0 or oy >= height:
                continue

            cur_pos = (x, y)
            if can_move(get_height(cur_pos), get_height(other_pos)):
                g.add_edge(cur_pos, other_pos)
 
print(f'[*] Graph has {len(g.nodes)} nodes and {len(g.edges)} edges')

# Phase 0 - no graphics, but we...
# This file has the right answer, so this works
shortest_path = nx.shortest_path(g, start_pos, end_pos)
# Networkx includes the starting node in the shortest path, unlike the problem
shortest_path.remove(start_pos)
#print(f'[*] {shortest_path=}')
print(f'[A] {len(shortest_path)=}')

# Phase 1 - just drawing with nx and plt
#print('nx.draw(g)...', end='')
#start_time = time.time()
#nx.draw(g, node_size=2)
#duration = time.time() - start_time
#print(f' finished in {duration:.02f} seconds')
## Test took 154.81 seconds
#filename = 'fixed-digraph0.png'
#print(f'[*] plt.savefig({filename})...')
#plt.savefig(filename, format="PNG")

# We need a bit more data to improve the graph
def get_metadata(g):
    position_dict = {}
    colors = []
    labels = {}
    for cur_pos in g.nodes:
        x, y = cur_pos

        position_dict[cur_pos] = [x/width, y/height]

        if cur_pos == start_pos:
            cur_color = 'green'
        elif cur_pos == end_pos:
            cur_color = 'red'
        else:
            cur_color = 'skyblue'
        colors.append(cur_color)

        cur_label = grid[y][x]
        labels[cur_pos] = cur_label

    return position_dict, colors, labels

position_dict, colors, labels = get_metadata(g)

# Phase 2 - put nodes in positions and color start and finish
#start_time = time.time()
#print('nx.draw(g)...', end='')
#nx.draw(g, pos=position_dict, node_color=colors, node_size=4)
#duration = time.time() - start_time
#print(f' finished in {duration:.02f} seconds')
## Test took 0.62 seconds
#filename = 'fixed-digraph1.png'
#print(f'plt.savefig({filename})...')
#plt.savefig(filename, format="PNG")


# Phase 3 - Improve the graph by making it bigger and adding labels
#plt.figure(figsize=(40,24))
#print('nx.draw(g)...', end='')
#start_time = time.time()
#nx.draw(g, pos=position_dict, labels=labels, node_color=colors, node_size=160)
#duration = time.time() - start_time
#print(f' finished in {duration:.02f} seconds')
## Test took 2.12 seconds
#filename = 'fixed-digraph2.png'
#print(f'[*] plt.savefig({filename})...', end='')
#start_time = time.time()
#plt.savefig(filename, format="PNG")
#duration = time.time() - start_time
#print(f' finished in {duration:.02f} seconds')
## Test took 4.74 seconds

# Phase 4 - use force-directed layout to see if we can see a disconnect
#plt.figure(figsize=(40,24))
#print('nx.draw(g)...', end='')
#start_time = time.time()
#nx.draw_spring(g, node_color=colors, node_size=120)
##nx.draw_kamada_kawai(g, node_color=colors, node_size=120)
#duration = time.time() - start_time
#print(f' finished in {duration:.02f} seconds')
## Spring took 63.33 seconds
## Kamada Kawai took 469.08 seconds
#filename = "fixed-digraph3-spring.png"
##filename = "fixed-digraph3-kamada_kawai.png"
#print(f'[*] plt.savefig({filename})...', end='')
#start_time = time.time()
#plt.savefig(filename, format="PNG")
#duration = time.time() - start_time
#print(f' finished in {duration:.02f} seconds')
## Test took 4.74 seconds


# Phase 5: color nodes differently if they're reachable
#print(f'[*] Calculating descendants...', end='')
#start_time = time.time()
#reachable_nodes = nx.descendants(g, start_pos)
#duration = time.time() - start_time
#print(f' finished in {duration:.02f} seconds')
#
#updated_colors = []
#for i, cur_pos in enumerate(g.nodes):
#    old_color = colors[i]
#    if cur_pos in [start_pos, end_pos] or cur_pos in reachable_nodes:
#        new_color = old_color
#    # unreachable nodes
#    else:
#        new_color = 'orchid'
#    updated_colors.append(new_color)
#
#plt.figure(figsize=(40,24))
#print('nx.draw(g)...', end='')
#start_time = time.time()
#nx.draw(g, pos=position_dict, labels=labels, node_color=updated_colors, node_size=160)
#duration = time.time() - start_time
#print(f' finished in {duration:.02f} seconds')
## Test took 17.64 seconds
#filename = 'fixed-digraph4.png'
#print(f'[*] plt.savefig({filename})...', end='')
#start_time = time.time()
#plt.savefig(filename, format="PNG")
#duration = time.time() - start_time
#print(f' finished in {duration:.02f} seconds')
### Test took 10.09 seconds

# Phase 6: color nodes on the shortest path
print(f'[*] Calculating descendants...', end='')
start_time = time.time()
reachable_nodes = nx.descendants(g, start_pos)
duration = time.time() - start_time
print(f' finished in {duration:.02f} seconds')

updated_colors = []
for i, cur_pos in enumerate(g.nodes):
    old_color = colors[i]
    # Start, end, and untraveled nodes remain the same
    if cur_pos not in shortest_path or cur_pos in [start_pos, end_pos]:
        new_color = old_color
    # highlight traveled nodes
    else:
        new_color = 'orchid'
    updated_colors.append(new_color)

plt.figure(figsize=(40,24))
print('[*] nx.draw(g)...', end='')
sys.stdout.flush()
start_time = time.time()
nx.draw(g, pos=position_dict, labels=labels, node_color=updated_colors, node_size=160)
duration = time.time() - start_time
print(f' finished in {duration:.02f} seconds')
# Test took 17.64 seconds
filename = 'fixed-digraph5.png'
print(f'[*] plt.savefig({filename})...', end='')
start_time = time.time()
plt.savefig(filename, format="PNG")
duration = time.time() - start_time
print(f' finished in {duration:.02f} seconds')
# Test took 10.09 seconds

# export data as json
node_data = []
i = 0
shortest_path.insert(0, start_pos)
shortest_path.append(end_pos)
for y in range(height):
    for x in range(width):
        height = grid[y][x]
        # Since we have a shortest path, use that
        covered = (x,y) in shortest_path
        node_info = {
            'pos': (x, y),
            'x': x,
            'y': y,
            'i': i,
            'height': height,
            'covered': covered,
        }
        node_data.append(node_info)
        i += 1

import json
filename = 'day12-right.json'
with open(filename, 'w') as f:
    json.dump(node_data, f)
    print(f'[+] Wrote json to {filename}')
