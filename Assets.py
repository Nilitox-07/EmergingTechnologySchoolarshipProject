import pygame
import os
import random
import sys

# This gets the path of wher ethe folder is located, and checking if its a .py or .exe

if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

All_Characters_Images: dict[str, str] = {'Wraith' : ["Wraith_01", "Wraith_02", "Wraith_03"],
                                         'Satyr' : ["Satyr_01", "Satyr_02", "Satyr_03"],
                                         'Minotaur' : ["Minotaur_01", "Minotaur_02", "Minotaur_03"],
                                         'Golem' : ["Golem_01", "Golem_02", "Golem_03"]}

Attacking = "Attacking"
Dying = "Dying"
Hurt = "Hurt"
Idle = "Idle"
Walking = "Walking"

def Characters_Image(Name: str, image_number: int, scale: float, sequence: str = "Idle", sequence_number: int = 0, sequence_clock: int = 0, sequence_clock_original: int = 0, moving_right: bool = False) -> tuple[pygame.Surface, int, float, float, int]:
    '''
    Creates and returns the image of the player
    
    Parameters:
        Name (str): The name of the Character being retrived
        image_number (int): Which style needs to be retrived
        scale (float): The image will be scaled down by this number
        sequence (str): For the type of animation
        sequence_number (int): The frame of animation
        sequence_clock (int): It will tell the program if to step the sequence_number
        sequence_clock_original (int): It will reset the sequence_clock to this value
        moving_right (bool): When False it will point right and when true it will point left
        
    Returns:
        tuple(pygame.Surface, int, float, float, int): The object of the image, the next frame of animation, the width, height, and
        the updated sequence_clock
    '''
    Folder_Path: str = os.path.join('Assets', Name, 'PNG', f'{All_Characters_Images[Name][image_number]}', 'PNG Sequences', f'{sequence}')
    Total_Images = len(os.listdir(Folder_Path))

    if sequence_number >= Total_Images:
        sequence_number = 0
    
    Path: str =  f'{All_Characters_Images[Name][image_number]}_{sequence}_{sequence_number:03}.png'
    Image_Path = os.path.join(Folder_Path, Path)

    

    if sequence_clock == 0:
        next_number_in_sequence = sequence_number + 1
        sequence_clock_return = sequence_clock_original
    else:
        next_number_in_sequence = sequence_number
        sequence_clock_return = sequence_clock

    if next_number_in_sequence == Total_Images:
        next_number_in_sequence = 0
    

    Image: pygame.Surface = pygame.image.load(Image_Path)
    New_Width = Image.get_width() * scale
    New_Height = Image.get_height() * scale
    Image = pygame.transform.flip(pygame.transform.scale(Image, (New_Width, New_Height)), moving_right, False)

    return (Image, next_number_in_sequence, New_Width, New_Height, sequence_clock_return)

def Floor_Images(unit_size: tuple[int, int]) -> pygame.Surface:

    Folder_Path = os.path.join('Assets', 'Surrounding', 'Floor Tiles')
    All_Images = os.listdir(Folder_Path)
    File = random.choice(All_Images)
    Image_Path = os.path.join(Folder_Path, File)

    Image: pygame.Surface = pygame.image.load(Image_Path)
    Image = pygame.transform.scale(Image, unit_size)

    return Image

def Main_Font(size: int) -> pygame.font.Font:

    Font_Path = os.path.join('Assets', 'Fonts', 'TinyFontCraftpixPixel.otf')

    return pygame.font.Font(Font_Path, int(size))

if __name__ == '__main__':
    pass