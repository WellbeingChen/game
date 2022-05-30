import pygame
import grid_map as gm

#this class is to config the scenario
class Scenario_config:
    def __init__(self, screen_size, scenario_name, title):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(title)
        self.update_scenario(scenario_name)  
    #display background scenario
    def display_scenario(self):
        screen_position = (0, 0)
        self.screen.blit(self.background, screen_position)
    #update the background scenario
    def update_scenario(self, scenario_name):  
        self.scenario_name = scenario_name
        self.background = pygame.image.load('pic/' + self.scenario_name).convert()

''' Inspiration idea of using matrix to represent different areas in a scenario:
    https://github.com/zxf20180725/pygame-jxzj/blob/master/04_1_%E4%BA%BA%E7%89%A9%E8%A1%8C%E8%B5%B0_%E5%9C%B0%E5%9B%BE%E8%AE%BE%E8%AE%A1/jxzj/core.py
    this method can help bulid an explicit connection between scenario and functions and events of it
 '''
class Scenario_operation:

    grid_size = [36, 25]  #set the size of matrix

    def __init__(self, game_main):
        self.update_scenario(game_main)

    ''' Inspiration idea of using Cartesian coordinates in Chinese:
        http://programarcadegames.com/index.php?lang=en&chapter=introduction_to_graphics
        this method can help use Pygame coordinates which connected with Cartesian coordinates
     '''
    #calculate the coordinate value of the original grid pixels and size of matrix
    def convert_coordinate(position, pixel):
        Scenario_operation.game_main = gm.pick_dict('game_main')
        new_position = [0, 0]
        #pixel is half height and half width of role (in this program, these two values are equal)

        new_position[1] = int((position[0] + pixel) // (Scenario_operation.game_main.screen_size[0] / Scenario_operation.grid_size[0]))
        new_position[0] = int((position[1] + pixel) // (Scenario_operation.game_main.screen_size[1] / Scenario_operation.grid_size[1]))
        return new_position
    #check whether the current position is boundary
    def check_boundary(self, position):  
        new_position = Scenario_operation.convert_coordinate(position, 25)
        #if it is outside boundary, then can not move ahead
        if (new_position[0] < 0 or new_position[0] > Scenario_operation.grid_size[1] - 1
                or new_position[1] < 0 or new_position[1] > Scenario_operation.grid_size[0] - 1):
            return 0
        #if it is inside boundary, then can move ahead
        return self.scenario[new_position[0]][new_position[1]]

    def update_scenario(self, game_main):
        matrix_dict = gm.pick_dict('matrix_dict')
        self.scenario_name = game_main.scenario_name
        self.scenario = matrix_dict[self.scenario_name]
