import pygame
import json

pygame.init()

#Here we are gonna place the colors we use.

black = (0, 0, 0)
brown = (128, 64, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue= (0, 0, 255)
green = (0, 255, 0)
purple = (255, 0, 255)
white = (255, 255, 255)

def draw_grid(screen):
    #In here we will display our grid onto the screen.
    for x in range(0, width):
        pygame.draw.line(screen, black, (x * length, 0), (x * length, height * length), 2)
    for y in range(0, height):
        pygame.draw.line(screen, black, (0, y * length), (width * length, y * length), 2)

width = 20
height = 20

length = 20

screen = pygame.display.set_mode((width * length, height * length))

run = True



with open('Tests/levels_test_grid.json', 'r') as File:
    data = json.load(File)



for key, val in data.items():
     
    grid = val
    
    screen.fill(white)
    
    for r, row in enumerate(grid):
        for c, column in enumerate(row):
            if grid[r][c] == 0:
                pass
            elif grid[r][c] == 1:
                pygame.draw.rect(screen, green, ((c * length, r * length), (length, length)))
            elif grid[r][c] == 2:
                pygame.draw.rect(screen, black, ((c * length, r * length), (length, length)))
            elif grid[r][c] == 3:
                pygame.draw.rect(screen, brown, ((c * length, r * length), (length, length)))
            elif grid[r][c] == 4:
                pygame.draw.rect(screen, red, ((c * length, r * length), (length, length)))
            elif grid[r][c] == 5:
                pygame.draw.rect(screen, yellow, ((c * length, r * length), (length, length)))
            elif grid[r][c] == 6:
                pygame.draw.rect(screen, purple, ((c * length, r * length), (length, length)))
                
    draw_grid(screen)      
    
    pygame.display.flip()
    
    pygame.image.save(screen, f"Tests/GridTests/screenshot{key}.png")