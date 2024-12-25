import pygame
import sys
from country_codes import country_codes
from const import *

pygame.init()

screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y])

pygame.display.set_caption('image')

# Pick image
img_path = ".\\country-flags\\ad.png"
imp = pygame.image.load(img_path).convert()

# Get code and country name
country_code = img_path[-6:-4].upper()
country_name = country_codes[country_code]

# Redimensioning and positioning flag
flag_x = imp.get_width()
flag_y = imp.get_height()
end_flag_x = flag_x/2
end_flag_y = flag_y/2
flag_dim = (end_flag_x, end_flag_y)
imp = pygame.transform.scale(imp, flag_dim)

# Using blit to copy content from one surface to other
screen.blit(imp, (0, 0))

# paint screen one time
pygame.display.flip()

## Text input
# Dimensioning and positioning text input
input_rect = pygame.Rect((SCREEN_X-TEXT_WIDTH)/2, end_flag_y, TEXT_WIDTH, TEXT_HEIGHT)
# Text input font
base_font = pygame.font.Font(None, TEXT_HEIGHT)
user_text = ''
# Text input color
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
			elif event.key == pygame.K_RETURN:
				if user_text == country_name:
					print("Correct")
				else:
					print("Wrong")
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
