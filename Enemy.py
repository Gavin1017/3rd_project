import pygame
import random
from pygame.locals import *
import sys
from noise import snoise2
import numpy as np
import cv2
import math


class Enemy:
    def __init__(self, x, y, append_time):
        self.x = x
        self.y = y
        # self.size = 20
        self.health = 100  # 假设敌人有100点生命值
        self.defence = 2
        self.attack = 10
        self.speed = 2

        self.pic = pygame.image.load("picture\\enemy_down.png")
        self.left_pic = pygame.image.load("picture\\enemy_left.png")
        self.right_pic = pygame.image.load("picture\\enemy_right.png")
        self.top_pic = pygame.image.load("picture\\enemy_top.png")
        self.down_pic = pygame.image.load("picture\\enemy_down.png")

        self.rect = self.pic.get_rect()
        self.append_time = append_time
        self.shooting_time = append_time
        self.moving_time = append_time

        self.direction = random.randint(1, 4)  # 1:up, 2:down, 3:left, 4:right
        self.path = [(j, j) for j in range(100)]
        self.step = 0

    def hit(self, damaged):
        self.health -= damaged - self.defence  # 每次被击中减少10点生命值
        if self.health <= 0:
            return True  # 如果生命值归零，返回True
        return False

    # def draw(self, screen1):
    #     pygame.draw.rect(screen1, (0, 166, 255), (self.x, self.y, self.size, self.size))

    def check_collision(self, bullet):
        # 简单的矩形碰撞检测
        # if self.x < bullet.x < self.x + self.size and self.y < bullet.y < self.y + self.size:
        #     return True
        # return False
        nearest_x = max(self.x - self.rect.right / 2, min(bullet.x, self.x + self.rect.right / 2))
        nearest_y = max(self.y - self.rect.bottom / 2, min(bullet.y, self.y + self.rect.bottom / 2))

        # 计算这个点到圆心的距离
        distance_x = bullet.x - nearest_x
        distance_y = bullet.y - nearest_y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        return distance < bullet.radius

    def random_move(self,  elapsed_time, width, height):
        """1:up, 2:down, 3:left, 4:right"""
        if elapsed_time >= 1000:
            self.direction = random.randint(1, 4)

        if self.direction == 1 and self.y > 0:  # up
            self.pic = self.top_pic
            self.y -= self.speed
        elif self.direction == 2 and self.y < height :  # down
            self.pic = self.down_pic
            self.y += self.speed
        elif self.direction == 3 and self.x > 0:  # left
            self.pic = self.left_pic
            self.x -= self.speed
        elif self.direction == 4 and self.x < width : # right
            self.pic = self.right_pic
            self.x += self.speed

        if self.y <= 0 and self.direction == 1:
            self.direction = 2
        if self.y >= height and self.direction == 2:
            self.direction = 1
        if self.x <= 0 and self.direction == 3:
            self.direction = 4
        if self.x >= width and self.direction == 4:
            self.direction = 3

    # def toward(self):

    def check_enemy_collision(self, next_enemy):
        x1, y1, width1, height1 = self.x, self.y, self.pic.get_width(), self.pic.get_height()
        # 第二个矩形的位置和大小
        x2, y2, width2, height2 = next_enemy.x, next_enemy.y, next_enemy.pic.get_width(), next_enemy.pic.get_height()

        overlap_x = (x1 < x2 + width2) and (x1 + width1 > x2)
        overlap_y = (y1 < y2 + height2) and (y1 + height1 > y2)
        if overlap_x and overlap_y:
            return True
        else:
            return False


    # def a_star_move(self, elapsed_time):
    #     if elapsed_time > 1000:
    #         if self.path[int(self.step) + 1][0] - self.path[int(self.step)][0] > 0:
    #             self.direction = "down"
    #         elif self.path[int(self.step) + 1][0] - self.path[int(self.step)][0] < 0:
    #             self.direction = "up"
    #         elif self.path[int(self.step) + 1][1] - self.path[int(self.step)][1] > 0:
    #             self.direction = "right"
    #         elif self.path[int(self.step) + 1][1] - self.path[int(self.step)][1] < 0:
    #             self.direction = "left"
    #
    #     if self.direction == "down":
    #         self.pic = self.down_pic
    #         self.y += self.speed
    #     elif self.direction == "up":
    #         self.pic = self.down_pic
    #         self.y -= self.speed
    #     elif self.direction == "left":
    #         self.pic = self.down_pic
    #         self.x -= self.speed
    #     elif self.direction == "right":
    #         self.pic = self.down_pic
    #         self.x += self.speed




