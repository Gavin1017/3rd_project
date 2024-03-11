import pygame
import random
from pygame.locals import *
import sys
from noise import snoise2
import numpy as np
import cv2
import math
from scipy.ndimage import label, find_objects
from skimage.graph import route_through_array
from Player import *
from Bullet import *
from Enemy import *
from Map import *
import Map_Maze
import Map_Cave
import random
import Astar

# 写一个三维numpy，前两维是长和宽，第三维是信息（列如炸弹，）



width, height = 1200, 800

cell_size = 15
cols, rows = width // cell_size, height // cell_size # cols=80, rows = 60
cave_time = 0

bomb_list = []
fire_list = []
cave_enemy_list = []


#没有用
cave_surface = ""
enemy=[]

# 控制键设置
key_settings = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d
}
thecave = Map_Cave.Cave(width, height, cell_size, enemy)
thecave.initial()
thecave.cellular_automaton(5) # step of the cellular automaton
thecave.final_map(10) # the threshold of the area
thecave.connect_components()
thecave.block()

cave_position = Map_Cave.find_init_position(thecave.unconnected_cave)
cave_player = Map_Cave.Player(cave_position[1], thecave.matrix, cell_size, cave_surface, cell_size)
enemy_position_values = list(cave_position.values())[1:]
cave_enemy_list_pos = random.choices(enemy_position_values, k=1)
for enemy_pos in cave_enemy_list_pos:
    cave_enemy_list.append(Map_Cave.Enemy(enemy_pos, thecave.matrix, cell_size, cave_surface, cell_size))

print(type(thecave.matrix))

print(cave_enemy_list[0].position)
print(thecave.matrix[cave_enemy_list[0].position[0], cave_enemy_list[0].position[1]]) # 敌人所在的位置
