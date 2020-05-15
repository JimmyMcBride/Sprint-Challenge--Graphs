from room import Room
from player import Player
from world import World
from utils import Graph
from utils import Stack

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
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ["n", "n"]
traversal_path = []
graph = Graph()
back_track = Stack()


def inverse(step):
    if step == "n":
        return "s"
    if step == "s":
        return "n"
    if step == "e":
        return "w"
    if step == "w":
        return "e"


def next_direction(current_room):
    for direction, room_id in graph.get_room_exits(current_room):
        next_room = current_room.get_room_in_direction(direction)
        if graph.has_room(next_room) is False:
            if room_id == None:
                return direction
    return None


def traverse(direction):
    player.travel(direction)
    traversal_path.append(direction)
    back_track.push(inverse(direction))


def retreat(direction):
    player.travel(direction)
    traversal_path.append(direction)


def traverse_the_fog():

    graph.add_room(player.current_room.id, player.current_room.get_exits())

    while graph.size() < len(world.rooms):
        current_room = player.current_room

        if graph.has_room(current_room) is False:
            graph.add_room(current_room.id, current_room.get_exits())
        direction = next_direction(current_room)

        if direction is None:
            fog_has_been_traversed = False

            while fog_has_been_traversed is False:
                step = back_track.pop()
                current_room = player.current_room
                prev_room = current_room.get_room_in_direction(step)
                retreat(step)
                graph.add_exit(prev_room, inverse(step), current_room)
                prev_room_exits = graph.get_room_exits(prev_room)
                for ex in prev_room_exits:
                    # print(ex)
                    if ex[1] == None:
                        fog_has_been_traversed = True

        else:
            next_room = current_room.get_room_in_direction(direction)
            if graph.has_room(next_room) is False:
                graph.add_room(next_room.id, next_room.get_exits())
                graph.add_exit(next_room, inverse(direction), current_room)

            traverse(direction)


traverse_the_fog()


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited"
    )
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
# print("starting room:", world.starting_room)
# cmds = input("-> ").lower().split(" ")
# if cmds[0] in ["n", "s", "e", "w"]:
#     player.travel(cmds[0], True)
# elif cmds[0] == "q":
#     break
# else:
#     print("I did not understand that command.")
