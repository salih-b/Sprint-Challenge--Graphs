from room import Room
from player import Player
from world import World
from queue import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player("Player1", world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

cache_r = {}
def retrieve_unvisited_rooms(starting_room):
    q = Queue()
    room = cache_r[starting_room]
    for direction, id in room.items():
        q.enqueue([(direction, id)])
    visited = set()

    while q.size() > 0:
        path = q.dequeue()
        room_id = path[-1][1]
        if room_id not in visited:
            if room_id is None:
                path_to_travel = [room[0] for room in path]
                return path_to_travel
            visited.add(room_id)
            for direction, id in cache_r[room_id].items():
                new_path = list(path)
                new_path.append((direction, id))
                q.enqueue(new_path)


def make_exit():
    for room_exit in player.current_room.get_exits():
        room_id = player.current_room.id

        if room_id not in cache_r:
            cache_r[room_id] = {}
        if room_exit not in cache_r[room_id]:
            cache_r[room_id][room_exit] = None


def traverse_rooms():
    make_exit()
    current_id = player.current_room.id

    # Check if current room has an unvisited exit and if so visit it
    for direction, room_id in cache_r[current_id].items():
        if room_id is None:
            traversal_path.append(direction)
            player.travel(direction)
            make_exit()

            new_id = player.current_room.id
            cache_r[current_id][direction] = new_id

            if direction == 'n':
                cache_r[new_id]['s'] = current_id
            elif direction == 's':
                cache_r[new_id]['n'] = current_id
            elif direction == 'w':
                cache_r[new_id]['e'] = current_id
            else:
                cache_r[new_id]['w'] = current_id

            return traverse_rooms()

    # If current room has no unvisited exits check if any room in cache has one and head there before looping
    for room in cache_r:
        if None in cache_r[room].values():
            for direction in retrieve_unvisited_rooms(current_id):
                traversal_path.append(direction)
                player.travel(direction)
            return traverse_rooms()
traverse_rooms()

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
