import pygame
import json
from enemy import Enemy
from world import World
from turret import Turret
import constants as const
from button import Button

def start_game():
    pygame.init()
    pygame.mixer.init()


    game_clock = pygame.time.Clock()
    pygame.display.set_caption("LockDown-Defense")
    game_window = pygame.display.set_mode(
        (const.SCREEN_WIDTH + const.SIDE_PANEL, const.SCREEN_HEIGHT))
    game_active = True
    last_enemy_spawn = pygame.time.get_ticks()

    icn = pygame.image.load("assets/bg_image/turret_icon.png").convert_alpha()
    pygame.display.set_icon(icn)

    # Variables
    game_over = False
    game_outcome = 0 #-1 is a loss and 1 is win  
    level_started = False
    placing_turrets = False
    selected_turret = None

    #Load Music
    pygame.mixer.music.load("assets/audio/bg_music.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    #Sound fx
    #Sound fx
    plc_fx = pygame.mixer.Sound("assets/audio/place_fx.mp3")
    plc_fx.set_volume(0.6)
    upg_fx = pygame.mixer.Sound("assets/audio/upgrade_fx.mp3")
    upg_fx.set_volume(0.6)
    click_fx = pygame.mixer.Sound("assets/audio/click.mp3")
    click_fx.set_volume(0.5)
    gm_ovr_fx = pygame.mixer.Sound("assets/audio/game_over_fx.mp3")
    gm_ovr_fx.set_volume(0.5)

    # Load Images
    # turret
    turret_spritesheets = []
    for x in range(1, const.TURRET_LEVEL + 1):
        turret_sheet = pygame.image.load(
            f"assets/turrets/turret_{x}.png").convert_alpha()
        turret_spritesheets.append(turret_sheet)
    cursor_turret = pygame.image.load(
        "assets/turrets/cursor_turret.png").convert_alpha()

    # buttons
    buy_turret_image = pygame.image.load(
        "assets/buttons/BUY.png").convert_alpha()
    cancel_turret_image = pygame.image.load(
        "assets/buttons/CANCEL.png").convert_alpha()
    upgrade_turret_image = pygame.image.load(
        "assets/buttons/upgrade_button.png").convert_alpha()
    begin_image = pygame.image.load(
        "assets/buttons/begin.png").convert_alpha()
    restart_image = pygame.image.load(
        "assets/buttons/restart.png").convert_alpha()
    restart_image = pygame.transform.scale(restart_image, (170, 40))
    fast_forward_image = pygame.image.load(
        "assets/buttons/fast_forward.png").convert_alpha()

    #gui
    coin_image = pygame.image.load("assets/gui/coin.png").convert_alpha()
    coin_image = pygame.transform.scale(coin_image, (24, 24))
    heart_image = pygame.image.load("assets/gui/heart.png").convert_alpha()
    side_panel_bg = pygame.image.load("assets/gui/side_panel.png").convert_alpha()
    game_over_img = pygame.image.load("assets/gui/game_over.png").convert_alpha()
        
    #shot effects 
    shot_fx = pygame.mixer.Sound("assets/audio/shot.wav")
    shot_fx.set_volume(0.5)
    # json
    with open('levels/waypoint.tmj') as file:
        world_data = json.load(file)
    #display text
    ps_font = "assets/fonts/press_start.ttf"
    ka_font = "assets/fonts/ka1.ttf"

    text_font = pygame.font.Font(ps_font, 14)
    level_font = pygame.font.Font(ps_font, 25)
    

    def draw_text(text, font, text_color, x, y):
        img = font.render(text, False, text_color)
        game_window.blit(img, (x, y)) 

    def display_data():

        game_window.blit(side_panel_bg, (const.SCREEN_WIDTH, 0))
        #display data 
        draw_text("LEVEL: " + str(world.level), level_font, 'white', const.SCREEN_WIDTH + 43, 55)
        game_window.blit(heart_image, (const.SCREEN_WIDTH + 32, 127))
        draw_text(str(world.health), text_font, 'white', const.SCREEN_WIDTH + 72, 137)
        game_window.blit(coin_image,(const.SCREEN_WIDTH + 36, 160))
        draw_text(str(world.coins), text_font, 'white',const.SCREEN_WIDTH + 72, 165)
    

    def create_turret(mouse_pos):
        mouse_tile_x = mouse_pos[0] // const.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // const.TILE_SIZE
        mouse_tile_num = (mouse_tile_y * const.COLUMS) + mouse_tile_x
        if world.tile_map[mouse_tile_num] == 1:
            space_is_free = True
            for turret in turret_group:
                if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                    space_is_free = False

            if space_is_free == True:
                plc_fx.play()
                new_turret = Turret(turret_spritesheets,
                                    mouse_tile_x, mouse_tile_y, shot_fx)
                turret_group.add(new_turret)
                world.coins -= const.BUY_COST


    def select_turret(mouse_pos):
        mouse_tile_x = mouse_pos[0] // const.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // const.TILE_SIZE
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                return turret
    
    def is_button_held(button_rect):
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        return button_rect.collidepoint(mouse_pos) and mouse_pressed[0]


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

    # button
    turret_button = Button(const.SCREEN_WIDTH + 57, 260, buy_turret_image, True)
    cancel_button = Button(const.SCREEN_WIDTH + 57, 320, cancel_turret_image, True)
    upgrade_button = Button(const.SCREEN_WIDTH + 57, 320,
                            upgrade_turret_image, True)
    begin_button = Button(const.SCREEN_WIDTH + 57, 420,
                            begin_image, True)
    restart_button = Button(315, 310,
                            restart_image, True)
    fast_forward_button = Button(const.SCREEN_WIDTH + 57, 420,
                            fast_forward_image, False)


    while game_active:
        game_clock.tick(const.FPS)
        world.draw(game_window)

        keys = pygame.key.get_pressed()

        # Draw
        enemy_group.draw(game_window)
        for turret in turret_group:
            turret.draw(game_window)

        display_data()
        
        
        # Draw Buttons
        #for the "turret button" show cost of turret and draw the button 
        #draw_text(str(const.BUY_COST), text_font, 'blue', const.SCREEN_WIDTH + 215, 135)
        #game_window.blit(coin_image,(const.SCREEN_WIDTH + 260, 130))
        
        if turret_button.draw(game_window):
            click_fx.play()
            placing_turrets = True
        if placing_turrets == True:
            draw_text(str(f'COST:{const.BUY_COST}'), text_font, "#FFFFFF", const.SCREEN_WIDTH + 87, 232)
            game_window.blit(coin_image,(const.SCREEN_WIDTH + 202, 228))

            cursor_rect = cursor_turret.get_rect()
            cursor_pos = pygame.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= const.SCREEN_WIDTH:
                game_window.blit(cursor_turret, cursor_rect)
            if cancel_button.draw(game_window):
                click_fx.play()
                placing_turrets = False
        # if turret selected, show button
        if selected_turret:
            draw_text(str(f'COST:{const.UPGRADE_COST:}'), text_font, "#FFFFFF", const.SCREEN_WIDTH + 87, 378)
            game_window.blit(coin_image,(const.SCREEN_WIDTH + 202, 375))
            if selected_turret.upgrade_level < const.TURRET_LEVEL:
                if upgrade_button.draw(game_window):
                    click_fx.play()
                    if world.coins >= const.UPGRADE_COST:
                        selected_turret.upgrade()
                        world.coins -= const.UPGRADE_COST
                        upg_fx.play()
        if game_over == False:
            #check if player lost
            if world.health  <= 0:
                game_over = True
                game_outcome = -1 #lost
                gm_ovr_fx.play()

        #  Check win condition after finishing a level
            if world.level > const.TOTAL_LEVEL:
                world.level -= 1
                game_over = True
                game_outcome = 1  # win



            # update group
            enemy_group.update(world)
            turret_group.update(enemy_group, world)

            # higlight selected turret
            if selected_turret:
                selected_turret.selected = True
        
        if game_over == False:
        #check if the level has started o not 
            if level_started == False:
                if begin_button.draw(game_window):
                    click_fx.play()
                    level_started = True
            else:
            # fast forward option
                world.game_speed = 1
                if fast_forward_button.draw(game_window) or keys[pygame.K_SPACE]:
                    world.game_speed = 2
                    
                    
            # spawn enemies
                if pygame.time.get_ticks() - last_enemy_spawn > const.SPAWN_COOLDOWN:
                    if world.spawned_enemies < len(world.enemy_list):
                        enemy_type = world.enemy_list[world.spawned_enemies]
                        enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                        enemy_group.add(enemy)
                        world.spawned_enemies += 1
                        last_enemy_spawn = pygame.time.get_ticks()


            #check if the wave is finished 
            if world.check_level_complete() == True:
                #world.coins += const.LEVEL_COMPLETE_REWARD 
                world.level += 1
                level_started = False
                last_enemy_spawn = pygame.time.get_ticks()
                world.reset_level()
                world.process_enemies()
                
            # enemy path
           # if len(world.waypoints) >= 2:
               # pygame.draw.lines(game_window, 'Yellow', False, world.waypoints)
        else: 
            game_window.blit(game_over_img, (200, 200))
                #restart level 
            if restart_button.draw(game_window):
                click_fx.play()
                game_over = False
                level_started = False
                placing_turrets = False
                selected_turret = None
                last_enemy_spawn = pygame.time.get_ticks()
                world = World(world_data, world_surf)
                world.process_data()
                world.process_enemies()
                # empty group
                enemy_group.empty()
                turret_group.empty()


    #  at the bottom of the main loop 
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                game_active = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] < const.SCREEN_WIDTH and mouse_pos[1] < const.SCREEN_HEIGHT:
                    selected_turret = None
                    clear_selection()
                    if placing_turrets and world.coins >= const.BUY_COST:
                        create_turret(mouse_pos)
                    else:
                        selected_turret = select_turret(mouse_pos)

        pygame.display.flip()

    pygame.quit()
    
        