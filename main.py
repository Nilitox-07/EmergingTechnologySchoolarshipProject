
#Annotation Helpers

from __future__ import annotations

#Graphics Engine

import pygame
from pygame.key import ScancodeWrapper

#Physics Engine

import pymunk

#Extra needed Modules

import copy
import json
import math
import os
import platform
import sys

from typing import Any

#My modules

import Assets
from LevelCreationAlgorithm import LevelCreation

class Start_Screen:
    def __init__(self, Core: Core):
        self.Core = Core
        self.Timer = 60
        self.Original_Timer = self.Timer

    def Display(self) -> None:

        if self.Core.Update:

            Game_Title_Font_Size: int = int(150 * self.Core.Scale_Factor)
            Instructions_Font_Size: int = int(60 * self.Core.Scale_Factor)

            self.Screen_Block: pygame.Surface = pygame.Surface(self.Core.Screen.get_size(), pygame.SRCALPHA)

            self.Game_Name_Text = Assets.Main_Font(Game_Title_Font_Size).render(self.Core.Game_Name, False, self.Core.Colors['pure_white'])
            self.Start_With_Any_Button_Text: pygame.Surface = Assets.Main_Font(Instructions_Font_Size).render('Click anywhere to continue', False, self.Core.Colors['pure_white'])

        self.Core.Screen.blit(self.Game_Name_Text, self.Game_Name_Text.get_rect(center=(self.Core.Get_Screen_Center()[0], self.Core.Get_Screen_Center()[1] - int(250 * self.Core.Height_Ratio))))
        self.Core.Screen.blit(self.Start_With_Any_Button_Text, self.Start_With_Any_Button_Text.get_rect(center=(self.Core.Get_Screen_Center()[0], self.Core.Get_Screen_Center()[1] + int(500 * self.Core.Height_Ratio))))

        if self.Timer > 0:
                
                self.Timer -= 1
                self.Oppacity = int(255 * (self.Timer / self.Original_Timer))
                self.Screen_Block.fill((0, 0, 0, self.Oppacity))
                self.Core.Screen.blit(self.Screen_Block, (0, 0))

    def Update_Display(self) -> None:

        pass

    def Run(self) -> bool:

        while True:
                self.Core.Delta_Time()
                self.Core.Get_Events()

                self.Display()

                if self.Core.Exit_Loop():
                    return False 
                
                for event in self.Core.Events:
                    if event.type == pygame.MOUSEBUTTONDOWN and self.Timer <= 0:
                        if event.button == 1:
                            return True
                    
                self.Core.Frame_Manager()

    def Clear_Memory(self):
        Core: Core = self.Core
        self.__dict__.clear()
        self.__init__(Core)

class Choose_Your_Save_File_Screen_Manager:
    def __init__(self, Core: Core):
        self.Core = Core
        self.Timer: int = 0
        self.Typing: bool = False
        self.Typing_Update: bool = True
        self.Typing_Text_Update: bool = False
        self.Character_Style_Choosen: int = 0
        self.Username_Text_Input: str = ""

    def Display(self) -> None:
        
        if self.Core.Update:

            #Main Assets
            
            self.Choose_Your_File_Txt: pygame.Surface = Assets.Main_Font(int(90 * self.Core.Scale_Factor)).render('Choose your save file', False, self.Core.Colors['pure_white'])
            
            #Right below here will go Buttons Assets
            
            Center_Button_Position: tuple[int, int] = (self.Core.Get_Screen_Center()[0], self.Core.Get_Screen_Center()[1] + int(50 * self.Core.Height_Ratio))
            self.Buttons_Size: tuple[int, int] = (int(550 * self.Core.Width_Ratio), int(800 * self.Core.Height_Ratio))
            
            Button_Color: tuple[int, int, int, int] = self.Core.Colors['choosing_character_color']
            Border_Button_Color: tuple[int, int, int, int] = self.Core.Colors['pure_white']
            Border_Thickness: int = int(10 * self.Core.Scale_Factor)
            Border_Radius: int = int(10 * self.Core.Scale_Factor)
            
            
            Create_Save_File_Font_Size: int = int(80 * self.Core.Scale_Factor)

            Text_1: pygame.Surface = Assets.Main_Font(Create_Save_File_Font_Size).render("Create", False, self.Core.Colors['pure_white'])
            Text_2: pygame.Surface = Assets.Main_Font(Create_Save_File_Font_Size).render("Save", False, self.Core.Colors['pure_white'])
            Text_3: pygame.Surface = Assets.Main_Font(Create_Save_File_Font_Size).render("File", False, self.Core.Colors['pure_white'])

            Create_Save_File: list[pygame.Surface] = [Text_1, Text_2, Text_3]

            self.All_Buttons: list[pygame.Rect] = []
            self.All_Surfaces: list[pygame.Surface] = []

            for x in range(3):
                Button = pygame.Rect((0, 0), self.Buttons_Size)
                Surface = pygame.Surface(self.Buttons_Size, pygame.SRCALPHA)
                pygame.draw.rect(Surface, Button_Color, Button, border_radius=Border_Radius)
                pygame.draw.rect(Surface, Border_Button_Color, Button, Border_Thickness, border_radius=Border_Radius)
                Button.center = (Center_Button_Position[0] - int(600 * self.Core.Width_Ratio) + int(600 * self.Core.Width_Ratio) * x, Center_Button_Position[1])
                self.All_Buttons.append(Button)
                self.All_Surfaces.append(Surface)
            
            Test_Button_Size: tuple[int, int] = (int(250 * self.Core.Width_Ratio), int(75 * self.Core.Height_Ratio))
            Test_Border_Thickness: int = 5

            Test_File_Font_Size: int = int(40 * self.Core.Scale_Factor)

            Test_Text: pygame.Surface = Assets.Main_Font(Test_File_Font_Size).render("Test", False, self.Core.Colors['pure_white'])
            File_Text: pygame.Surface = Assets.Main_Font(Test_File_Font_Size).render("File", False, self.Core.Colors['pure_white'])
            
            Button = pygame.Rect((0, 0), Test_Button_Size)
            Surface = pygame.Surface(Test_Button_Size, pygame.SRCALPHA)
            pygame.draw.rect(Surface, Button_Color, Button, border_radius=Border_Radius)
            pygame.draw.rect(Surface, Border_Button_Color, Button, Test_Border_Thickness, border_radius=Border_Radius)
            Button.center = (int(1700 * self.Core.Width_Ratio), int(100 * self.Core.Height_Ratio))

            Surface.blit(Test_Text, Test_Text.get_rect(center=(self.Core.Get_Surface_Center(Surface)[0] - int(52 * self.Core.Width_Ratio), self.Core.Get_Surface_Center(Surface)[1])))
            Surface.blit(File_Text, File_Text.get_rect(center=(self.Core.Get_Surface_Center(Surface)[0] + int(52 * self.Core.Width_Ratio), self.Core.Get_Surface_Center(Surface)[1])))

            self.All_Buttons.append(Button)
            self.All_Surfaces.append(Surface)

            self.Loaded_Data = self.Retrieve_Character_Data()

            for Number, Character in enumerate(self.Loaded_Data):
                if Character["Save File Started"]:
                    Character_Name = Assets.Main_Font(int(60 * self.Core.Scale_Factor)).render(Character['Preferences']['Name'], False, self.Core.Colors['pure_white'])
                    Character_Image = Assets.Characters_Image("Wraith", Character['Preferences']['Character_Style'], 1)
                    Center_Width = self.Core.Get_Surface_Center(self.All_Surfaces[Number])[0]
                    self.All_Surfaces[Number].blit(Character_Name, Character_Name.get_rect(center=(Center_Width, (int(75 * self.Core.Height_Ratio)))))
                    self.All_Surfaces[Number].blit(Character_Image[0], Character_Image[0].get_rect(center=(Center_Width, int(300 * self.Core.Height_Ratio))))
                    Skill_Render = Assets.Main_Font(int(35 * self.Core.Scale_Factor))
                    Unit_Height = int(50 * self.Core.Width_Ratio)
                    for x, (Skill, Value) in enumerate(Character['Skills'].items()):
                        Skill_Name = Skill_Render.render(Skill, False, self.Core.Colors['pure_white'])
                        if Value == 10:
                            Value = "Max"
                        Skill_Number = Skill_Render.render(str(Value), False, self.Core.Colors['pure_white'])
                        self.All_Surfaces[Number].blit(Skill_Name, Skill_Name.get_rect(midleft=(int(25 * self.Core.Width_Ratio), int(475 * self.Core.Height_Ratio) + Unit_Height * x)))
                        self.All_Surfaces[Number].blit(Skill_Number, Skill_Number.get_rect(midright=(self.All_Surfaces[Number].get_width() - int(25 * self.Core.Width_Ratio), int(475 * self.Core.Height_Ratio) + Unit_Height * x)))
                else:
                    for x, Text in enumerate(Create_Save_File):
                        Height_CSF: int = 280 + (100 * x)
                        self.All_Surfaces[Number].blit(Text, Text.get_rect(center=(self.Core.Get_Surface_Center(self.All_Surfaces[Number])[0], int(Height_CSF * self.Core.Height_Ratio))))

            self.Core.Screen.blit(self.Choose_Your_File_Txt, self.Choose_Your_File_Txt.get_rect(center=(self.Core.Get_Screen_Center()[0], self.Core.Get_Screen_Center()[1] - int(450 * self.Core.Height_Ratio))))

            self.Core.Update = False

        for x in range(4):
            self.Core.Screen.blit(self.All_Surfaces[x], self.All_Surfaces[x].get_rect(center=self.All_Buttons[x].center))

    def Typing_Display(self) -> None:
        '''
        Will handle Typing in the Username
        '''
        if self.Typing_Update:
            
            self.Dim_Surface: pygame.Surface = pygame.Surface((self.Core.Screen.get_size()), pygame.SRCALPHA)
            self.Dim_Surface.fill((0, 0, 0) + (175,))
            
            Typing_Button_Size: tuple[int, int] = (int(665 * self.Core.Width_Ratio), int(100 * self.Core.Height_Ratio))
            self.Typing_Surface_Color: tuple[int, int, int, int] = (180, 180, 180, 240)
            self.Typing_Border_Color: tuple[int, int, int, int] = self.Core.Colors['pure_white']
            self.Typing_Surface_Thickness: int = int(5 * self.Core.Scale_Factor)
            Typing_Surface_Position: tuple[int, int] = (self.Core.Get_Screen_Center()[0], int(200 * self.Core.Height_Ratio))
            
            #Typing Button
            
            self.Typing_Button: pygame.Rect = pygame.Rect((0, 0), Typing_Button_Size)
            self.Typing_Surface: pygame.Surface = pygame.Surface(Typing_Button_Size, pygame.SRCALPHA)
            self.Typing_Surface.fill(self.Core.Colors['fully_transparent'])
            pygame.draw.rect(self.Typing_Surface, self.Typing_Surface_Color, self.Typing_Button, border_radius=5)
            pygame.draw.rect(self.Typing_Surface, self.Typing_Border_Color, self.Typing_Button, self.Typing_Surface_Thickness, 5)
            self.Typing_Button.center = Typing_Surface_Position
            
            #Cancel Button
            
            Cancel_Button_Size: tuple[int, int] = (int(200 * self.Core.Width_Ratio), int(75 * self.Core.Height_Ratio))
            Cancel_Button_Position: tuple[int, int] = (int(110 * self.Core.Width_Ratio), int(1030 * self.Core.Height_Ratio))
            Cancel_Button_Color: tuple[int, int, int, int] = (255, 255, 255) + (200,)
            Cancel_Border_Color: tuple[int, int, int, int] = (255, 255, 255) + (255,)
            Cancel_Border_Thickness: int = int(3 * self.Core.Scale_Factor)
            Cancel_Border_Radius: int = int(5 * self.Core.Scale_Factor)
            
            self.Cancel_Button: pygame.Rect = pygame.Rect((0, 0), Cancel_Button_Size)
            self.Cancel_Surface: pygame.Surface = pygame.Surface((Cancel_Button_Size), pygame.SRCALPHA)
            self.Cancel_Surface.fill(self.Core.Colors['fully_transparent'])
            pygame.draw.rect(self.Cancel_Surface, Cancel_Button_Color, self.Cancel_Button, border_radius=Cancel_Border_Radius)
            pygame.draw.rect(self.Cancel_Surface, Cancel_Border_Color, self.Cancel_Button, Cancel_Border_Thickness, Cancel_Border_Radius)
            self.Cancel_Button.center = Cancel_Button_Position
            
            Cancel_Text: pygame.Surface = Assets.Main_Font(int(45 * self.Core.Scale_Factor)).render("Cancel", False, self.Core.Colors['pure_white'])
            self.Cancel_Surface.blit(Cancel_Text, Cancel_Text.get_rect(center=(self.Core.Get_Surface_Center(self.Cancel_Surface))))
            
            self.Message_For_Username_Text_1: pygame.Surface = Assets.Main_Font(int(55 * self.Core.Scale_Factor)).render("Username can not be longer than 15 Characters", False, self.Core.Colors['pure_white'])
            self.Message_For_Username_Text_2: pygame.Surface = Assets.Main_Font(int(55 * self.Core.Scale_Factor)).render('Any spaces will be replaced by "_"', False, self.Core.Colors['pure_white'])

            self.Character_Style_Buttons: list[pygame.Rect] = []
            self.Character_Style_Surface: list[pygame.Surface] = []

            width: int = self.Core.Get_Screen_Center()[0] - int(400 * self.Core.Width_Ratio)
            height: int = self.Core.Get_Screen_Center()[1] + int(200 * self.Core.Height_Ratio)

            for x in range(3):
                Character = Assets.Characters_Image("Wraith", x, 1)
                Surface = pygame.Surface((Character[0].get_width() - int(200 * self.Core.Width_Ratio), Character[0].get_height() - int(10 * self.Core.Height_Ratio)), pygame.SRCALPHA)
                Surface.fill(self.Core.Colors['fully_transparent'])
                Surface.blit(Character[0], Character[0].get_rect(center=self.Core.Get_Surface_Center(Surface)))
                Button = Surface.get_rect(center=(width + int(400 * self.Core.Width_Ratio * x), height))
                self.Character_Style_Surface.append(Surface)
                self.Character_Style_Buttons.append(Button)
            
            self.Typing_Update = False
        
        if self.Typing_Text_Update:
            
            Username_Text: pygame.Surface = Assets.Main_Font(int(50 * self.Core.Scale_Factor)).render(self.Username_Text_Input, False, self.Core.Colors['pure_white'])
            pygame.draw.rect(self.Typing_Surface, self.Typing_Surface_Color, ((0, 0), self.Typing_Button.size), border_radius=5)
            pygame.draw.rect(self.Typing_Surface, self.Typing_Border_Color, ((0, 0), self.Typing_Button.size), self.Typing_Surface_Thickness, 5)
            self.Typing_Surface.blit(Username_Text, Username_Text.get_rect(center=(self.Core.Get_Surface_Center(self.Typing_Surface))))
            
        self.Core.Screen.blit(self.Dim_Surface, (0, 0))
        self.Core.Screen.blit(self.Typing_Surface, self.Typing_Surface.get_rect(center=(self.Typing_Button.center)))
        self.Core.Screen.blit(self.Cancel_Surface, self.Cancel_Surface.get_rect(center=(self.Cancel_Button.center)))
        self.Core.Screen.blit(self.Message_For_Username_Text_1, self.Message_For_Username_Text_1.get_rect(center=(self.Typing_Button.center[0], self.Typing_Button.center[1] + int(110 * self.Core.Height_Ratio))))
        self.Core.Screen.blit(self.Message_For_Username_Text_2, self.Message_For_Username_Text_2.get_rect(center=(self.Typing_Button.center[0], self.Typing_Button.center[1] + int(210 * self.Core.Height_Ratio))))
        for x in range(3):
            self.Core.Screen.blit(self.Character_Style_Surface[x], self.Character_Style_Surface[x].get_rect(center=(self.Character_Style_Buttons[x].center)))
            if self.Character_Style_Choosen == x:
                pygame.draw.rect(self.Core.Screen, self.Core.Colors['pure_white'], self.Character_Style_Buttons[x], int(5 * self.Core.Width_Ratio), border_radius=int(25 * self.Core.Width_Ratio))

    def Run(self) -> bool:
        
        self.Typing_Display()

        self.Core.Update = True

        self.Max_Username_Length: int = 15

        while True:
                
                self.Core.Delta_Time()
                self.Core.Get_Events()
                self.Core.Get_Keys()
                
                if self.Core.Update:
                    self.Core.Screen.fill(self.Core.Colors["pure_black"])

                self.Display()

                if self.Typing:
                    self.Typing_Display()

                if self.Core.Exit_Loop():
                    return False 
                
                if self.Timer <= 0 and self.Core.Keys[pygame.K_BACKSPACE]:
                    self.Username_Text_Input = self.Username_Text_Input[:-1]
                    self.Typing_Text_Update = True
                    self.Timer = 1
                elif self.Timer > 0:
                    self.Timer -= 1

                for event in self.Core.Events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if self.Typing:
                                if self.Typing_Button.collidepoint(event.pos):
                                    self.Core.Typing(self.Typing_Button)
                                elif self.Cancel_Button.collidepoint(event.pos):
                                    self.Username_Text_Input = ""
                                    self.Typing = False
                                    self.Core.Update = True
                                    self.Core.Stop_Typing()
                                else:
                                    self.Core.Stop_Typing()
                                    for x, Button in enumerate(self.Character_Style_Buttons):
                                        if Button.collidepoint(event.pos):
                                            self.Typing_Update = True
                                            self.Character_Style_Choosen = x
                            for x, Button in enumerate(self.All_Buttons):
                                if x > 2:
                                    continue
                                if Button.collidepoint(event.pos) and not self.Typing:
                                    self.Core.Loaded_File = x
                                    if self.Loaded_Data[x]["Save File Started"]:
                                        self.Clear_Memory()
                                        return True
                                    else:
                                        self.Typing = True
                                        self.Core.Typing(self.Typing_Button)
                            if self.All_Buttons[3].collidepoint(event.pos) and not self.Typing:
                                self.Core.Loaded_File = 3
                                self.Clear_Memory()
                                return True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.Timer = 15
                        if event.key == pygame.K_RETURN:
                            if self.Typing:
                                self.Username_Text_Input = self.Username_Check(self.Username_Text_Input)
                                self.Core.Create_File(self.Username_Text_Input, self.Core.Loaded_File, self.Character_Style_Choosen)
                                self.Username_Text_Input = ""
                                self.Typing = False
                                self.Clear_Memory()
                                return True
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_BACKSPACE:
                            self.Timer = 0
                    if event.type == pygame.TEXTINPUT and self.Typing:
                        if len(self.Username_Text_Input) < self.Max_Username_Length:
                            self.Username_Text_Input += event.text
                            self.Typing_Text_Update = True
                    
                self.Core.Frame_Manager()

    def Retrieve_Character_Data(self) -> list:

        Loaded_Data = []

        Folder_Path = 'CharacterSaves'

        for x in range(1, 4):

            json_path = os.path.join(Folder_Path, f'Character{x}', 'CharacterSave.json')

            with open(json_path, 'r') as File:
                Data = json.load(File)

            Loaded_Data.append(Data)

        return Loaded_Data
    
    def Username_Check(self, Username: str) -> str:
        '''
        Will update the username given to fill any spaces with "_"
        
        Parameters:
            Username (str): Un-updated username
            
        Returns:
            (str): Updated Username
        '''
        newUsername: str = ""
        for letter in Username:
            if letter == " ":
                newUsername += "_"
            else:
                newUsername += letter
        return newUsername
    
    def Clear_Memory(self):
        Core: Core = self.Core
        self.__dict__.clear()
        self.__init__(Core)

class Main_Menu_Screen_Manager:
    def __init__(self, Core: Core) -> None:
        self.Core = Core
        self.Initialize_Buttons: bool = True
        self.Update_All_Buttons: bool = True
        self.Update_Position: bool = True
        self.Update_Buttons: list[bool] = [True] * 3
        self.Exit: int = 0
        self.Play: int = 1
        self.Settings: int = 2
        self.Info: int = 3
        self.Animation_Speed: int = 120
        
    def Display(self) -> None:
        
        if self.Core.Update:
            
            '''
            Display for Main Menu
            '''
            
            #Main Assets
            
            self.Game_Title_Text: pygame.Surface = Assets.Main_Font(int(150 * self.Core.Scale_Factor)).render(self.Core.Game_Name, False, self.Core.Colors['pure_white'])
            self.Game_Title_Position: tuple[int, int] = (self.Play_Button.center[0], int(150 * self.Core.Height_Ratio))
            
            self.Core.Update = False
            
        self.Core.Screen.fill(self.Core.Colors['pure_black'])
        self.Core.Screen.blit(self.Game_Title_Text, self.Game_Title_Text.get_rect(center=(self.Game_Title_Position)))
        self.Core.Screen.blit(self.Play_Surface, self.Play_Surface.get_rect(center=(self.Play_Button.center)))
        self.Core.Screen.blit(self.Settings_Surface, self.Settings_Surface.get_rect(center=(self.Settings_Button.center)))
        self.Core.Screen.blit(self.Quit_Surface, self.Quit_Surface.get_rect(center=(self.Quit_Button.center)))
        
            
    def Run(self) -> int:
        '''
        This will control all that happend in the Main Menu, without including Settings Tab, Play/Levels, and Credits
        '''
        
        self.Loaded_File = self.Core.Get_Data(os.path.join('CharacterSaves', f'Character{self.Core.Loaded_File + 1}', 'CharacterSave.json'))

        self.Core.Update = True
        
        while True:
        
            self.Core.Get_Events()
            self.Core.Get_Mouse_Position()
            
            self.Update_Button_Fonts()
            self.Display()
            
            if self.Core.Exit_Loop():
                return self.Exit
            
            for event in self.Core.Events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.Quit_Button.collidepoint(event.pos):
                            self.Clear_Memory()
                            self.Core.Variable_Changer()
                            return self.Exit
                        elif self.Play_Button.collidepoint(event.pos):
                            self.Clear_Memory()
                            return self.Play
                        elif self.Settings_Button.collidepoint(event.pos):
                            self.Clear_Memory()
                            return self.Settings
                    
            temp_Button_List: list[pygame.Rect] = [self.Play_Button, self.Settings_Button, self.Quit_Button]
            temp_Index_List: list[int] = [self.Play_Font_Index, self.Settings_Font_Index, self.Quit_Font_Index]
            
            for button, index in zip(temp_Button_List, temp_Index_List):
                
                if button.collidepoint(self.Core.Mouse_Position):
                    self.Update_Buttons[index] = self.Increase_Font_Size(index)
                    if not self.Update_All_Buttons:
                        self.Update_All_Buttons = self.Update_Buttons[index]
                else:
                    self.Update_Buttons[index] = self.Decrease_Font_Size(index)
                    if not self.Update_All_Buttons:
                        self.Update_All_Buttons = self.Update_Buttons[index]
            
            self.Core.Frame_Manager()
    
    def Decrease_Font_Size(self, Font_Index: int) -> bool:
        '''
        Increases the corresponding font for the buttons
        
        Parameters:
            Font_Index (int): Decreases by Animation_Speed the corresponding font
            
        Returns:
            bool: If it doesnt change it returns False, else True
        '''
        
        if self.Main_Buttons_Font_Size[Font_Index] > 0:
            self.Main_Buttons_Font_Size[Font_Index] -= int(self.Animation_Speed * self.Core.DeltaTime)
            return True
        return False
    
    def Increase_Font_Size(self, Font_Index: int) -> bool:
        '''
        Increases the corresponding font for the buttons
        
        Parameters:
            Font_Index (int): Increases by 1 the corresponding font
            
        Returns:
            bool: If it doesnt change it returns False, else True
        '''
        
        if self.Main_Buttons_Font_Size[Font_Index] < self.Initial_Difference:
            self.Main_Buttons_Font_Size[Font_Index] += int(self.Animation_Speed * self.Core.DeltaTime)
            return True
        return False
    
    def Update_All(self) -> None:
        '''
        Sets all updates to true
        '''
        self.Initialize_Buttons = True
        self.Update_All_Buttons = True
        self.Update_Position = True
        self.Update_Buttons = [True] * 3
        
    
    def Update_Button_Fonts(self) -> None:
        '''
        Initializes the Button variable and updates the needed Variable
        '''
        
        if self.Initialize_Buttons:
            
            #Font Variables
            
            self.Main_Buttons_Font_Size: list[int] = [0] * 3
            
            self.Play_Font_Index: int = 0
            self.Settings_Font_Index: int = 1
            self.Quit_Font_Index: int = 2
            
            self.Initial_Difference: int = 30 # Non_Selected Font minus Selected Font
            
            self.Initialize_Buttons = False
            
        if self.Update_All_Buttons:
            
            #Buttons
            
            #Assets for Buttons
            
            self.Non_Selected_Buttons_Text_Font_Size: int = int(100 * self.Core.Scale_Factor)
            self.Selected_Button_Text_Font_Size: int = int(130 * self.Core.Scale_Factor)
            
            self.Play_Font: int = self.Non_Selected_Buttons_Text_Font_Size + int(self.Main_Buttons_Font_Size[self.Play_Font_Index] * self.Core.Scale_Factor)
            self.Settings_Font: int = self.Non_Selected_Buttons_Text_Font_Size + int(self.Main_Buttons_Font_Size[self.Settings_Font_Index] * self.Core.Scale_Factor)
            self.Quit_Font: int = self.Non_Selected_Buttons_Text_Font_Size + int(self.Main_Buttons_Font_Size[self.Quit_Font_Index] * self.Core.Scale_Factor)
            
            self.Buttons_Color: tuple[int, int, int, int] = self.Core.Colors['fully_transparent']
            
            Button_Margin_Width: int = int(10 * self.Core.Width_Ratio)
            Button_Margin_Height: int = int(-5 * self.Core.Height_Ratio)
            
            #Play Button
            
            if self.Update_Buttons[self.Play_Font_Index]:

                Text: str = "Play"
                if self.Loaded_File['Started Dungeon']:
                    Text = "Continue"
            
                Play_Text: pygame.Surface = Assets.Main_Font(self.Play_Font).render(Text, False, self.Core.Colors['pure_white'])
                self.Play_Surface: pygame.Surface = pygame.Surface((Play_Text.get_width() + Button_Margin_Width, Play_Text.get_height() + Button_Margin_Height), pygame.SRCALPHA)
                self.Play_Button: pygame.Rect = self.Play_Surface.get_rect()
                
                self.Play_Surface.fill(self.Buttons_Color)
                self.Play_Surface.blit(Play_Text, Play_Text.get_rect(center=(self.Core.Get_Surface_Center(self.Play_Surface))))
            
                if not self.Update_Position:
                    
                    self.Update_Position = True
                    
                self.Update_Buttons[self.Play_Font_Index] = False
            
            #Settings Button
            
            if self.Update_Buttons[self.Settings_Font_Index]:
            
                Settings_Text: pygame.Surface = Assets.Main_Font(self.Settings_Font).render("Settings", False, self.Core.Colors['pure_white'])
                self.Settings_Surface: pygame.Surface = pygame.Surface((Settings_Text.get_width() + Button_Margin_Width, Settings_Text.get_height() + Button_Margin_Height), pygame.SRCALPHA)
                self.Settings_Button: pygame.Rect = self.Settings_Surface.get_rect()
                
                self.Settings_Surface.fill(self.Buttons_Color)
                self.Settings_Surface.blit(Settings_Text, Settings_Text.get_rect(center=(self.Core.Get_Surface_Center(self.Settings_Surface))))
            
                if not self.Update_Position:
                    
                    self.Update_Position = True
                    
                self.Update_Buttons[self.Settings_Font_Index] = False
                
            #Quit Button
            
            if self.Update_Buttons[self.Quit_Font_Index]:
            
                Quit_Text: pygame.Surface = Assets.Main_Font(self.Quit_Font).render("Quit", False, self.Core.Colors['pure_white'])
                self.Quit_Surface: pygame.Surface = pygame.Surface((Quit_Text.get_width() + Button_Margin_Width, Quit_Text.get_height() + Button_Margin_Height), pygame.SRCALPHA)
                self.Quit_Button: pygame.Rect = self.Quit_Surface.get_rect()
                
                self.Quit_Surface.fill(self.Buttons_Color)
                self.Quit_Surface.blit(Quit_Text, Quit_Text.get_rect(center=(self.Core.Get_Surface_Center(self.Quit_Surface))))
                
                if not self.Update_Position:
                    
                    self.Update_Position = True
                    
                self.Update_Buttons[self.Quit_Font_Index] = False
                
            self.Update_All_Buttons = False
        
        if self.Update_Position:
            
            Unit_Height = int(40 * self.Core.Height_Ratio)
            
            Buttons_Text_Start_Position: tuple[int, int] = (self.Core.Get_Screen_Center()[0], int(350 * self.Core.Height_Ratio))
            
            self.Play_Button.midtop = Buttons_Text_Start_Position
            self.Settings_Button.midtop = (self.Play_Button.midbottom[0],  self.Play_Button.midbottom[1] + Unit_Height)
            self.Quit_Button.midtop = (self.Settings_Button.midbottom[0], self.Settings_Button.midbottom[1] + Unit_Height)

    def Clear_Memory(self):
        Core: Core = self.Core
        self.__dict__.clear()
        self.__init__(Core)

class Settings_Screen_Manager:
    def __init__(self, Core: Core):
        self.Core = Core

    def Display(self) -> None:

        if self.Core.Update:

            Settings_Text = Assets.Main_Font(int(40 * self.Core.Scale_Factor)).render("Settings", False, self.Core.Colors['pure_white'])

            # Return Button

            Back_Text = Assets.Main_Font(int(25 * self.Core.Scale_Factor)).render("Back", False, self.Core.Colors['pure_white'])
            self.Back_Surface = pygame.Surface((Back_Text.get_width() + int(20 * self.Core.Width_Ratio), Back_Text.get_height() + int(10 * self.Core.Height_Ratio)), pygame.SRCALPHA)
            self.Back_Button = self.Back_Surface.get_rect(bottomleft = (int(25 * self.Core.Width_Ratio), self.Core.Screen.get_height() - int(25 * self.Core.Height_Ratio)))

        

class Player(pygame.sprite.Sprite):
    def __init__(self, Game: Game, position: tuple[int, int], difficulty: int = 0, fight_zones_opened: int = 0, stores_opened: int = 0, levels_started: bool = False) -> None:
        
        pygame.sprite.Sprite.__init__(self)
        
        #Important Variables
    
        self.Game: Game = Game
        self.position: pygame.Vector2 = pygame.Vector2(position)
        self.dungeon_position: tuple[int, int] = (0, 0)
        self.difficulty = difficulty
        self.fight_zones_opened = fight_zones_opened
        self.stores_opened = stores_opened
        self.levels_started = levels_started
        self.state = Assets.Idle

        #Initiating Image

        self.scale = 0.35
        self.moving_right = False
        self.image_sequence = 0
        self.image_sequence_clock = 3
        self.image_sequence_clock_original = self.image_sequence_clock
        self.character_image = 'Wraith'
        self.character_style = 0
        self.image, self.image_sequence, self.Width_Size, self.Height_Size, self.image_sequence_clock = Assets.Characters_Image(self.character_image, self.character_style, self.scale, self.state, self.image_sequence, self.image_sequence_clock, self.image_sequence_clock_original, self.moving_right)

        self.rect = self.image.get_rect(center=self.position)
        self.rect.center = self.position
        
        self.Sprite = pygame.sprite.Group(self)
        
        #Initiating Hitbox

        self.Body: pymunk.Body = pymunk.Body(pymunk.Body.KINEMATIC)
        self.Pymunk_Position()
        self.Object: pymunk.Circle = pymunk.Circle(self.Body, self.Width_Size // 2, (0, 17.5))
        self.Object.mass = 1
        self.Object.elasticity = 0
        self.Game.Core.Space.add(self.Body, self.Object)
        
        #Movement
        
        self.Moving: bool = True
        self.Movement_Speed: float
        self.SPEED: int = 20000
        self.DIAGONAL_CONSTANT: float = 2 ** 0.5
    
    def Draw(self, Screen: pygame.Surface) -> None:
        '''
        Draws the image to the position
        
        Parameters:
            Screen (pygame.Surface): Where the image will be drawn to
        
        '''
        
        Screen.blit(self.image, self.image.get_rect(center=(self.Game.Core.Screen.get_width() / 2, self.Game.Core.Screen.get_height() / 2)))
    
    def Movement(self) -> bool:
        '''
        Returns:
            (True): When player is moving
            (False): Otherwise
        '''
        if self.Moving:
            
            vx: float = 0
            vy: float = 0
            xPressed: bool = False
            yPressed: bool = False
            
            shiftPressed: float = 1
            if self.Game.Core.Keys[pygame.K_LSHIFT]:
                shiftPressed = 1.25
        
            self.Movement_Speed = self.SPEED * shiftPressed
            
            if self.Game.Core.Keys[pygame.K_a]:
                vx = -self.Game.Core.DeltaTime
                xPressed = True
                self.moving_right = True
                
            if self.Game.Core.Keys[pygame.K_d]:
                if not xPressed:
                    vx = self.Game.Core.DeltaTime
                    xPressed = True
                    self.moving_right = False
                else:
                    vx = 0
                    xPressed = False
            
            if self.Game.Core.Keys[pygame.K_w]:
                vy = -self.Game.Core.DeltaTime
                yPressed = True
                
            if self.Game.Core.Keys[pygame.K_s]:
                if not yPressed:
                    vy = self.Game.Core.DeltaTime
                    yPressed = True
                else:
                    vy = 0
                    yPressed = False
                    
            if xPressed and yPressed:
                self.Movement_Speed = self.Movement_Speed / self.DIAGONAL_CONSTANT
                
                
            self.Body.velocity = (self.Movement_Speed * vx, self.Movement_Speed * vy) #NEED TO FIX THIS DELTA TIME DOESNT WORK PROPERLY
            if vx or vy:
                self.state = Assets.Walking
                return True
            else:
                return False
                
    def Pygame_Position(self) -> None:
        '''
        Sets the position depending on its bodies position into a pygame.Vector2 
        '''
        self.position = pygame.Vector2(self.Body.position.x, self.Body.position.y)
        self.rect.center = self.position
        
    def Pymunk_Position(self) -> None:
        '''
        Sets the position to its body to place in pymunks engine
        '''
        self.Body.position = (self.position.x, self.position.y)
        
    def Update_Image(self) -> None:
        '''
        Updates the image corresponding to the new screens Ratio
        '''
        self.image_sequence_clock -= 1
        self.image, self.image_sequence, self.Width_Size, self.Height_Size, self.image_sequence_clock = Assets.Characters_Image(self.character_image, self.character_style, self.scale, self.state, self.image_sequence, self.image_sequence_clock, self.image_sequence_clock_original, self.moving_right)

class Game:
    def __init__(self, Core: Core) -> None:
        self.Core: Core = Core
        self.Player: Player = Player(self, (25, 25))
        self.Map: pygame.Surface = pygame.Surface((10000, 10000), pygame.SRCALPHA)
        self.Map.fill(self.Core.Colors['pure_green'])
        
    def Display(self) -> None:
    
        self.Core.Screen.fill(self.Core.Colors['pure_white'])
    
    def Update_Display(self) -> None:
        
        pass
        
    def Run(self) -> bool:
    
        self.Core.Update = True
        Save_pos: pygame.Vector2 = pygame.Vector2(0, 0)
        
        while True:
        
            self.Core.Delta_Time()
            self.Core.Get_Events()
            self.Core.Get_Keys()
            self.Core.Get_Mouse_Position()
            self.Core.Get_Mouse_Pressed()
            
            if self.Core.Update:
                self.Core.Get_Ratio()
                self.Update_Display()
                self.Core.Update = False
                
            self.Display()
            
            if self.Player.Movement():
                self.Player.Update_Image()
            else:
                self.Player.state = Assets.Idle
                self.Player.Update_Image()

            self.Player.Pygame_Position()
            self.Core.Screen.blit(self.Map, -self.Player.position)
            self.Player.Draw(self.Core.Screen)
            
            
            if self.Core.Exit_Loop():
                return False
                
            for event in self.Core.Events:
                break
                
            self.Core.Frame_Manager() 
    
    def GetTileSize(self) -> None:

        self.TileSize = (147 * self.Core.Width_Ratio, 147 * self.Core.Height_Ratio) # The width of our characters is 147

    def LoadGrid(self) -> None:
        pass

class Core:
    def __init__(self) -> None:
        
        #Initializing Important Variable
        
        self.Colors: dict[str, tuple[int, int, int, int]]
        self.DeltaTime: float
        self.Events: list[pygame.event.Event]
        self.Keys: ScancodeWrapper
        self.Mouse_Position: tuple[int, int]
        self.Mouse_Buttons: tuple[int, int, int]
        self.Loaded_File: int = -1 # Not Selected, It can be from 0 - 3, 3 being Tester File
        self.Game_Name: str = "Through the Dungeons"

        #Ratios

        self.Width_Ratio: float
        self.Height_Ratio: float
        self.Scale_Factor: float
        
        #Mouse Buttons
        
        self.LEFT_CLICK: int = 0
        self.MIDDLE_CLICK: int = 1
        self.RIGHT_CLICK: int = 2
        
        #Platform
        
        self.Platform: str = platform.system()
        
        #Control Variables
        
        self.Running: bool = True
        self.Update: bool = True
        
        #Screen
        
        Info = pygame.display.Info()
        
        # The orignal is the resolution of the developer's screen so the objects go in reference of his screen.

        self.Original_Screen_Width: int = 1920
        self.Original_Screen_Height: int = 1080

        Width = Info.current_w
        Height = Info.current_h

        self.Screen: pygame.Surface = pygame.display.set_mode((Width, Height), pygame.DOUBLEBUF | pygame.FULLSCREEN)
        
        #Screen Control
        
        self.FPS_Value: int = 60
        self.FPS_Ratio: float = 1 / self.FPS_Value
        self.Clock: pygame.time.Clock = pygame.time.Clock()
        
        #Space

        self.Space: pymunk.Space = pymunk.Space()

        #Calling Needed Functions
        
        self.Get_Ratio()
        self.Save_Colors()
        
        #Screens

        self.Start_Screen = Start_Screen(self)
        self.Choose_Your_Save_File_Screen = Choose_Your_Save_File_Screen_Manager(self)
        self.Main_Menu_Screen = Main_Menu_Screen_Manager(self)
        self.Game_Screen = Game(self)
    
    #Helper/Getter Functions Sorted ABC
    
    def Save_Colors(self) -> None:
        '''
        Save the colors in Memory
        
        Run Core.Print_Colors()
        
        To see available Colors
        '''
        
        self.Colors: dict[str, tuple[int, int, int, int]] = {"fully_transparent" : (0, 0, 0, 0),
                                                             "pure_red" : (255, 0, 0, 255),
                                                             "pure_green" : (0, 255, 0, 255),
                                                             "pure_blue" : (0, 0, 255, 255),
                                                             "pure_black" : (0, 0, 0, 255),
                                                             "pure_white" : (255, 255, 255, 255),
                                                             "choosing_character_color" : (121, 121, 121, 200)}
    
    def Create_File(self, Username: str, File: int, Character_Style: int) -> None:
        '''
        Creates a new file for the player
        
        Parameters:
            Username (str): The Username Choosen by the player
            File (int): The number of the character
        '''
        rawData: dict
        if len(Username) < 1:
            rawData = self.Get_Data(os.path.join('CharacterSaves', 'CharacterSave.json'))
            rawData['Save File Started'] = True
            rawData['Preferences']['Name'] = "Player"
            rawData['Preferences']['Character_Style'] = Character_Style
            self.Input_Data(rawData, os.path.join('CharacterSaves', f'Character{File + 1}', 'CharacterSave.json'))
        else:
            rawData = self.Get_Data(os.path.join('CharacterSaves', 'CharacterSave.json'))
            rawData['Save File Started'] = True
            rawData['Preferences']['Name'] = Username
            rawData['Preferences']['Character_Style'] = Character_Style
            self.Input_Data(rawData, os.path.join('CharacterSaves', f'Character{File + 1}', 'CharacterSave.json'))

    def Delta_Time(self) -> None:
        '''
        Saves the time from the start of the last frame to the start of the current frame in Miliseconds
        '''
        
        self.DeltaTime = self.Clock.get_time() / 1000
    
    def Get_Data(self, Path: str) -> dict:
        '''
        Will return the data from a Json File
        
        Parameters:
            Path (str): Desired path of the Json file to get
            
        Returns:
            The data in the Json File as a Python Dict
        
        '''
        with open(Path, 'r') as File:
            
            return json.load(File)

    def Get_Screen_Center(self) -> tuple[int, int]:
        '''
        Will return the coordinates for the center of the screen
        '''

        screen_width = self.Screen.get_width()
        screen_height = self.Screen.get_height()

        return (screen_width // 2, screen_height // 2)

    def Get_Surface_Center(self, Surface: pygame.Surface) -> tuple[int, int]:
        '''
        Will return the center of the Surface Given
        '''

        surface_width = Surface.get_width()
        surface_height = Surface.get_height()

        return (surface_width // 2, surface_height // 2)

    def Get_Events(self) -> None:
        '''
        Saves pygame Events in a Variable called Events
        '''
        self.Events: list[pygame.event.Event] = list(pygame.event.get())
    
    def Get_Keys(self) -> None:
        '''
        Saves Keys in a Variable called Keys
        '''
        
        self.Keys: ScancodeWrapper = pygame.key.get_pressed()
        
    def Get_Mouse_Position(self) -> None:
        '''
        Saves the mouse position in a variable called Mouse_Position
        '''
        
        self.Mouse_Position = pygame.mouse.get_pos()
        
    def Get_Mouse_Pressed(self) -> None:
        '''
        Saves the mouse buttons pressed in a variable called Mouse_Buttons
        
        Can call each button by indexing:
            
            Core.Mouse_Buttons[Core.LEFT_CLICK] for Left Click
            Core.Mouse_Buttons[Core.MIDDLE_CLICK] for Scroll Click
            Core.Mouse_Buttons[Core.RIGHT_CLICK] for Right Click
        '''
        
        self.Mouse_Buttons = pygame.mouse.get_pressed()
    
    def Get_Ratio(self) -> None:
        '''
        Saves the Ratio from the Current Width and Height over the Original Width and Height in the following Variables
        
            self.Width_Ratio (float): Current Width over Original Width 
            self.Height_Ratio (float): Current Height over Original Height
            self.Scale_Factor (float): The squared root of the Quotient of Product of Current Height and Width over
                                Original Height and Width
                                
        '''
        self.Width_Ratio = self.Screen.get_width() / self.Original_Screen_Width
        self.Height_Ratio = self.Screen.get_height() / self.Original_Screen_Height
        
        Current_Resolution_Product: int = self.Screen.get_width() * self.Screen.get_height()
        Original_Resolution_Product: int = self.Original_Screen_Width * self.Original_Screen_Height
        
        Scale_Factor_Proportion: float = Current_Resolution_Product / Original_Resolution_Product
        
        self.Scale_Factor = Scale_Factor_Proportion ** 0.5

    def Input_Data(self, Data: dict, Path: str) -> None:
        '''
        Will input the data given into the corresponding Json File
        
        Parameters:
            Data (dict): This will hold the data structured for Json File
            Path (str): This is place where the data will be alocated
        '''
        with open(Path, 'w') as File:
            
            json.dump(Data, File, indent=4)

    #Developer Functions
    
    def Loop_Holder(self) -> bool:
        '''
        This is mostly for test cases where I am not running a Screen Class
        so for the program to not quit it instantly and atleast be able to
        hold the pygame screen.
        
        This also sets how each Run function in the Screen classes will look
        
        '''
        
        while True:
            '''
            Not all run functions will need to have all of this Getter Functions
            Comands in between ---- Are not mandatory but most games/UI do use them ----
            Every run function must have:
                self.Delta_Time() at the top
                self.Get_Events() Following it
                
                --------
                Display Funtions here
                
                Any movement modules if any
                --------
                
                if Exit_Loop():
                    return False For the program to be able to close
                    
                --------
                Add the Loop iterator here for event handling
                
                And anything extra after
                --------
                    
                Frame_Manager() Screen Updates plus Frame Steper
            '''
            
            self.Delta_Time()
            self.Get_Events()
            self.Get_Keys()
            self.Get_Mouse_Position()
            self.Get_Mouse_Pressed()
            
            if self.Exit_Loop():
                return False
                
            self.Frame_Manager()
            
            return True # Testing Purposes
    
    def Print_Colors(self) -> None:
        '''
        Prints all Created Colors and their RGB Values
        
        >>> Name          |Value
            ---------------------------
            color_name    |(r, g, b, a)
        '''
        
        Name_And_Value_Prompt: str = "Name                   |Value"
        
        print(Name_And_Value_Prompt)
        print("---------------------------------------------")
        
        Separator: int = len(Name_And_Value_Prompt) - 6 #6 Being the length of Value + the '|' separator
        
        for color, value in self.Colors.items():
            newString: str = f'{color}'
            
            colorLength: int = len(color)
            
            for _ in range(Separator - colorLength):
                newString += ' '
            
            newString += f'|{value}'
            
            print(newString)
    
    def Stop_Typing(self) -> None:
        '''
        Stops the pygame text input
        '''
        pygame.key.stop_text_input()

    def Typing(self, Surface: pygame.Rect) -> None:
        '''
        Stars and sets the surface where the text input will go
        '''
        pygame.key.start_text_input()
        
        pygame.key.set_text_input_rect(Surface)

    #Game Controller
    
    def Variable_Changer(self) -> None:
        self.Running = False
        pygame.quit()
        sys.exit()

    def Exit_Loop(self) -> bool:
        '''
        It exits pygame and sys
        
        Returns:
            (True) if Quit is Press
            (False) otherwise
        '''
        
        for event in self.Events:
            if event.type == pygame.QUIT:
                self.Variable_Changer()
                return True
        return False
    
    def Frame_Manager(self) -> None:
        '''
        Updates the screen and steps the frame
        '''
        
        step: int = 10
        
        for _ in range(step):
            self.Space.step(self.DeltaTime / step)
        
        pygame.display.flip()
        
        self.Clock.tick(self.FPS_Value)
    
    #Brain
    
    def Start(self) -> None:
        '''
        Runs all the Screens
        '''
        
        while self.Running:
            if self.Loop_Holder():
                if self.Start_Screen.Run():
                    if self.Choose_Your_Save_File_Screen.Run():
                        Main_Menu_Controller = -1
                        while Main_Menu_Controller != self.Main_Menu_Screen.Exit:
                            Main_Menu_Controller = self.Main_Menu_Screen.Run()
                            if Main_Menu_Controller == self.Main_Menu_Screen.Exit:
                                break
                            elif Main_Menu_Controller == self.Main_Menu_Screen.Play:
                                if self.Game_Screen.Run(): 
                                    pass
                            elif Main_Menu_Controller == self.Main_Menu_Screen.Settings:
                                pass

if __name__ == '__main__':
    
    pygame.init()

    Core_Manager = Core()
    Core_Manager.Start()