# Trong file projectile.py

import pygame
import os

class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y - 5
        self.direction = 1
        self.vel = 7 * direction
        self.width = 10
        self.height = 10
        self.images = [pygame.image.load(os.path.join('images', f'bullet_{i}.png')) for i in range(1, 6)]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def update_image(self):
        self.image_index = (self.image_index + 1) % len(self.images)
        self.image = self.images[self.image_index]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))