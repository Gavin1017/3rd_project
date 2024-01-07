import pygame
import random
from pygame.locals import *
import sys
from noise import snoise2
import numpy as np
import cv2
import math
from Player import *
from Bullet import *
from Enemy import *
from Map import *

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PCG Game")
clock = pygame.time.Clock()

init_surface = pygame.Surface(screen.get_size())
init_surface.fill((255, 255, 255))
main_surface = pygame.Surface(screen.get_size())

# init_surface.fill((255,255,255))


def main():
    # 地图参数
    scale = 150
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0
    seed = random.randint(0, 100)

    the_river_threshold = -0.2  # 用于分类河流的阈值
    the_land_threshold = 0.0  # 用于分类陆地的阈值
    the_mountain_threshold = 0.2  # 用于分类高山的阈值
    noise_map = []

    # 绘制地图
    the_map = Map(width, height)
    noise_map = the_map.generate_noise_map(width, height, scale, octaves, persistence, lacunarity, seed)
    the_map.render_map(noise_map, the_river_threshold, the_land_threshold, the_mountain_threshold)
    map = pygame.image.load("picture\map.jpg")

    # 生成玩家和子弹
    # player_bullet = Bullet()
    player = Player(width, height)
    keydown = ""
    keyup = ""
    player_bullets = []

    # 生成一些敌人
    enemies = [Enemy(100, 100), Enemy(200, 200)]

    # 特定事件
    special_event_triggered = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 1:  # 检测左键点击
            #         mouse_x, mouse_y = pygame.mouse.get_pos()
            #         print(f"Left mouse button clicked at ({mouse_x}, {mouse_y})")
            if event.type == KEYDOWN:
                keydown = event.key
            else:
                keydown = None
            if event.type == KEYUP:
                keyup = event.key
            else:
                keyup = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.atan2(mouse_y - player.position[1], mouse_x - player.position[0])
                player_bullets.append(Bullet(player.position[0], player.position[1], angle))
            # 按下空格键触发特定事件
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                special_event_triggered = True
        # 如果特定事件被触发，改变所有子弹的属性
        if special_event_triggered:
            for bullet in player_bullets:
                bullet.change_speed(5)  # 增加速度
                bullet.change_radius(10)  # 增加半径

        # 判断玩家移动
        player.move(keyup)
        player.shooting_direction()

        # 更新子弹
        for bullet in player_bullets[:]:
            bullet.update()
            if bullet.is_out_of_range():
                player_bullets.remove(bullet)

        # 检测敌人和子弹的碰撞
        for bullet in player_bullets[:]:
            for enemy in enemies[:]:
                if enemy.check_collision(bullet):
                    player_bullets.remove(bullet)
                    if enemy.hit(player.attack):  # 如果敌人被击败
                        enemies.remove(enemy)

        main_surface.fill((0, 0, 0))
        main_surface.blit(map, (0, 0))
        main_surface.blit(player.pic,
                          (player.position[0] - player.rect.right / 2, player.position[1] - player.rect.bottom / 2))
        #
        # main_surface.blit(pygame.transform.smoothscale(player.pic, (int(player.rect[2]), int(player.rect[3]))),
        #             (player.position[0] - player.rect.right / 2, player.position[1] - player.rect.bottom / 2))  # 放大或者缩小
        # 绘制子弹
        for bullet in player_bullets:
            bullet.draw(main_surface)
        # 绘制敌人
        for enemy in enemies:
            main_surface.blit(enemy.pic,
                              (enemy.x - enemy.rect.right / 2, enemy.y - enemy.rect.bottom / 2))
            # main_surface.blit(pygame.transform.smoothscale(enemy.pic, (int(enemy.rect[2]/3), int(enemy.rect[3]/3))),
            #             (enemy.x - enemy.rect.right / 2,
            #              enemy.y - enemy.rect.bottom / 2))  # 放大或者缩小
            # enemy.draw(main_surface)
        # print((enemies[0].x - enemies[0].rect.right / 2, enemies[0].y - enemies[0].rect.bottom / 2))
        screen.blit(main_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    # exit()


def init():
    start_game = True
    start = pygame.image.load("picture\\start.png")
    finish = pygame.image.load("picture\\finish.png")
    start_r = pygame.image.load("picture\\start_r.png")
    finish_r = pygame.image.load("picture\\finish_r.png")
    while start_game:
        clock.tick(60)
        buttons = pygame.mouse.get_pressed()
        x1, y1 = pygame.mouse.get_pos()
        if width * (3 / 8) <= x1 <= width * (5 / 8) and height * (5 / 10) <= y1 <= height * (6 / 10):
            init_surface.blit(start_r, (width * (3 / 8), height * (5 / 10)))
            if buttons[0]:
                start_game = False
        elif width * (3 / 8) <= x1 <= width * (5 / 8) and height * (7 / 10) <= y1 <= height * (8 / 10):
            init_surface.blit(finish_r, (width * (3 / 8), height * (7 / 10)))
            if buttons[0]:
                pygame.quit()
                exit()
        else:
            init_surface.blit(start, (width * (3 / 8), height * (5 / 10)))
            init_surface.blit(finish, (width * (3 / 8), height * (7 / 10)))

        screen.blit(init_surface, (0, 0))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


if __name__ == "__main__":
    init()
    main()
