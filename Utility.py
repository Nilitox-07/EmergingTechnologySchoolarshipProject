import math

def ManhattanDistance(position_1: tuple[int, int], position_2: tuple[int, int]) -> tuple[int, int]:
    '''
    This function will return the distance in x and y of 2 points
    '''
    x: int = abs(position_1[0] - position_2[0])
    y: int = abs(position_1[1] - position_2[1])
    return (x, y)