
'''
So what does this need to do.

Set up the Dungeon Grid.
It will be a 20 by 20 area and the first one always needs to have a Safe Area, In this safe area you return Home with your loot.

Randomly Selecting 1 unit from the 5 by 5 dungeon.
This all need to be connected. This game will also test how good you remember your way back to this safe room
Every time you go to a new grid. The Difficulty will increase, this dificulty is saved by the character selected.

Each Character will have its own save file.
Depending on where the unit is selected, there should be an exit to every possible side.

There is going to be a boss every 5 Fight Rooms Checked.
'''
from __future__ import annotations

import copy
import json
import random

from AStarAlgorithm import AStarAlgorithm
from Utility import ManhattanDistance

class LevelCreation:
    def __init__(self, player: main.Player, is_first_room: bool = False):
        '''
        Parameters:
            is_first_room (bool): If True, this room will include a Safe Area which means is the first room in a dungeon, otherwise it will include a Rest Room.
            player (Player): This will give reference to the character in the dungeon
        '''
        self.player = player
        self.is_first_room = is_first_room

    def DungeonStart(self, size: tuple[int, int] = (5, 5)) -> None:
        '''
        This will start the Dungeon 2D Array in the size of the size var.

        It will just have 0 and 1 for either if the level has appeared or not.
        '''
        self.dungeon_grid: list[list[int]] = [[0 for _ in range(size[0])] for _ in range(size[1])]

        x_position: int = random.randint(0, size[0] - 1)
        y_position: int = random.randint(0, size[1] - 1)

        self.player.dungeon_position = (x_position, y_position)

    def StartGrid(self) -> None:
        '''
        This will initialize the grid of this said level in a 2D Array.
        0 Empty
        1 is Safe Area/Rest Area
        2 Tunnel
        3 Wall
        4 Fight Room
        5 Chest Room
        6 Store
        7 Boss Room

        Pseudo-Code

        1. Initialize Empty Grid
        2. Select a Random Spot for the Safe Area
        3. Enclose it with Walls
        4. Spawn 1 Fight Room in a random place
        5. Enclose it with Walls
        6. Spawn 1 Chest Room in a random place
        7. Enclose it with Walls
        - Now starts the RNG
        8. Depending on how many Stores have been opened, start with a 90% Chance for a Store to spawn in a random place 
           (Will lower by 10 every opened store stoping at 10%)
        9. If spawned, Enclose it with Walls
        10. 50% Chance of spawning a 2nd Fight Room.
        11. If spawned, Enclose it with Walls
        12. Connect all rooms with tunnels, in corresponding to the nearest one to them.
            If they are they are the closest one to a wall, they will have a passage to 
            the unit to that side.
        '''

        grid_size: tuple[int, int] = (20, 20)

        all_centers: list[tuple[int, int]] = []

        all_exits: list[list[tuple[int, int]]] = []

        directions: list[tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        # 1

        self.grid: list[list[int]] = [[0 for _ in range(grid_size[0])] for _ in range(grid_size[1])]

        # 2 and 3
        # Safe Area/Rest Area, is a 3 by 5 Area and the x_pos and y_pos is the center, we are offsetting that center to a corner and looping through all the area

        x_position: int = random.randint(2, grid_size[0] - 3)
        y_position: int = random.randint(3, grid_size[1] - 4)

        self.safe_area_center: tuple[int, int] = (x_position, y_position)
        all_centers.append(self.safe_area_center)

        for y in range(y_position - 3, y_position + 4):
            for x in range(x_position - 2, x_position + 3):
                if y == y_position - 3 or x == x_position - 2 or y == y_position + 3 or x == x_position + 2:
                    self.grid[y][x] = 3
                else:
                    self.grid[y][x] = 1
        safe_area_exits: list[tuple[int, int]] = [(self.safe_area_center[0] - 2, self.safe_area_center[1]), 
                                                (self.safe_area_center[0], self.safe_area_center[1] + 3),
                                                (self.safe_area_center[0] + 2, self.safe_area_center[1]),
                                                (self.safe_area_center[0], self.safe_area_center[1] - 3)]
        all_exits.append(safe_area_exits)

        # 4 and 5
        while True:

            x_position: int = random.randint(3, grid_size[0] - 4)
            y_position: int = random.randint(3, grid_size[1] - 4)

            fight_area_one_center: tuple[int, int] = (x_position, y_position)
            x, y = ManhattanDistance(self.safe_area_center, fight_area_one_center)

            if x > 6 or y > 7:
                for y in range(y_position - 3, y_position + 4):
                    for x in range(x_position - 3, x_position + 4):
                        if y == y_position - 3 or x == x_position - 3 or y == y_position + 3 or x == x_position + 3:
                            self.grid[y][x] = 3
                        else:
                            self.grid[y][x] = 4
                all_centers.append(fight_area_one_center)
                break

        fight_area_one_exits: list[tuple[int, int]] = [(fight_area_one_center[0] - 3, fight_area_one_center[1]), 
                                                    (fight_area_one_center[0], fight_area_one_center[1] + 3),
                                                    (fight_area_one_center[0] + 3, fight_area_one_center[1]),
                                                    (fight_area_one_center[0], fight_area_one_center[1] - 3)]
        
        all_exits.append(fight_area_one_exits)

        # 6 and 7

        while True:

            x_position: int = random.randint(2, grid_size[0] - 3)
            y_position: int = random.randint(2, grid_size[1] - 3)

            chest_room_one_center: tuple[int, int] = (x_position, y_position)
            x_1, y_1 = ManhattanDistance(chest_room_one_center, self.safe_area_center)
            x_2, y_2 = ManhattanDistance(chest_room_one_center, fight_area_one_center)

            if (x_1 > 5 or y_1 > 6) and (x_2 > 6 or y_2 > 6):
                for y in range(y_position - 2, y_position + 3):
                    for x in range(x_position - 2, x_position + 3):
                        if y == y_position - 2 or x == x_position - 2 or y == y_position + 2 or x == x_position + 2:
                            self.grid[y][x] = 3
                        else:
                            self.grid[y][x] = 5
                all_centers.append(chest_room_one_center)
                break
        
        chest_room_one_exits: list[tuple[int, int]] = [(chest_room_one_center[0] - 2, chest_room_one_center[1]), 
                                                        (chest_room_one_center[0], chest_room_one_center[1] + 2),
                                                        (chest_room_one_center[0] + 2, chest_room_one_center[1]),
                                                        (chest_room_one_center[0], chest_room_one_center[1] - 2)]
        
        all_exits.append(chest_room_one_exits)

        # 8 and 9

        chance: float = 0.9
        for _ in range(self.player.stores_opened):
            if chance > 0.1:
                chance -= 0.1

        is_there_a_store: bool = False

        while True:
            if random.random() < chance:
                for _ in range(1000):
                    x_position: int = random.randint(3, grid_size[0] - 4)
                    y_position: int = random.randint(3, grid_size[1] - 4)
                    
                    store_center: tuple[int, int] = (x_position, y_position)
                    x_1, y_1 = ManhattanDistance(store_center, self.safe_area_center)
                    x_2, y_2 = ManhattanDistance(store_center, fight_area_one_center)
                    x_3, y_3 = ManhattanDistance(store_center, chest_room_one_center)

                    if (x_1 > 6 or y_1 > 6) and (x_2 > 7 or y_2 > 6) and (x_3 > 6 or y_3 > 5):
                        for y in range(y_position - 2, y_position + 3):
                            for x in range(x_position - 3, x_position + 4):
                                if y == y_position - 2 or x == x_position - 3 or y == y_position + 2 or x == x_position + 3:
                                    self.grid[y][x] = 3
                                else:
                                    self.grid[y][x] = 6
                        is_there_a_store = True
                        all_centers.append(store_center)
                        break
                break
            else:
                break
        
        if is_there_a_store:
            store_exits: list[tuple[int, int]] = [(store_center[0] - 3, store_center[1]), 
                                                (store_center[0], store_center[1] + 2),
                                                (store_center[0] + 3, store_center[1]),
                                                (store_center[0], store_center[1] - 2)]
            all_exits.append(store_exits)

        # 10 and 11

        is_there_a_second_fight_zone = False

        while True:
            if random.random() < 0.5: # 50 Percent Chance to spawn 2nd Fight Room
                for _ in range(1000):
                    x_position: int = random.randint(3, grid_size[0] - 4)
                    y_position: int = random.randint(3, grid_size[1] - 4)

                    fight_area_two_center: tuple[int, int] = (x_position, y_position)
                    x_1, y_1 = ManhattanDistance(fight_area_two_center, self.safe_area_center)
                    x_2, y_2 = ManhattanDistance(fight_area_two_center, fight_area_one_center)
                    x_3, y_3 = ManhattanDistance(fight_area_two_center, chest_room_one_center)
                    check_one = True
                    if is_there_a_store:
                        x_4, y_4 = ManhattanDistance(fight_area_two_center, store_center)
                        check_one = (x_4 > 7 or y_4 > 6)

                    if (x_1 > 6 or y_1 > 7) and (x_2 > 7 or y_2 > 7) and (x_3 > 6 or y_3 > 6) and check_one:
                        for y in range(y_position - 3, y_position + 4):
                            for x in range(x_position - 3, x_position + 4):
                                if y == y_position - 3 or x == x_position - 3 or y == y_position + 3 or x == x_position + 3:
                                    self.grid[y][x] = 3
                                else:
                                    self.grid[y][x] = 4
                        is_there_a_second_fight_zone = True
                        all_centers.append(fight_area_two_center)
                        break
                break
            else:
                break
        
        if is_there_a_second_fight_zone:
            fight_area_two_exits: list[tuple[int, int]] = [(fight_area_two_center[0] - 3, fight_area_two_center[1]), 
                                                        (fight_area_two_center[0], fight_area_two_center[1] + 3),
                                                        (fight_area_two_center[0] + 3, fight_area_two_center[1]),
                                                        (fight_area_two_center[0], fight_area_two_center[1] - 3)]
        
            all_exits.append(fight_area_two_exits)

        # 12

        all_centers_v2 = copy.deepcopy(all_centers)

        for i in range(len(all_centers) - 1, -1, -1):
            room = all_centers[i]
            del all_centers[i]
            for j, check_room in enumerate(all_centers):
                x, y = ManhattanDistance(room , check_room)
                least_distance = 40
                index_1 = 0
                index_2 = 0
                if x + y <= 19: # 19 Tiles Away of the Center
                    for h, exit_1 in enumerate(all_exits[i]):
                        for k, exit_2 in enumerate(all_exits[j]):
                            x_1, y_1 = ManhattanDistance(exit_1, exit_2)
                            if x_1 + y_1 < least_distance and abs(h - k) % 2 == 0:
                                least_distance = x_1 + y_1
                                index_1 = h
                                index_2 = k
                                
                    self.grid[all_exits[i][index_1][1]][all_exits[i][index_1][0]] = 0
                    self.grid[all_exits[j][index_2][1]][all_exits[j][index_2][0]] = 0

                    tunnel_1 = all_exits[i][index_1]
                    tunnel_2 = all_exits[j][index_2]
                    
                    tunnel = AStarAlgorithm(tunnel_1, tunnel_2, self.grid, grid_size)

                    if tunnel != None:
                        for unit in tunnel:
                            self.grid[unit[1]][unit[0]] = 2

                    self.grid[all_exits[i][index_1][1]][all_exits[i][index_1][0]] = 2
                    self.grid[all_exits[j][index_2][1]][all_exits[j][index_2][0]] = 2

        shortest_exit_left = (0, 0)
        shortest_exit_down = (0, 19)
        shortest_exit_right = (19, 19)
        shorters_exit_up = (19, 0)

        left = 40
        down = 40
        right = 40
        up = 40

        for c, center in enumerate(all_centers_v2):
            for e, exit in enumerate(all_exits[c]):
                if self.grid[exit[1]][exit[0]] == 2:
                    continue
                else:
                    x, y = ManhattanDistance(exit, (-1, -1))
                    if x < left:
                        shortest_exit_left = exit
                        left = x
                    if 21 - x < right:
                        shortest_exit_right = exit
                        right = 21 - x
                    if y < up:
                        shorters_exit_up = exit
                        up = y
                    if 21 - y < down:
                        shortest_exit_down = exit
                        down = 21 - y

        shortest_exits = [shortest_exit_left, shortest_exit_down, shortest_exit_right, shorters_exit_up]
        sides = [left, down, right, up]

        possible_directions = [True] * 4

        for d, dir in enumerate(directions):
            dx, dy = dir
            x, y = self.player.dungeon_position
            if 0 <= x + dx < len(self.dungeon_grid) and 0 <= y + dy < len(self.dungeon_grid):
                pass
            else:
                possible_directions[d] = False

        for s, short_exit in enumerate(shortest_exits):
            x, y = short_exit
            if not possible_directions[s]:
                continue
            for d in range(sides[s]):
                self.grid[y + (d * directions[s][1])][x + (d * directions[s][0])] = 2

        all_directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

        for c, col in enumerate(self.grid):
            for r, row in enumerate(col):
                if row == 2:
                    for dir in all_directions:
                        dx, dy = dir
                        x, y = (dx + r, dy + c)
                        if 0 <= x < grid_size[0] and 0 <= y < grid_size[1]:
                            if self.grid[y][x] == 0:
                                self.grid[y][x] = 3


if __name__ == '__main__':

    import main

    counter = 0
    json_dump = {}
    for _ in range(100):
        counter += 1
        testPlayer = main.Player(main.Game(main.Core()), (0, 0))
        testClass = LevelCreation(testPlayer)
        testClass.DungeonStart()
        testClass.StartGrid()
        del testPlayer
        json_dump[f"{counter}"] = testClass.grid
    with open('Tests/levels_test_grid.json', 'w') as File:
        json.dump(json_dump, File, indent=4)
