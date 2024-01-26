# Trong file enemy.py

import pygame
import os
import random

class Enemy:
    def __init__(self, x, y, width, height, health, move_speed):
        self.direction = 1  # Mặc định hướng ban đầu là về bên phải (1)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.vel = move_speed
        self.walk_right_animation_images = [pygame.image.load(os.path.join('images', f'enemy_walk_right_{i}.png')) for i in range(1, 4)]
        self.walk_left_animation_images = [pygame.image.load(os.path.join('images', f'enemy_walk_left_{i}.png')) for i in range(1, 4)]
        self.enemy_appear_images = [pygame.image.load(os.path.join('images', f'enemy_appear_{i}.png')) for i in range(1, 11)]
        self.walk_animation_index = 0
        self.walk_animation_speed = 7
        self.walk_animation_counter = 0
        self.enemy_appear_speed = 3
        self.enemy_appear_index = 0
        self.enemy_appear_counter = 0
        self.image = self.enemy_appear_images[self.enemy_appear_index]  # Bắt đầu với hình ảnh xuất hiện
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.is_dead = False
        self.appear_done = False  # Thêm một biến để kiểm tra xem hiệu ứng appear đã hoàn thành chưa

    def update_direction(self, player_x):
        if self.x < player_x:
            self.direction = 1  # Nếu nhân vật ở bên phải, đặt hướng về bên phải
        else:
            self.direction = -1  # Ngược lại, đặt hướng về bên trái

    def update_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.is_dead = True

    def appear(self):
        if not self.appear_done:
            self.image = self.enemy_appear_images[self.enemy_appear_index]
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.enemy_appear_counter += 1
            if self.enemy_appear_counter % self.enemy_appear_speed == 0:
                self.enemy_appear_index = (self.enemy_appear_index + 1) % len(self.enemy_appear_images)
                if self.enemy_appear_index == 0:
                    self.appear_done = True  # Hiệu ứng appear hoàn thành khi index về 0

    def move(self):
        if not self.is_dead and self.appear_done:  # Chỉ di chuyển khi hiệu ứng appear hoàn thành
            self.x += self.vel * self.direction  # Di chuyển theo hướng

            if self.direction == 1:
                self.image = self.walk_right_animation_images[self.walk_animation_index]
            else:
                self.image = self.walk_left_animation_images[self.walk_animation_index]

            self.image = pygame.transform.scale(self.image, (self.width, self.height))

            self.walk_animation_counter += 1
            if self.walk_animation_counter % self.walk_animation_speed == 0:
                self.walk_animation_index = (self.walk_animation_index + 1) % len(self.walk_right_animation_images)

    def calculate_die_frame(self):
        die_frame = self.walk_right_animation_images[self.walk_animation_index]
        die_frame = pygame.transform.scale(die_frame, (self.width, self.height))
        return die_frame

    @classmethod
    def create_random_enemy(cls, win_width, win_height):
        x = win_width
        y = random.randint(50, win_height - 50)
        width = 35
        height = 35
        health = 50
        move_speed = random.uniform(1, 4)
        return cls(x, y, width, height, health, move_speed)
