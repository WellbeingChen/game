import pygame

# This class is to display various elements
class Display:
    #display the image in the screen
    def display_image(screen, player, position, image_x, image_y, image_w, image_h):  
        screen.blit(player, position, (image_x * image_w, image_y * image_h, image_w, image_h))
    #display the mouse to call events
    def display_mouse_screen(screen, image): 
        mouse_position = (0, 0)
        screen.blit(image, mouse_position)
    #display the text onto the screen when answering the question
    def display_str(screen, text, position=(672, 224)):  # Show words in screen
        font_type = "century gothic BOLD.ttf"  #font name
        font_size = 35
        font_color = pygame.Color(0, 0, 0)  #R.G.B format
        font = pygame.font.Font(font_type, font_size)
        text_set = font.render(text, True, font_color)
        screen.blit(text_set, position)

#This class is to play various kinds of music
class Music:
    pygame.mixer.init()
    bgm = pygame.mixer.Sound("music/" + 'start.wav')

    def play_music(music):
        if music[1] == 0:  #play short music for one time
            music_play = pygame.mixer.Sound("music/" + music[0])
            music_play.set_volume(music[2])
            music_play.play()
        else:  #play long music in loop
            Music.bgm = pygame.mixer.Sound("music/" + music[0])
            Music.bgm.set_volume(music[2])
            Music.bgm.stop()
            Music.bgm.play(loops=-1)  
