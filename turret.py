import pygame
import constants as const


class Turret(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, tile_x, tile_y):
        pygame.sprite.Sprite.__init__(self)
        self.cooldown = 1000
        self.last_shot = pygame.time.get_ticks()

        self.tile_x = tile_x
        self.tile_y = tile_y

        self.x = (self.tile_x + 0.5) * const.TILE_SIZE
        self.y = (self.tile_y + 0.5) * const.TILE_SIZE

        # animation var
        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # update image

        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def load_images(self):
        size = self.sprite_sheet.get_height()
        animation_list = []
        for x in range(const.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(x * size, 0,  size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self):
        if pygame.time.get_ticks() - self.last_shot > self.cooldown:
            self.play_animation()

    def play_animation(self):
        # update
        self.image = self.animation_list[self.frame_index]
        # check time passed
        if pygame.time.get_ticks() - self.update_time > const.ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                self.last_shot = pygame.time.get_ticks()
