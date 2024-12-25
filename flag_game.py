import pygame
import sys
import random
from country_codes import country_codes
from const import *

pygame.init()

screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y])

pygame.display.set_caption('image')

# Pick country randomly
# TODO: check if there's an image for every country code
country_code, country_name = random.choice(list(country_codes.items()))
img_path = ".\\country-flags\\" + country_code.lower() + ".png"
imp = pygame.image.load(img_path).convert()

# Redimensioning and positioning flag
flag_x = imp.get_width()
flag_y = imp.get_height()
end_flag_x = flag_x/2
end_flag_y = flag_y/2
flag_dim = (end_flag_x, end_flag_y)
imp = pygame.transform.scale(imp, flag_dim)

# Using blit to copy content from one surface to other
screen.blit(imp, ((SCREEN_X-end_flag_x)/2, 0))

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

# Dropdown - select country
dropdown_rect = pygame.Rect(input_rect.x, input_rect.y + TEXT_HEIGHT + 5, TEXT_WIDTH + 20, TEXT_HEIGHT)
dropdown_font = pygame.font.Font(None, TEXT_HEIGHT - 5)
dropdown_visible = False
filtered_countries = []

status = True
while status:

    screen.fill((0, 0, 0))  # Clear screen for redrawing
    screen.blit(imp, ((SCREEN_X - end_flag_x) / 2, 0))  # Redraw flag

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

            # Handle selection from the dropdown
            if dropdown_visible:
                for idx, country in enumerate(filtered_countries):
                    option_rect = dropdown_rect.move(0, idx * TEXT_HEIGHT)
                    if option_rect.collidepoint(event.pos):
                        user_text = country
                        dropdown_visible = False
                        break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.key == pygame.K_RETURN:
                if user_text.lower() == country_name.lower():
                    print("Correct")
                else:
                    print("Wrong")
            else:
                user_text += event.unicode

            # Update dropdown visibility and filter list
            if user_text.strip():
                filtered_countries = [
                    name for name in country_codes.values()
                    if user_text.lower() in name.lower()
                ]
                dropdown_visible = bool(filtered_countries)
            else:
                dropdown_visible = False

    # Input box color
    color = color_active if active else color_passive

    # Draw input box
    pygame.draw.rect(screen, color, input_rect)
    text_surface = base_font.render(user_text, True, (255, 255, 255))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    input_rect.w = max(100, text_surface.get_width() + 10)

    # Draw dropdown
    if dropdown_visible:
        for idx, country in enumerate(filtered_countries):
            option_rect = dropdown_rect.move(0, idx * TEXT_HEIGHT)
            pygame.draw.rect(screen, (50, 50, 50), option_rect)
            option_text = dropdown_font.render(country, True, (255, 255, 255))
            screen.blit(option_text, (option_rect.x + 5, option_rect.y + 5))

    pygame.display.flip()

# deactivates the pygame library
pygame.quit()
sys.exit()
