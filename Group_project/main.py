import pygame
import grid_map as gm
from scenario import Scenario_config, Scenario_operation
from role import Player
from covid import Covid_list
from mouse import Mouse_click
from display import Music
from antiseptic import Antiseptic_bottle

'''
Picture files used by this game( .PNG format).
     he players pictures(Isaac.png,Thor.png)
	 The map pictur(A32Q0.png,A32Q1.png,A32Q2.png,A32Q3.png,factory.png,
                 desert.png,ground.png,park.png)
     The attackers and bullet pictures(alpha.png,beta.png,delta.png,omicron.png,anseptic.png)
     The other pictures(win.png,gameover.png,select_player.png,start.png,question1.png,question2.png,question3.png)
     Pictures above are all made by RPG Maker MZ. 
     
     The remaining pictures(die.png,help1.png,letter.png,vaccine1_fail.png,
     vaccine1_success.png,vaccine2_fail.png,vaccine2_success.png,vaccine3_fail.png,vaccine3_success.png)
	 Pictures above are made by Photoshop and the material in the pictures is available for purchase 
     via the following link:https://588ku.com/


Music files used by this game(.WAV format).
	 All music used by this document are downloaded from this link:
	 https://opengameart.org/
	 Copyright allowed to be used
     
Fonts used in this game
     Download it at the following link and allow users to use it for free:
     https://www.aigei.com/

'''

# Initialize the pygame window and some basic parameters
WINDOW_SIZE = (1152, 800)
WINDOW_INIT_IMAGE = 'select_player.png'
TITLE = 'COVID WAR'
PLAYER_INIT_IMAGE = [['Thor.png', 'Isaac.png'], 50, 50]
MOUSE_INIT = ['start.png', 'start']
MUSIC_INIT = ['start.wav', 1, 1]
TIME = 60  #define the flip rate
SPEED = 5  
MOVE_PIXEL = 3  #the pixels of movement when press the keyboard once
V_count = 1   #count the vaccine that would be taken in the game 

pygame.init()

#line 54 - line 66
#this block of code creates several instances of different classes seperately 
#after creating, storing these instances as values in a dictionary in order to call them efficiently
''' Inspiration idea of storing instances in dicionary :
    https://stackoverflow.com/questions/38706855/edit-save-dictionary-in-another-python-file
    then those instances can be treated as global variables to call efficiently 
 '''
game_main = Scenario_config(WINDOW_SIZE, WINDOW_INIT_IMAGE, TITLE)
gm.add_dict('game_main', game_main)
scenario = Scenario_operation(game_main)
gm.add_dict('scenario', scenario)
player = Player(PLAYER_INIT_IMAGE[0], PLAYER_INIT_IMAGE[1], PLAYER_INIT_IMAGE[2])
gm.add_dict('player', player)
mouse_click_screen = Mouse_click(MOUSE_INIT)
gm.add_dict('mouse_click_screen', mouse_click_screen)
virus_list = Covid_list()
gm.add_dict('virus_list', virus_list)
antiseptic_bottle = Antiseptic_bottle()
gm.add_dict('antiseptic_bottle', antiseptic_bottle)
gm.add_dict('V_count', V_count)

clock = pygame.time.Clock()   # create an object to track the time
Music.play_music(MUSIC_INIT)  # Initializing music playback

while (True):
    clock.tick(TIME)  #refresh
    #monitor the events
    e = pygame.event.poll()
    if e.type == pygame.QUIT:   #quit the game
        break
    
    ''' Inspiration code for monitoring the keboard :
        https://stackoverflow.com/questions/67921521/is-there-a-more-efficient-version-of-pygame-key-get-pressedpygame-k 
        we use pygame.key.get_pressed() to obtain the status of the keyboard.
    '''

    if not mouse_click_screen.show_flag:   #when do not click the mouse
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:  #player can attack
                player.attack()
                antiseptic_bottle.shoot()

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_DOWN]:  #player can go down
            player.speed = [0, SPEED]   #define the speed in this direction to be non-negative
            player.direction = 0
            player.walk(MOVE_PIXEL)
        elif key_pressed[pygame.K_LEFT]:  #player can go left
            player.speed = [-SPEED, 0]  #alter the speed according to the direction
            player.direction = 1  
            player.walk(MOVE_PIXEL)  
        elif key_pressed[pygame.K_RIGHT]:  #player can go right
            player.speed = [SPEED, 0]     #define the speed in this direction to be non-negative
            player.direction = 2
            player.walk(MOVE_PIXEL)
        elif key_pressed[pygame.K_UP]:  #player can go up
            player.speed = [0, -SPEED]  #alter the speed according to the direction
            player.direction = 3
            player.walk(MOVE_PIXEL)

    if e.type == pygame.MOUSEBUTTONDOWN:   #when click the mouse
        #obtain the coordinate of the click point to operate various events
        mouse_click_screen.check_event(e.pos)  
    #in these maps checking whether all the viruses are alive, if not, back to lab
    if (game_main.scenario_name == 'factory.png' or game_main.scenario_name == 'desert.png' or
            game_main.scenario_name == 'park.png' or game_main.scenario_name == 'ground.png'):
        virus_list.check_alive()

    #keep running the methods of judging different elements and display corresponding results
    game_main.display_scenario()
    player.role_check()
    virus_list.check_covid_list()
    antiseptic_bottle.check_antiseptic_bottle()
    mouse_click_screen.check_text()
    pygame.display.flip()

pygame.quit()

