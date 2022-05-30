from role import Virus
import grid_map as gm
from display import Music
#this class is to store the virus
class Covid_list:
    def __init__(self):
        self.list=[]   #create an empty list to store virus
        self.event_map = []
        self.game_main = gm.pick_dict('game_main')
        self.mouse_click_screen=gm.pick_dict('mouse_click_screen')
        self.scenario = gm.pick_dict('scenario')
    #line 14 - line 52
    #put four types of viruses in corresponding scenario with prepared number and position
    def put_covid1(self, number):
        covid_image=[['alpha.png','die.png'],50,50]
        player1=gm.pick_dict('player')
        virus_position=gm.pick_dict('virus_position')       
        virus_position_list=virus_position[str(number)]
        for i in virus_position_list:
            new_covid=Virus(i[0], i[1], player1, covid_image[0], covid_image[1], covid_image[2], 1, False)
            self.list.append(new_covid)

    def put_covid2(self, number):  
        covid_image = [['beta.png', 'die.png'], 50, 50]
        player1 = gm.pick_dict('player')
        virus_position = gm.pick_dict('virus_position')  

        virus_position_list = virus_position[str(number)]
        for i in virus_position_list:
            new_covid = Virus(i[0], i[1], player1, covid_image[0], covid_image[1], covid_image[2], 1, False)
            self.list.append(new_covid)

    def put_covid3(self, number):  
        covid_image = [['delta.png', 'die.png'], 50, 50]
        player1 = gm.pick_dict('player')
        virus_position = gm.pick_dict('virus_position')  

        virus_position_list = virus_position[str(number)]
        for i in virus_position_list:
            new_covid = Virus(i[0], i[1], player1, covid_image[0], covid_image[1], covid_image[2], 1, False)
            self.list.append(new_covid)

    def put_covid4(self, number):  
        covid_image = [['omicron.png', 'die.png'], 50, 50]
        player1 = gm.pick_dict('player')
        V_count=gm.pick_dict('V_count')
        virus_position = gm.pick_dict('virus_position')  

        virus_position_list = virus_position[str(number)]
        for i in virus_position_list:
            new_covid = Virus(i[0], i[1], player1, covid_image[0], covid_image[1], covid_image[2], 840 // V_count, True)
            self.list.append(new_covid)
    #check the status of virus
    def check_covid_list(self):
        for i in self.list:
            i.virus_check()
    #line 59 - line 73
    #put four types of viruses into the list
    def fresh_covid1(self, number):
        self.list=[]
        self.put_covid1(number)

    def fresh_covid2(self, number):
        self.list=[]
        self.put_covid2(number)

    def fresh_covid3(self, number):
        self.list=[]
        self.put_covid3(number)

    def fresh_covid4(self, number):
        self.list=[]
        self.put_covid4(number)
    #check the status of all the viruses in current scenario, if true, returning to lab
    def check_alive(self):
        count=0
        matrix_dict = gm.pick_dict('matrix_dict')
        for i in self.list:
            if i.show_flag==True:
                return True
            else:
                count+=1
                if count==len(self.list)and len(self.list)==5:
                    self.game_main.update_scenario('A32Q1.png')
                    self.mouse_click_screen.event_map = matrix_dict['A32Q1.png']
                    self.scenario.update_scenario(self.game_main)
                    Music.bgm.stop()
                    Music.play_music(['A32.wav', 1, 1])
                elif count==len(self.list) and len(self.list)==10:
                    self.game_main.update_scenario('A32Q2.png')
                    self.mouse_click_screen.event_map = matrix_dict['A32Q2.png']
                    self.scenario.update_scenario(self.game_main)
                    Music.bgm.stop()
                    Music.play_music(['A32.wav', 1, 1])
                elif count==len(self.list) and len(self.list)==15:
                    self.game_main.update_scenario('A32Q3.png')
                    self.mouse_click_screen.event_map = matrix_dict['A32Q3.png']
                    self.scenario.update_scenario(self.game_main)
                    Music.bgm.stop()
                    Music.play_music(['A32.wav', 1, 1])
                elif count==len(self.list) and len(self.list)==3:
                    self.game_main.update_scenario('win.png')
                    self.mouse_click_screen.event_map = matrix_dict['win.png']
                    self.scenario.update_scenario(self.game_main)
                    Music.bgm.stop()
                    Music.play_music(['you_win.wav', 0, 1])


        return False