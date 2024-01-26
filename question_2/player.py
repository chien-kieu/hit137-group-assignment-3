import pygame
import os

class Player:
    def __init__(self, x, y, width, height):
        self.idle_left_animation_images = [pygame.image.load(os.path.join('images', f'idle_left_{i}.png')) for i in
                                           range(1, 10)]
        self.idle_right_animation_images = [pygame.transform.flip(image, True, False) for image in self.idle_left_animation_images]
        self.last_direction = 1  # Hướng cuối cùng
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.can_shoot = True
        self.health = 100
        self.lives = 3
        self.collision_timer = 0
        self.collision_cooldown = 0.5
        self.collision_cooldown_timer = 0
        self.current_frame = 0

    def handle_collision(self, fps):
        if self.collision_timer <= 0:
            self.update_health(10)
            self.collision_timer = 0.5
        else:
            self.collision_timer -= 1 / fps

    def move_left(self):
        self.x -= self.vel

    def move_right(self, win_width):
        self.x += self.vel
        if self.x > win_width - self.width:
            self.x = win_width - self.width

    def jump(self):
        if not self.isJump:
            self.isJump = True

    def handle_jump(self):
        if self.jumpCount >= -10:
            neg = 1
            if self.jumpCount < 0:
                neg = -1
            self.y -= (self.jumpCount ** 2) * 0.5 * neg
            self.jumpCount -= 1
        else:
            self.isJump = False
            self.jumpCount = 10

    def update_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.lives -= 1
            if self.lives > 0:
                self.health = 100
            else:
                pygame.quit()
                exit()

    def draw(self, win, animation_images):
        flipped_image = pygame.transform.flip(animation_images[self.current_frame], self.direction == -1, False)
        win.blit(flipped_image, (self.x, self.y))

    def update(self, win_width, keys):
        self.update_animation(keys)

        if keys[pygame.K_LEFT]:
            self.move_left()

        if keys[pygame.K_RIGHT]:
            self.move_right(win_width)

        if keys[pygame.K_UP]:
            self.jump()

        if self.isJump:
            self.handle_jump()
