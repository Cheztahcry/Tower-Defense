import pygame
import time
import sys
import main

pygame.init()
pygame.mixer.init()

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1020
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("LockDown-Defense")
clock = pygame.time.Clock()
icn = pygame.image.load("assets/bg_image/turret_icon.png").convert_alpha()
pygame.display.set_icon(icn)

pygame.mixer.music.load("assets/audio/load_music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

play_btn_img = pygame.image.load("assets/bg_image/play button.png").convert_alpha()
resized_image = pygame.transform.scale(play_btn_img, (100, 75))
play_button_rect = resized_image.get_rect(bottomright=(1010, 725))
play_button_trans = 0

slime_ss = pygame.image.load("assets/bg_image/slime.png").convert_alpha()
frame_width = slime_ss.get_width() // 4
frame_height = slime_ss.get_height()

scale = 1.5
frames = []
for i in range(4):
    frame = slime_ss.subsurface((i * frame_width, 0, frame_width, frame_height))
    scaled_frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
    frames.append(scaled_frame)

frame_index = 0
frame_timer = 0
frame_speed = 0.1

bg = pygame.image.load("assets/bg_image/CHESTER_DF.jpg").convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.SysFont("Arial", 17)


for i in range(101):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            

    dt = clock.tick(60) / 1000
    frame_timer += dt
    if frame_timer >= frame_speed:
        frame_timer = 0
        frame_index = (frame_index + 1) % len(frames)

    screen.blit(bg, (0, 0))

    loading_text = font.render(f"Loading: {i}%", True, (139, 255, 255))
    screen.blit(loading_text, (920, 690))
    screen.blit(frames[frame_index], (915, 615))

    pygame.display.flip()
    time.sleep(0.08)

def draw_play_button():
    global play_button_trans

    if play_button_trans < 255:
        play_button_trans += 5  
        play_button_trans = min(play_button_trans, 255)

    temp_image = resized_image.copy()
    temp_image.set_alpha(play_button_trans)
    screen.blit(temp_image, play_button_rect)


#Main Loop
running = True
loading_complete = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if play_button_rect.collidepoint(event.pos) and play_button_trans == 255:
                pygame.quit()
                import main
                main.start_game()
                sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and play_button_trans == 255:
                pygame.quit()
                import main
                main.start_game()
                sys.exit()

    screen.blit(bg, (0, 0))

    if loading_complete:
        draw_play_button()

    pygame.display.flip()
    clock.tick(60)


