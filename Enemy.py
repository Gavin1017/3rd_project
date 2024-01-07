import pygame
import random
from pygame.locals import *
import sys
from noise import snoise2
import numpy as np
import cv2
import math


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # self.size = 20
        self.health = 100  # 假设敌人有100点生命值
        self.defence = 2
        self.attack = 10
        self.pic = pygame.image.load("picture\\player.png")
        self.rect = self.pic.get_rect()

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
