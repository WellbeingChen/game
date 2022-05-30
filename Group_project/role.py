import pygame
import grid_map as gm
from display import Display, Music

#this class is the parent class to Player and Virus
class Role:
    #display player and virus on the screen
    def show(self):
        game_main = gm.pick_dict('game_main')  
        Display.display_image(game_main.screen, self.image, self.position, self.pic_index, self.direction, self.image_x,
                              self.image_y)
    #movement of player and virus
    def move(self):
        mouse_click_screen = gm.pick_dict('mouse_click_screen')
        scenario = gm.pick_dict('scenario')

        if mouse_click_screen.show_flag == False:
            target_p1 = self.position.move([5 * i for i in self.speed])  
            target_p2 = self.position.move(self.speed)
            # player and virus can not move forward
            if not scenario.check_boundary(list(target_p1)):  
                self.target_position = self.position
            # player and virus can move forward
            else:  
                self.position = target_p2
                #display the dynamic effect of player and virus when moving
                self.pic_index = (self.pic_index + 1) % 3
        self.show()
''' Inspiration idea of rect in Chinese:
    https://blog.csdn.net/TheCity2333/article/details/106958808?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.essearch_pc_relevant&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.essearch_pc_relevant
    use rect function in pygame can spot part of a picture effectively
    also get some core value (e.g. center coordinate)
 '''
#this class is to define player
class Player(Role):

    def __init__(self, picture_list, image_x, image_y, x=0, y=0):
        self.picture_list = picture_list 
        self.image = pygame.image.load('pic/' + self.picture_list[0]).convert_alpha()
        self.position = self.image.get_rect(center=(x, y))
        self.speed = [0, 0]  # speed in x axis and y axis seperately
        self.direction = 0 
        self.pic_index = 1  # Get the character in the second column of the play.png pic
        self.target_position = self.position  
        self.attack_index = 0  # define the attack status
        self.image_x = image_y  # width of player
        self.image_y = image_x  # height of player
        self.show_flag = True  # check whether the player is alive or not
    #update displaying the player
    def update(self, position):
        self.show_flag = True
        self.position = self.image.get_rect(center=position)
        self.speed = [0, 0]
        self.target_position = self.position
    #player walks
    def walk(self, speed_number):  # Move speed_number*speed
        new_speed = [speed_number * i for i in self.speed]
        self.target_position = self.position.move(new_speed)
    #check status
    def role_check(self):  
        mouse_click_screen = gm.pick_dict('mouse_click_screen')
        matrix_dict = gm.pick_dict('matrix_dict')
        appear_list1 = [matrix_dict['A32Q0.png'], matrix_dict['A32Q1.png'], matrix_dict['A32Q2.png'], matrix_dict['A32Q3.png'],
                        matrix_dict['factory.png'], matrix_dict['desert.png'], matrix_dict['park.png'], matrix_dict['ground.png']]
        #only if player has not reach the target position, it can move
        if self.show_flag:  
            if self.target_position != self.position:
                self.move()
            else:
                if self.attack_index == 0:  
                    self.pic_index = 1
                else:
                    self.attack()
                #only if player is in these scenarios, player can be displayed on the screen    
                if mouse_click_screen.event_map in appear_list1:
                    self.show()
    #change into attack status
    def attack(self):
        self.attack_index = 1

#this class is to define virus
class Virus(Role):

    def __init__(self, x, y, target, picture_list, image_x, image_y, life, is_boss):
        self.picture_list = picture_list
        self.image = pygame.image.load('pic/' + self.picture_list[0]).convert_alpha()
        self.position = self.image.get_rect(center=(x, y))
        self.speed = [0, 0]
        self.direction = 0
        self.pic_index = 1  
        self.target = target
        self.target_position = target.position
        self.show_flag = True
        self.image_x = image_x
        self.image_y = image_y
        self.attack = -1
        self.life = life    #virus has life
        self.is_boss = is_boss   #viruses can be divided into normal type and boss type
        self.infect_range = 30  #initial range of infection

    def virus_check(self):
        #if the virus is alive 
        if self.show_flag:  
            #if player is alive
            if self.attack == -1 and self.target.show_flag:  
                self.target_position = self.target.position  
                #calculate the distance between virus and player
                d, x, y = Virus.get_distance(self.position.left, self.target.position.left, self.position.top,
                                             self.target.position.top)
                self.self_target_distance = d
                if d >= 30:
                    #if the distance between virus and player is bigger than infection range
                    self.get_speed(d, x, y)
                    self.move()
                else:
                    #if in the infect range, player will get infected——then gameover
                    self.infect()
                    self.show()

            else:
                self.show_flag = False  
    #virus will infect player
    def infect(self):
        mouse_click_screen = gm.pick_dict('mouse_click_screen')
        event_dict = gm.pick_dict('event_dict')
        matrix_dict = gm.pick_dict('matrix_dict')
        scenario = gm.pick_dict('scenario')
        virus_list = gm.pick_dict('virus_list')
        #if player is in the infection range, gameover
        if self.self_target_distance <= self.infect_range:  
            mouse_click_screen.game_main.update_scenario(event_dict['loss'][0])
            mouse_click_screen.event_map = matrix_dict[event_dict['loss'][0]]
            scenario.update_scenario(mouse_click_screen.game_main)
            Music.bgm.stop()
            Music.play_music(['game_over.wav', 0, 1])
            virus_list.list = []
        self.image = pygame.image.load('pic/' + self.picture_list[1]).convert_alpha()
        self.image_x = 50
        self.image_y = 50
        self.attack = 0
        self.direction = 0
        self.pic_index = 0
        Music.play_music(["boom.wav", 0, 0.5])
    #calculate the speed of virus when moving towards player
    def get_speed(self, d, x, y): 
        if d >= 1:  
            new_speed_x = -x / d * 1.414
            new_speed_y = -y / d * 1.414
        else:
            new_speed_x = -x
            new_speed_y = -y
        self.speed = [new_speed_x, new_speed_y]
    #calculate the Euclidean distance between virus and player 
    def get_distance(p1, p2, p3, p4):
        x = p1 - p2
        y = p3 - p4
        d = (x ** 2 + y ** 2) ** (0.5)
        return d, x, y
