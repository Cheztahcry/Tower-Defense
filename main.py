import pygame
import json
from enemy import Enemy
from world import World
from turret import Turret
import constants as const
from button import Button

pygame.init()


game_clock = pygame.time.Clock()
pygame.display.set_caption("Tower Defense")
game_window = pygame.display.set_mode(
    (const.SCREEN_WIDTH + const.SIDE_PANEL, const.SCREEN_HEIGHT))
game_active = True
last_enemy_spawn = pygame.time.get_ticks()

#Variables
placing_turrets = False
selected_turret = None

# Load Images
# turret
turret_sheet = pygame.image.load(
    "assets/turrets/turret_1.png").convert_alpha()
cursor_turret = pygame.image.load(
    "assets/turrets/cursor_turret.png").convert_alpha()

#buttons
buy_turret_image = pygame.image.load("assets/buttons/buy_button.png").convert_alpha()
cancel_turret_image = pygame.image.load("assets/buttons/cancel_button.png").convert_alpha()


# json
with open('levels/waypoints.tmj') as file:
    world_data = json.load(file)


def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // const.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // const.TILE_SIZE
    mouse_tile_num = (mouse_tile_y * const.COLUMS) + mouse_tile_x
    if world.tile_map[mouse_tile_num] == 121:
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False

        if space_is_free == True:
            new_turret = Turret(turret_sheet, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)

def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // const.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // const.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret
        
def clear_selection():
    for turret in turret_group:
        turret.selected = False


# Map
world_surf = pygame.image.load('levels/map.png').convert_alpha()
world = World(world_data, world_surf)
world.process_data()
world.process_enemies()

# Enemy
enemy_images = {
    "common": pygame.image.load('assets/enemies/slime_1.png').convert_alpha(),
    "uncommon": pygame.image.load('assets/enemies/slime_2.png').convert_alpha(),
    "rare": pygame.image.load('assets/enemies/slime_3.png').convert_alpha(),
    "epic": pygame.image.load('assets/enemies/slime_4.png').convert_alpha()
}
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()

print(world.waypoints)

#button
turret_button = Button(const.SCREEN_WIDTH + 50, 120, buy_turret_image, True)
cancel_button = Button(const.SCREEN_WIDTH + 50, 180, cancel_turret_image, True)



while game_active:
    game_clock.tick(const.FPS)
    game_window.fill("White")
    world.draw(game_window)

    # Draw
    enemy_group.draw(game_window)
    for turret in turret_group:
        turret.draw(game_window)

    #Draw Buttons
    if turret_button.draw(game_window):
        placing_turrets = True
    if placing_turrets == True:

        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pygame.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= const.SCREEN_WIDTH:
            game_window.blit(cursor_turret, cursor_rect)
        if cancel_button.draw(game_window):
            placing_turrets = False

    # update group
    enemy_group.update()
    turret_group.update(enemy_group)

    #higlight selected turret
    if selected_turret:
        selected_turret.selected = True

    # spawn enemies
    if pygame.time.get_ticks() - last_enemy_spawn > const.SPAWN_COOLDOWN:
        if world.spawned_enemies < len(world.enemy_list):
            enemy_type = world.enemy_list[world.spawned_enemies]
            enemy = Enemy(enemy_type, world.waypoints, enemy_images)
            enemy_group.add(enemy)
            world.spawned_enemies += 1
            last_enemy_spawn = pygame.time.get_ticks()

    # enemy path
    pygame.draw.lines(game_window, 'Yellow', False, world.waypoints)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < const.SCREEN_WIDTH and mouse_pos[1] < const.SCREEN_HEIGHT:
                selected_turret = None
                clear_selection()
                if placing_turrets == True:
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

    pygame.display.flip()

pygame.quit()
