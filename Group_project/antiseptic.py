import pygame
import grid_map as gm
from display import Display
from role import Virus

#this class is to store antiseptic(type of attack by player)
class Antiseptic_bottle:

    def __init__(self):
        self.lst = []  #initialize an empty bottle
    #add new antiseptic to the bottle
    def add_antiseptic(self, image, position, speed, direction):
        new_antiseptic = Antiseptic(image, position, speed, direction)
        self.lst.append(new_antiseptic)
    #for antiseptic in the bottle, once shooted out, keeping moving according to its position 
    def check_antiseptic_bottle(self):
        for i in self.lst:
            if i.flag:
                i.check_position()  
                i.move()
    #when player attacks, shoot the antiseptic from the bottle
    def shoot(self):  
        player = gm.pick_dict('player')  
        antiseptic_image = 'antiseptic.png'  
        SPEED = 5  #move speed
        if player.direction == 0:  #when player turns down
            antiseptic_position = (player.position.center[0] - player.image_x // 3, player.position.center[1])
            antiseptic_speed = [0, SPEED]
        elif player.direction == 1:  #when player turns left
            antiseptic_position = (player.position.center[0] - player.image_x, player.position.center[1] - player.image_y // 2)
            antiseptic_speed = [-SPEED, 0]
        elif player.direction == 2:  #when player turns right
            antiseptic_position = (player.position.center[0], player.position.center[1] - player.image_y // 2)
            antiseptic_speed = [SPEED, 0]
        elif player.direction == 3:  #when player turns up
            antiseptic_position = (player.position.center[0] - player.image_x // 3, player.position.center[1] - player.image_y)
            antiseptic_speed = [0, -SPEED]
        self.add_antiseptic(antiseptic_image, antiseptic_position, antiseptic_speed, player.direction)  # append new bullet object

#this class is to define antiseptic(type of attack by player)
class Antiseptic:

    def __init__(self, image, position, speed, direction):
        #initialize some attributes 
        #image：antiseptic picture; 
        #postion：antiseptic coordinates; speed：moving speed; 
        #direction: shooting direction

        self.image = pygame.image.load('pic/' + image).convert_alpha()
        self.position = self.image.get_rect(center=position)
        self.speed = speed
        #set the shooting range of antiseptic to 200 pixels.
        self.new_speed = [40 * i for i in self.speed]
        self.target_position = self.position.move(self.new_speed) 
        self.direction = direction  
        self.flag = True  #True if the antiseptic is still in the shooting range
        self.pic_index = 1
        self.image_x = 30  # Bullet size
        self.image_y = 30

    def move(self):  #move
        target_position = self.position.move(self.speed)
        # When the antiseptic is still in the shooting range, displaying it on the window
        if self.position != self.target_position:  
            self.position = target_position
            self.show()
        else:  # When the antiseptic is out of the shooting range, it disappears
            self.flag = False

    def show(self):
        game_main = gm.pick_dict('game_main')
        Display.display_image(game_main.screen, self.image, self.position, self.pic_index, self.direction, self.image_x,
                              self.image_y)

    def check_position(self):
        attack_range = 30  #define a range to kill the virus
        virus_list = gm.pick_dict('virus_list')
        for i in virus_list.list:
            if i.show_flag and i.attack == -1:  # When the monster is alive and wriggling, calculate the distance between the bullet and the monster
                d, x, y = Virus.get_distance(self.position.center[0], i.position.center[0], self.position.center[1],
                                             i.position.center[1])
                #if virus is not the omicron type
                if not i.is_boss:
                    # When the distance between antiseptic and virus is less than 30, 
                    # the virus will be killed and antiseptic disappears at the same time
                    if d <= attack_range:  
                        i.infect()
                        self.flag = False
                else:
                    if d < attack_range:
                        i.life -= 1   #once in the killing range, the life of virus reduces
                        if i.life < 1:
                            i.infect()  
                            self.flag = False
