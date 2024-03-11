import pygame
import random
from pygame.locals import *
import sys
from noise import snoise2
import numpy as np
import cv2
import math


class Bullet:
    def __init__(self, x, y, angle, owner):
        self.x = x
        self.y = y
        self.angle = angle
        self.radius = 5
        self.speed = 5
        self.range = 300
        self.distance = 0
        self.owner = owner

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.distance += self.speed  # 更新移动距离

    def is_out_of_range(self):
        return self.distance >= self.range

    def draw(self, the_screen):
        pygame.draw.circle(the_screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius)

    def change_radius(self, value):
        self.radius = value

    def change_speed(self, value):
        self.speed = value

    def change_range(self, value):
        self.range = value
