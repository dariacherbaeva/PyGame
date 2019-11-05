import pygame

pygame.init()

display_width = 800
display_height = 600

usr_width = 60
usr_height = 100
usr_x = display_width // 3
usr_y = display_height - usr_height - 100

display = pygame.display.set_mode((display_width, display_height))

mouse_counter = 0
need_draw_click = False

usr_width = 60
usr_height = 100
usr_x = display_width // 3
usr_y = display_height - usr_height - 100

barrier_options = [69, 449, 37, 410, 40, 420]

clock = pygame.time.Clock()