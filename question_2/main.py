import pygame
import os
from player import Player
from enemy import Enemy
from projectile import Projectile
import random

pygame.init()

win_width, win_height = 640, 360
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Running, Jumping, Backing, and Idling Character")

run_animation_images = [pygame.image.load(os.path.join('images', f'running_{i}.png')) for i in range(1, 10)]
back_animation_images = [pygame.transform.flip(image, True, False) for image in run_animation_images]
jump_animation_images = [pygame.image.load(os.path.join('images', f'jump_{i}.png')) for i in range(1, 14)]
jump_back_animation_images = [pygame.transform.flip(image, True, False) for image in jump_animation_images]
idle_animation_images = [pygame.image.load(os.path.join('images', f'idle_{i}.png')) for i in range(1, 10)]
idle_left_animation_images = [pygame.transform.flip(image, True, False) for image in idle_animation_images]
shoot_animation_images = [pygame.image.load(os.path.join('images', f'shoot_{i}.png')) for i in range(1, 4)]
shoot_left_animation_images = [pygame.transform.flip(image, True, False) for image in shoot_animation_images]

life_image = pygame.image.load(os.path.join('images', "lives.png"))
life_image = pygame.transform.scale(life_image, (37, 50))

current_frame = 0

player = Player(50, 250, 40, 60)
projectiles = []

background = pygame.image.load(os.path.join('images', "background.webp"))
background = pygame.transform.scale(background, (win_width, win_height))

health_bar_width = 100
health_bar_height = 10
health_bar_color = (0, 255, 0)

life_spacing = 10

clock = pygame.time.Clock()
fps = 20

enemies = []
enemy_spawn_timer = 0
enemy_spawn_delay = random.randint(30, 60)

def spawn_enemy():
    x = random.randint(50, win_width - 50)
    y = win_height - 90
    width = 35
    height = 35
    health = 50
    speed = random.uniform(1, 2)

    enemy = Enemy(x, y, width, height, health, speed)
    enemy.player_x = player.x
    enemies.append(enemy)

run = True

while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    win.blit(background, (0, 0))

    projectiles = [projectile for projectile in projectiles if 0 < projectile.x < win_width]

    for enemy in enemies:
        if not enemy.is_dead:
            enemy.update_direction(player.x)
            enemy.appear()
            enemy.move()
            if enemy.appear_done:
                pygame.draw.rect(win, (0, 0, 255), (enemy.x, enemy.y - 10, enemy.width, 5))
                pygame.draw.rect(win, (255, 0, 0), (enemy.x, enemy.y - 10, max(0, enemy.health), 5))
                pygame.draw.rect(win, (0, 255, 0), (enemy.x, enemy.y - 10, max(0, enemy.health), 5))
            win.blit(enemy.image, (enemy.x, enemy.y))

    for enemy in enemies:
        if (
                enemy.appear_done
                and not enemy.is_dead
                and player.x < enemy.x + enemy.width
                and player.x + player.width > enemy.x
                and player.y < enemy.y + enemy.height
                and player.y + player.height > enemy.y
        ):
            player.handle_collision(fps)

    for projectile in projectiles:
        if projectile.direction == 1:
            projectile.x += projectile.vel
        else:
            projectile.x -= projectile.vel
        projectile.update_image()
        win.blit(projectile.image, (projectile.x, projectile.y))

        for enemy in enemies:
            if (
                enemy.appear_done
                and not enemy.is_dead
                and enemy.x < projectile.x < enemy.x + enemy.width
                and enemy.y < projectile.y < enemy.y + enemy.height
            ):
                enemy.update_health(10)
                if enemy.health <= 0:
                    enemy.is_dead = True

                if projectile in projectiles:
                    projectiles.remove(projectile)

    if keys[pygame.K_LEFT]:
        player.move_left()

    if keys[pygame.K_RIGHT]:
        player.move_right(win_width)

    if keys[pygame.K_UP]:
        player.jump()

    if keys[pygame.K_SPACE] and player.can_shoot:
        direction = player.last_direction
        projectiles.append(Projectile(player.x + player.width // 2, player.y + player.height // 2, direction))
        player.can_shoot = False

    if not keys[pygame.K_SPACE]:
        player.can_shoot = True

    if player.isJump:
        player.handle_jump()

    if keys[pygame.K_RIGHT] and not player.isJump:
        player.last_direction = 1
        if keys[pygame.K_SPACE]:
            current_frame = (current_frame  + 1) % len(shoot_animation_images)
            win.blit(shoot_animation_images[current_frame], (player.x, player.y))
        else:
            win.blit(run_animation_images[current_frame], (player.x, player.y))
    elif keys[pygame.K_LEFT] and not player.isJump:
        player.last_direction = -1
        if keys[pygame.K_SPACE]:
            current_frame = (current_frame ) % len(shoot_left_animation_images)
            win.blit(shoot_left_animation_images[current_frame], (player.x, player.y))
        else:
            win.blit(back_animation_images[current_frame], (player.x, player.y))
    elif keys[pygame.K_RIGHT] and player.isJump:
        player.last_direction = 1
        win.blit(jump_animation_images[current_frame], (player.x, player.y))
    elif keys[pygame.K_LEFT] and player.isJump:
        player.last_direction = -1
        win.blit(jump_back_animation_images[current_frame], (player.x, player.y))
    elif player.isJump:
        if player.last_direction == 1:
            win.blit(jump_animation_images[current_frame], (player.x, player.y))
        else:
            win.blit(jump_back_animation_images[current_frame], (player.x, player.y))
    else:
        if keys[pygame.K_SPACE]:
            current_frame = (current_frame + 1) % len(shoot_animation_images)
            if player.last_direction == 1:
                win.blit  (shoot_animation_images[current_frame], (player.x, player.y))
            else:
                win.blit(shoot_left_animation_images[current_frame], (player.x, player.y))
        elif player.last_direction == 1:
            win.blit(idle_animation_images[current_frame], (player.x, player.y))
        else:
            win.blit(idle_left_animation_images[current_frame], (player.x, player.y))

    current_frame = (current_frame + 1) % 9

    pygame.draw.rect(win, (255, 0, 0), (10, 10, health_bar_width, health_bar_height))
    pygame.draw.rect(win, health_bar_color, (10, 10, player.health, health_bar_height))

    for i in range(player.lives):
        win.blit(life_image, (win_width - 600 - i * (10 + life_spacing), 10))

    pygame.display.update()

    enemy_spawn_timer += 1
    if enemy_spawn_timer >= enemy_spawn_delay:
        if len(enemies) < 10:
            spawn_enemy()
        enemy_spawn_timer = 0
        enemy_spawn_delay = random.randint(30, 60)

pygame.quit()