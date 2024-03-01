import pygame
import random
from pygame.locals import *
import sys
from noise import snoise2
import numpy as np
import cv2
import math


class Player:
    def __init__(self, the_width, the_height):
        self.position = [random.randint(0, 800), random.randint(0, 600)]
        self.width = the_width
        self.height = the_height
        # self.position = [300, 400]
        self.speed = 5
        self.pic = pygame.image.load("picture\\player.png")
        self.rect = self.pic.get_rect()
        self.left_available = True
        self.right_available = True
        self.top_available = True
        self.down_available = True
        self.left_pic = pygame.image.load("picture\\player_left.png")
        self.right_pic = pygame.image.load("picture\\player_right.png")
        self.top_pic = pygame.image.load("picture\\player_top.png")
        self.down_pic = pygame.image.load("picture\\player_down.png")
        self.shoot_direction = 0

        self.attack = 10  # 基础攻击
        self.defense = 2  # 基础防御
        self.hp = 100
        self.equipments = []

        # self.bullet = bullet

    def move(self, keyup):
        kp = pygame.key.get_pressed()
        # print(self.rect)
        # print(self.position)
        if kp[pygame.K_a] and self.left_available:
            self.position[0] = self.position[0] - self.speed
        if kp[pygame.K_d] and self.right_available:
            self.position[0] = self.position[0] + self.speed
        if kp[pygame.K_s] and self.down_available:
            self.position[1] = self.position[1] + self.speed
        if kp[pygame.K_w] and self.top_available:
            self.position[1] = self.position[1] - self.speed

        if self.position[1] - self.rect.bottom / 2 <= 0:  # top
            self.top_available = False
        else:
            self.top_available = True
        if self.position[1] + self.rect.bottom / 2 >= self.height:  # down
            self.down_available = False
        else:
            self.down_available = True
        if self.position[0] - self.rect.right / 2 <= 0:  # left
            self.left_available = False
        else:
            self.left_available = True
        if self.position[0] + self.rect.right / 2 >= self.width:  # Right
            self.right_available = False
        else:
            self.right_available = True

    def shooting_direction(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.shoot_direction = math.atan2(mouse_y - self.position[1], mouse_x - self.position[0])
        if -(math.pi / 4) <= self.shoot_direction <= (math.pi / 4):
            self.pic = self.right_pic
            self.rect = self.pic.get_rect()
        if (math.pi / 4) <= self.shoot_direction <= (3 * math.pi / 4):
            self.pic = self.down_pic
            self.rect = self.pic.get_rect()
        if (3 * math.pi / 4) <= self.shoot_direction <= math.pi or -math.pi <= self.shoot_direction <= -(
                3 * math.pi / 4):
            self.pic = self.left_pic
            self.rect = self.pic.get_rect()
        if -(3 * math.pi / 4) <= self.shoot_direction <= -(math.pi / 4):
            self.pic = self.top_pic
            self.rect = self.pic.get_rect()

    def calculate_attribute(self):
        for equipment in self.equipments:
            self.attack += equipment.attack
            self.defense += equipment.defense

    # def check_collision(self, the_enemy):
    #     enemy_rect = pygame.Rect(the_enemy.x - the_enemy.rect.right / 2, the_enemy.y - the_enemy.rect.bottom / 2,
    #                              the_enemy.rect.right,the_enemy.rect.bottom)
    #     player_rect = pygame.Rect(self.position[0] - self.rect.right / 2, self.position[1] - self.rect.bottom / 2,
    #                               self.rect.right,self.rect.bottom)
    #     return player_rect.colliderect(enemy_rect)
