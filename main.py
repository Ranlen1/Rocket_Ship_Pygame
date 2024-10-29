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
clock = pygame.time.Clock()
run = True
player_position = [368, 750]
hp = 3
text_font = pygame.font.SysFont("Arial", 40)
moving_up = False;moving_down = False;moving_left = False;moving_right = False
meteorites_1 = [];meteorites_2 = []
meteorite_spawn_time_1 = 2000;meteorite_spawn_time_2 = 4100
last_spawn_time_1 = pygame.time.get_ticks();last_spawn_time_2 = pygame.time.get_ticks()
meteorite_falling_speed_1 = 6;meteorite_falling_speed_2 = 4
invulnerability = 0
death_time = 0
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
            meteorites_1.append([meteorite, -meteorite_1.get_height()])
            last_spawn_time_1 = current_time
            if meteorite_spawn_time_1 > 1500:meteorite_spawn_time_1 -= 17
            elif meteorite_spawn_time_1 > 1000:meteorite_spawn_time_1 -= 10
            else:meteorite_spawn_time_1 -= 6
            if meteorite_falling_speed_1 < 8.5:meteorite_falling_speed_1 += 0.05
            elif meteorite_falling_speed_1 < 10:meteorite_falling_speed_1 += 0.04
            else:meteorite_falling_speed_1 += 0.03
        if current_time - last_spawn_time_2 > meteorite_spawn_time_2:
            meteorite = random.randint(0, window_size[0] - meteorite_2.get_width())
            meteorites_2.append([meteorite, -meteorite_2.get_height()])
            last_spawn_time_2 = current_time
            if meteorite_spawn_time_2 > 3000:meteorite_spawn_time_2-=24
            elif meteorite_spawn_time_2 > 2000:meteorite_spawn_time_2-=15
            else:meteorite_spawn_time_2-=8
            if meteorite_falling_speed_2 < 6.5:meteorite_falling_speed_2 += 0.06
            elif meteorite_falling_speed_2 < 8:meteorite_falling_speed_2 += 0.05
            else:meteorite_falling_speed_2 += 0.04
        for meteorite in meteorites_2[:]:
            meteorite[1] += meteorite_falling_speed_2
            if meteorite[1] > window_size[1]:meteorites_2.remove(meteorite)
            else:screen.blit(meteorite_2, meteorite)
            if player_mask.overlap(meteorite_2_mask, (meteorite[0]-player_position[0],meteorite[1] - player_position[1])) and invulnerability <= 0:
                if hp > 1:hp -= 1; invulnerability = 60
                else:death_time = pygame.time.get_ticks();hp = 0
        for meteorite in meteorites_1[:]:
            meteorite[1] += meteorite_falling_speed_1
            if meteorite[1] > window_size[1]:meteorites_1.remove(meteorite)
            else:screen.blit(meteorite_1, meteorite)
            if player_mask.overlap(meteorite_1_mask, (meteorite[0]-player_position[0],meteorite[1] - player_position[1])) and invulnerability <= 0:
                if hp > 1:hp -= 1; invulnerability = 60
                else:death_time = pygame.time.get_ticks();hp = 0
        if moving_up: player_position[1] = max(player_position[1] - 5, -4)
        if moving_down: player_position[1] = min(player_position[1] + 5, 820)
        if moving_left: player_position[0] = max(player_position[0] - 5, -8)
        if moving_right: player_position[0] = min(player_position[0] + 5, 728)
        invulnerability -= 1
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
    pygame.display.update()
    clock.tick(60)