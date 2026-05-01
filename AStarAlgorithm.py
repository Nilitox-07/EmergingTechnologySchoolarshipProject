from Utility import ManhattanDistance
import heapq

def AddManhattanDistance(point_1: tuple[int, int], point_2: tuple[int, int]) -> int:
    x, y = ManhattanDistance(point_1, point_2)
    return x + y

def ReconstructPath(current: tuple[int, int], exit_1: tuple[int, int], tunnel: dict) -> list[tuple[int, int]]:
    path = []
    while current in tunnel:
        path.append(current)
        current = tunnel[current]
    path.append(exit_1)
    path.reverse()
    return path

def AStarAlgorithm(exit_1: tuple[int, int], exit_2: tuple[int, int], grid: list[list[int]], size: tuple[int, int]) -> list[tuple[int, int]]:
    '''
    This Algorithm will return the units to connect an exit to another exit.
    If along the way, it finds a tunnel it will just stop.
    '''
    open_set: list[tuple[int, tuple[int, int]]] = []
    heapq.heappush(open_set, (0, exit_1))
    tunnel = {}
    g_score = {exit_1: 0}

    while open_set:

        current = heapq.heappop(open_set)[1]

        if current == exit_2:
            return ReconstructPath(current, exit_1, tunnel)
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)

            if neighbor[0] < 0 or neighbor[0] >= size[1] or neighbor[1] < 0 or neighbor[1] >= size[0]:
                continue
            
            possible_obstacles = [1, 3, 4, 5, 6, 7]

            if grid[neighbor[1]][neighbor[0]] in possible_obstacles:
                continue
            
            ''' This is was an attempt to fix the tunnels not forming their own room
            if grid[neighbor[1]][neighbor[0]] == 2:
                tunnel[neighbor] = current
                return ReconstructPath(current, exit_1, tunnel)
            '''
            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                tunnel[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + AddManhattanDistance(neighbor, exit_2)
                heapq.heappush(open_set, (f_score, neighbor))
    print("No path found")