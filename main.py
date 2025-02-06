import pygame, sys, random
from pygame.locals import *
pygame.init()
window_size = (800, 900)
screen = pygame.display.set_mode(window_size, 0, 32)
pygame.display.set_caption('Ship Game')
player = pygame.image.load('ship.png').convert_alpha()
player_rect = player.get_rect()
player_mask = pygame.mask.from_surface(player)
background = pygame.image.load('background.png')
meteorite_1 = pygame.image.load('meteorite_1.png').convert_alpha()
meteorite_1_mask = pygame.mask.from_surface(meteorite_1)
meteorite_2 = pygame.image.load('meteorite_2.png').convert_alpha()
meteorite_2_mask = pygame.mask.from_surface(meteorite_2)
projectile = pygame.image.load('projectile.png').convert_alpha()
projectile_mask = pygame.mask.from_surface(projectile)
clock = pygame.time.Clock()
run = True
player_position = [368, 750]
hp = 3
text_font = pygame.font.SysFont("Arial", 40)
moving_up = False;moving_down = False;moving_left = False;moving_right = False; shooting = False
meteorites_1 = [];meteorites_2 = []; projectile_position = [0, 0]
meteorite_spawn_time_1 = 1400;meteorite_spawn_time_2 = 3250
last_spawn_time_1 = pygame.time.get_ticks();last_spawn_time_2 = pygame.time.get_ticks()
meteorite_falling_speed_1 = 6;meteorite_falling_speed_2 = 4
death_time = 0; projectile_cooldown = 180
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
while run:
    screen.blit(background, (0, 0))
    if hp > 0:
        screen.blit(player, player_position)
        draw_text(str(hp), text_font, (250, 250, 250), 750, 830)
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time_1 > meteorite_spawn_time_1:
            meteorite = random.randint(0, window_size[0] - meteorite_1.get_width())
            meteorites_1.append([meteorite, -meteorite_1.get_height(), 1])
            last_spawn_time_1 = current_time
        if current_time - last_spawn_time_2 > meteorite_spawn_time_2:
            meteorite = random.randint(0, window_size[0] - meteorite_2.get_width())
            meteorites_2.append([meteorite, -meteorite_2.get_height(), 1])
            last_spawn_time_2 = current_time
        if shooting and projectile_position[1] > -9:projectile_position[1] -= 8
        else:shooting = False
        for meteorite in meteorites_2[:]:
            meteorite[1] += meteorite_falling_speed_2
            if meteorite[1] > window_size[1]:meteorites_2.remove(meteorite)
            elif projectile_mask.overlap(meteorite_2_mask, (meteorite[0]-projectile_position[0],meteorite[1] - projectile_position[1])) and shooting:meteorites_2.remove(meteorite); shooting = False
            else:screen.blit(meteorite_2, [meteorite[0], meteorite[1]])
            if player_mask.overlap(meteorite_2_mask, (meteorite[0]-player_position[0],meteorite[1] - player_position[1])) and meteorite[2]:
                meteorite[2] = 0
                if hp > 1:hp -= 1
                else:death_time = pygame.time.get_ticks();hp = 0
        for meteorite in meteorites_1[:]:
            meteorite[1] += meteorite_falling_speed_1
            if meteorite[1] > window_size[1]:meteorites_1.remove(meteorite)
            elif projectile_mask.overlap(meteorite_1_mask, (meteorite[0]-projectile_position[0],meteorite[1] - projectile_position[1])) and shooting:meteorites_1.remove(meteorite); shooting = False
            else:screen.blit(meteorite_1, [meteorite[0], meteorite[1]])
            if player_mask.overlap(meteorite_1_mask, (meteorite[0]-player_position[0],meteorite[1] - player_position[1])) and meteorite[2]:
                meteorite[2] = 0
                if hp > 1:hp -= 1
                else:death_time = pygame.time.get_ticks();hp = 0
        if shooting:
            screen.blit(projectile, projectile_position)
        if moving_up: player_position[1] = max(player_position[1] - 6, -4)
        if moving_down: player_position[1] = min(player_position[1] + 6, 820)
        if moving_left: player_position[0] = max(player_position[0] - 6, -8)
        if moving_right: player_position[0] = min(player_position[0] + 6, 728)
        projectile_cooldown += 1; meteorite_falling_speed_1 += 0.002; meteorite_falling_speed_2 += 0.002; meteorite_spawn_time_1 -= 0.17; meteorite_spawn_time_2 -= 0.14
    else:
        draw_text("YOU DIED", text_font, (255, 0, 0), 300, 450)
        if pygame.time.get_ticks() - death_time > 1000:
            pygame.quit()
            sys.exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_w: moving_up = True
            if event.key == K_s: moving_down = True
            if event.key == K_a: moving_left = True
            if event.key == K_d: moving_right = True
        if event.type == KEYUP:
            if event.key == K_w: moving_up = False
            if event.key == K_s: moving_down = False
            if event.key == K_a: moving_left = False
            if event.key == K_d: moving_right = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT and projectile_cooldown >= 180:
                shooting = True; projectile_cooldown = 0; projectile_position = [player_position[0]+36, player_position[1]-4]
    pygame.display.update()
    clock.tick(60)