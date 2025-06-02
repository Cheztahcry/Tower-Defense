import pygame
import math
from pygame.math import Vector2
from enemy_data import ENEMY_DATA
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, waypoints, images):
        pygame.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.position = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.health = ENEMY_DATA.get(enemy_type)['health']
        self.speed = ENEMY_DATA.get(enemy_type)['speed']
        self.angle = 0
        self.orig_image = images.get(enemy_type)
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def movement(self):
        #target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.move = self.target - self.position
        else:
            self.kill()

        #calculate distance to waypoint 
        distance = self.move.length()
        if distance >= self.speed:
            self.position += self.move.normalize() * self.speed
        else:
            if distance != 0:
                self.position += self.move.normalize() * distance
            self.target_waypoint += 1

        

    def rotate(self):
        distance =  self.target - self.position

        #calculate distance
        self.angle = math.degrees(math.atan2(-distance[1], distance[0]))

        #rotate image and rect
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


 

    def update(self):
        
        self.movement()
        self.rotate()