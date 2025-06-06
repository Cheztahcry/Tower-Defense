import pygame
import json
from enemy import Enemy
from world import World
from turret import Turret
import constants as const

pygame.init() 



game_clock = pygame.time.Clock()
pygame.display.set_caption("Tower Defense")
game_window = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
game_active = True
last_enemy_spawn = pygame.time.get_ticks()





#Load Images

cursor_turret = pygame.image.load("assets/turrets/cursor_turret.png").convert_alpha()


#json
with open('levels/waypoints.tmj') as file:
    world_data = json.load(file)

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // const.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // const.TILE_SIZE
    turret = Turret(cursor_turret, mouse_tile_x, mouse_tile_y)
    turret_group.add(turret)

#Map
world_surf = pygame.image.load('levels/map.png').convert_alpha()
world = World(world_data, world_surf)
world.process_data()
world.process_enemies()

#Enemy
enemy_images = {
    "common" : pygame.image.load('assets/enemies/slime_1.png').convert_alpha(),
    "uncommon" : pygame.image.load('assets/enemies/slime_2.png').convert_alpha(),
    "rare" : pygame.image.load('assets/enemies/slime_3.png').convert_alpha(),
    "epic" : pygame.image.load('assets/enemies/slime_4.png').convert_alpha()



}
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()

print(world.waypoints)





while game_active:
    game_clock.tick(const.FPS)
    game_window.fill("White")
    world.draw(game_window)

    #Draw
    enemy_group.draw(game_window)
    turret_group.draw(game_window)

    #update group
    enemy_group.update()

    #spawn enemies
    if pygame.time.get_ticks() - last_enemy_spawn > const.SPAWN_COOLDOWN:
        if world.spawned_enemies <  len(world.enemy_list):
            enemy_type = world.enemy_list[world.spawned_enemies]
            enemy = Enemy(enemy_type, world.waypoints, enemy_images)
            enemy_group.add(enemy)
            world.spawned_enemies += 1
            last_enemy_spawn = pygame.time.get_ticks()

    #enemy path
    pygame.draw.lines(game_window, 'Yellow', False, world.waypoints)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==  1:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < const.SCREEN_WIDTH and mouse_pos[1] < const.SCREEN_HEIGHT:
                create_turret(mouse_pos)
                





    pygame.display.flip()

pygame.quit()


