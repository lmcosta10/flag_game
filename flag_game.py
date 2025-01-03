import pygame
import sys
import random
import os
from country_codes import country_codes
from const import *

pygame.init()

screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y])
pygame.display.set_caption('image')

## Text input
base_font = pygame.font.Font(None, TEXT_HEIGHT)
user_text = ''
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive
active = False

# Dropdown - select country
dropdown_y_spacing = 5
dropdown_width = TEXT_WIDTH + 20
dropdown_font = pygame.font.Font(None, TEXT_HEIGHT - 5)
dropdown_visible = False
filtered_countries = []

# Right or wrong
r_or_w_y_spacing = 5
r_or_w_width = TEXT_WIDTH + 20
r_or_w_font = pygame.font.Font(None, TEXT_HEIGHT - 5)
r_or_w_visible = False
r_or_w_answer = ""
r_or_w_answer_color = pygame.Color('white')

# Next
next_y_spacing = 5
next_width = TEXT_WIDTH - 5
next_font = pygame.font.Font(None, TEXT_HEIGHT - 5)
next_visible = False
next_color = pygame.Color('yellow')

change_flag = True
status = True
while status:

    if change_flag:
        # Pick country randomly
        found_flag = False
        while not found_flag:
            country_code, country_name = random.choice(list(country_codes.items()))
            img_path = ".\\country-flags\\" + country_code.lower() + ".png"
            if os.path.exists(img_path):
                found_flag = True
            else:
                print("Flag not found. Country code: " + country_code + ", country name: " + country_name + "\n")
        imp = pygame.image.load(img_path).convert()

        # Redimensioning and positioning flag
        flag_x = imp.get_width()
        flag_y = imp.get_height()
        end_flag_x = flag_x / 2
        end_flag_y = flag_y / 2
        if end_flag_x > MAX_FLAG_X:
            ratio = MAX_FLAG_X/end_flag_x
            end_flag_x = MAX_FLAG_X
            end_flag_y = end_flag_y * ratio
        if end_flag_y > MAX_FLAG_Y:
            ratio = MAX_FLAG_Y/end_flag_y
            end_flag_y = MAX_FLAG_Y
            end_flag_x = end_flag_x * ratio
        flag_dim = (end_flag_x, end_flag_y)
        imp = pygame.transform.scale(imp, flag_dim)

        # Using blit to copy content from one surface to other
        screen.blit(imp, ((SCREEN_X - end_flag_x) / 2, 0))

        pygame.display.flip()

        ## Positioning rectangles
        input_rect = pygame.Rect((SCREEN_X - TEXT_WIDTH) / 2, end_flag_y, TEXT_WIDTH, TEXT_HEIGHT)
        dropdown_rect = pygame.Rect(input_rect.x, input_rect.y + TEXT_HEIGHT + dropdown_y_spacing, dropdown_width, TEXT_HEIGHT)
        r_or_w_rect = pygame.Rect(input_rect.x, input_rect.y + TEXT_HEIGHT + r_or_w_y_spacing, r_or_w_width, TEXT_HEIGHT)
        next_rect = pygame.Rect(r_or_w_rect.x, r_or_w_rect.y + TEXT_HEIGHT + next_y_spacing, next_width, TEXT_HEIGHT)

        # Clear
        user_text = ""
        r_or_w_visible = False
        filtered_countries = []
        
        change_flag = False

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

            if r_or_w_visible and next_rect.collidepoint(event.pos):
                change_flag = True

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
                if not r_or_w_visible:
                    if user_text.lower() == country_name.lower():
                        r_or_w_answer = "Correct"
                        r_or_w_answer_color = pygame.Color('green')
                    else:
                        r_or_w_answer = "Wrong. Answer: " + country_name + "."
                        r_or_w_answer_color = pygame.Color('red')
                    r_or_w_visible = True
                else:
                    change_flag = True

            elif event.key == pygame.K_TAB:
                if dropdown_visible and filtered_countries:
                    user_text = filtered_countries[0]
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
    if dropdown_visible and not r_or_w_visible:
        for idx, country in enumerate(filtered_countries):
            option_rect = dropdown_rect.move(0, idx * TEXT_HEIGHT)
            pygame.draw.rect(screen, (50, 50, 50), option_rect)
            option_text = dropdown_font.render(country, True, (255, 255, 255))
            screen.blit(option_text, (option_rect.x + 5, option_rect.y + 5))
    
    # Draw answer box and next box
    if r_or_w_visible:
        pygame.draw.rect(screen, (50, 50, 50), r_or_w_rect)
        r_or_w_text = r_or_w_font.render(r_or_w_answer, True, r_or_w_answer_color)
        screen.blit(r_or_w_text, (r_or_w_rect.x + 5, r_or_w_rect.y + 5))

        pygame.draw.rect(screen, (50, 50, 50), next_rect)
        next_text = next_font.render("Next", True, next_color)
        screen.blit(next_text, (next_rect.x + 5, next_rect.y + 5))

    pygame.display.flip()

pygame.quit()
sys.exit()
