import pygame
from scenario import Scenario_operation
import grid_map as gm
from display import Display, Music

#this class is to interact between the mouse and the game window
class Mouse_click:

    def __init__(self, info_lst):
        matrix_dict = gm.pick_dict('matrix_dict')
        self.show_flag = True
        self.image = pygame.image.load('pic/' + info_lst[0]).convert_alpha()
        self.text = []
        self.key = ''
        self.event_map = matrix_dict[info_lst[1]]  # Get event list
        self.game_main = gm.pick_dict('game_main')

    def show(self):
        Display.display_mouse_screen(self.game_main.screen, self.image)
    #show text when answering the question
    def text_show(self):
        text_area = (672, 224)
        Display.display_str(self.game_main.screen, ''.join(self.text), text_area)

    def check_text(self):
        if self.show_flag:
            self.show()
        else:
            if self.text != []:  # show the text when it is not empty
                self.text_show()
    # Set the mouse interface
    def mouse_fresh_screen(self, info_lst):  
        matrix_dict = gm.pick_dict('matrix_dict')
        self.image = pygame.image.load('pic/' + info_lst[0]).convert_alpha()
        self.show_flag = True
        self.event_map = matrix_dict[info_lst[1]]
    #get the event keywords in various matrixs
    def obtain_event(self, position):  
        event = 'none'
        if self.event_map != []:
            new_position = Scenario_operation.convert_coordinate(position, 0)
            event = self.event_map[new_position[0]][new_position[1]]
        return event
    #operate different functions according to event keywords
    def check_event(self, position):  
        scenario = gm.pick_dict('scenario')
        event_dict = gm.pick_dict('event_dict')
        player = gm.pick_dict('player')
        virus_list = gm.pick_dict('virus_list')
        matrix_dict = gm.pick_dict('matrix_dict')
        V_count = gm.pick_dict('V_count')

        event = self.obtain_event(position)  

        if event != 1 and event != 0:
            if event == 'back' :   #back to homepage
                self.mouse_fresh_screen(event_dict[event])
                self.game_main.update_scenario(event_dict[event][0])
                scenario.update_scenario(self.game_main)
                Music.play_music(['click.wav', 0, 1])
                Music.bgm.stop()
                Music.play_music(['start.wav', 1, 1])  

            elif event == 'start':  #game start
                V_count=1
                gm.add_dict('V_count', V_count)
                self.show_flag = False
                self.game_main.update_scenario(event_dict[event][0])
                self.event_map = matrix_dict[event_dict[event][0]]
                scenario.update_scenario(self.game_main)

            elif event == 'help1':  #see the help page
                self.show_flag = False
                self.game_main.update_scenario(event_dict[event][0])
                self.event_map = matrix_dict[event_dict[event][0]]
                scenario.update_scenario(self.game_main)
                Music.play_music(['click.wav', 0, 1])

            elif event == 'lt':  #read the letter
                self.show_flag = False
                self.game_main.update_scenario(event_dict[event][0])
                self.event_map = matrix_dict[event_dict[event][0]]
                scenario.update_scenario(self.game_main)
                Music.bgm.stop()
                Music.play_music(event_dict[event][2])

            elif event == 'loss':  #gameover
                self.show_flag = False
                self.game_main.update_scenario(event_dict[event][0])
                self.event_map = matrix_dict[event_dict[event][0]]
                scenario.update_scenario(self.game_main)
                Music.bgm.stop()
                Music.play_music(['game_over.wav', 0, 1]) 

            elif event == 'Th' or event == 'Is':  #choose character
                if event == 'Th':
                    player.image = pygame.image.load('pic/' + player.picture_list[0]).convert_alpha()
                elif event == 'Is':
                     player.image = pygame.image.load('pic/' + player.picture_list[1]).convert_alpha()
                self.event_map = matrix_dict[event_dict[event][0]]
                self.game_main.update_scenario(event_dict[event][0])
                scenario.update_scenario(self.game_main)
                player.update(event_dict[event][1])
                Music.bgm.stop()
                Music.play_music(['click.wav', 0, 1])
                Music.play_music(event_dict[event][2])
            
            elif event == 'q1':   #answer question1
                self.game_main.update_scenario(event_dict[event][0])
                self.event_map = matrix_dict[event_dict[event][0]]
                self.key = '2'
                Music.play_music(['click.wav', 0, 1])
            elif event == 'q2':   #answer question2
                self.game_main.update_scenario(event_dict[event][0])
                self.event_map = matrix_dict[event_dict[event][0]]
                self.key = '24'
                Music.play_music(['click.wav', 0, 1])
            elif event == 'q3':   #answer question3
                self.game_main.update_scenario(event_dict[event][0])
                self.event_map = matrix_dict[event_dict[event][0]]
                Music.play_music(['click.wav', 0, 1])
                self.key = 'PYGAME'

            elif event == 11:  #delete the text of answer
                if len(self.text) >= 1:
                    self.text.pop()  # pop delete the last input number
                Music.play_music(['click.wav', 0, 1])

            #   Inspiration code for transfer list to string:
            #   https://www.simplilearn.com/tutorials/python-tutorial/list-to-string-in-python
            #   we use join() to transfer list to string in order to check the answer

            elif event == 12:  #submit the answer
                if ''.join(self.text) == self.key:  
                    self.show_flag = False
                    self.text = []
                    if self.key == '2':
                        self.game_main.update_scenario(event_dict['V1S'][0])
                        self.event_map = matrix_dict[event_dict['V1S'][0]]
                        V_count += 1     #inject vaccine1 
                        gm.add_dict('V_count', V_count)
                    elif self.key == '24':
                        self.game_main.update_scenario(event_dict['V2S'][0])
                        self.event_map = matrix_dict[event_dict['V2S'][0]]
                        V_count += 2     #inject vaccine2
                        gm.add_dict('V_count', V_count)
                    elif self.key=='PYGAME':
                        self.game_main.update_scenario(event_dict['V3S'][0])
                        self.event_map = matrix_dict[event_dict['V3S'][0]]
                        V_count += 3     #inject vaccine3
                        gm.add_dict('V_count', V_count)
                    scenario.update_scenario(self.game_main)
                    Music.bgm.stop()
                    Music.play_music(['success.wav', 0, 1])
                else:
                    self.text = []

            elif event == 13:  #abandon answering the question
                self.show_flag = False
                if self.key == '2':
                    self.game_main.update_scenario(event_dict['V1F'][0])
                    self.event_map = matrix_dict[event_dict['V1F'][0]]
                elif self.key == '24':
                    self.game_main.update_scenario(event_dict['V2F'][0])
                    self.event_map = matrix_dict[event_dict['V2F'][0]]
                elif self.key == 'PYGAME':
                    self.game_main.update_scenario(event_dict['V3F'][0])
                    self.event_map = matrix_dict[event_dict['V3F'][0]]
                Music.bgm.stop()
                Music.play_music(['error.wav', 0, 1])
                self.text = []
            #type text on the screen
            elif (type(event) == int and (event >= 1 and event <= 10)) or (event >= 'A' and event <= 'Z'):
                # Password lock interface-typing
                if (type(event) == int and event == 10):
                    event = 0
                if len(self.text) <= 10:
                    self.text.append(str(event))
                Music.play_music(['click.wav', 0, 1])

            elif event == 'm2':     #go to fight alpha type virus
                self.show_flag = False
                self.game_main.update_scenario(event_dict[event][0])
                self.event_map = matrix_dict[event_dict[event][0]]
                scenario.update_scenario(self.game_main)
                player.update(event_dict[event][2])
                virus_list.fresh_covid1(event_dict[event][1])
                Music.bgm.stop()
                Music.play_music(event_dict[event][3])

            elif event == 'm3':    #go to fight beta type virus
                self.show_flag = False
                self.game_main.update_scenario(event_dict[event][0])
                self.event_map = matrix_dict[event_dict[event][0]]
                scenario.update_scenario(self.game_main)
                player.update(event_dict[event][2])
                virus_list.fresh_covid2(event_dict[event][1])
                Music.bgm.stop()
                Music.play_music(event_dict[event][3])

            elif event == 'm4':     #go to fight delta type virus
                self.show_flag = False
                self.game_main.update_scenario(event_dict[event][0])
                self.event_map = matrix_dict[event_dict[event][0]]
                scenario.update_scenario(self.game_main)
                player.update(event_dict[event][2])
                virus_list.fresh_covid3(event_dict[event][1])
                Music.bgm.stop()
                Music.play_music(event_dict[event][3])

            elif event == 'm5':    #go to fight omicron type virus
                self.show_flag = False
                self.game_main.update_scenario(event_dict[event][0])
                self.event_map = matrix_dict[event_dict[event][0]]
                scenario.update_scenario(self.game_main)
                player.update(event_dict[event][2])
                virus_list.fresh_covid4(event_dict[event][1])
                Music.bgm.stop()
                Music.play_music(event_dict[event][3])
