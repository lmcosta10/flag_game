import pygame
import sys
from country_codes import country_codes
import const

pygame.init()

screen = pygame.display.set_mode([const.SCREEN_X, const.SCREEN_Y])

pygame.display.set_caption('image')

imp = pygame.image.load(".\\country-flags\\ad.png").convert()
flag_x = imp.get_width()
flag_y = imp.get_height()
flag_dim = (flag_x/2, flag_y/2)
imp = pygame.transform.scale(imp, flag_dim)

# Using blit to copy content from one surface to other
screen.blit(imp, (0, 0))

# paint screen one time
pygame.display.flip()

#####
base_font = pygame.font.Font(None, 32) 
user_text = ''
input_rect = pygame.Rect(200, 200, 140, 32)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive

active = False

status = True
while (status):

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            status = False
        
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if input_rect.collidepoint(event.pos): 
                active = True
            else: 
                active = False
        
        if event.type == pygame.KEYDOWN: 

            if event.key == pygame.K_BACKSPACE: 
                user_text = user_text[:-1]
            else: 
                user_text += event.unicode

    if active: 
        color = color_active 
    else: 
        color = color_passive 
    
    pygame.draw.rect(screen, color, input_rect) 
  
    text_surface = base_font.render(user_text, True, (255, 255, 255)) 
    
    screen.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
    
    input_rect.w = max(100, text_surface.get_width()+10) 
    
    pygame.display.flip() 

# deactivates the pygame library
pygame.quit()
sys.exit()
