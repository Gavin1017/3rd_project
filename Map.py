import pygame
import random
from pygame.locals import *
import sys
from noise import snoise2
import numpy as np
import cv2
import math


class Map:
    def __init__(self, the_width, the_height):
        self.width = the_width
        self.height = the_height
        self.cell_map = [[0 for y in range(the_width)] for x in range(the_height)]  # 地形
        self.map_color = [[0 for y in range(the_width)] for x in range(the_height)]  # 地形颜色
        self.river = 0
        self.land = 1
        self.mountain = 2
        self.change = 4

    def generate_noise_map(self, map_width, map_height, scale, octaves, persistence, lacunarity, seed):
        noise_map = [[0 for y in range(map_width)] for x in range(map_height)]
        for x in range(map_height):
            for y in range(map_width):
                sample_x = x / scale
                sample_y = y / scale
                value = snoise2(sample_x, sample_y, octaves=octaves, persistence=persistence,
                                lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=seed)
                noise_map[x][y] = value
        return noise_map

    def delete_small(self, cellmap, mapcolor):
        #  判断cell_map上下左右来决定对应的颜色
        for x in range(len(cellmap)):
            for y in range(len(cellmap[0])):
                if (x >= 5 and y >= 5) and (x <= len(cellmap) - 6 and y >= 5) and (
                        x >= 5 and y <= len(cellmap[0]) - 6) and (
                        x <= len(cellmap) - 6 and y <= len(cellmap[0]) - 6):
                    if cellmap[x][y] == self.change or cellmap[x][y] == self.river:
                        if cellmap[x - 5][y - 5] == self.land and cellmap[x - 5][y - 4] == self.land and cellmap[x - 5][
                            y - 3] == self.land and (
                                cellmap[x - 5][y - 2] == self.land) and cellmap[x - 5][y - 1] == self.land and \
                                cellmap[x - 5][
                                    y] == self.land and (
                                cellmap[x - 5][y + 1] == self.land) and cellmap[x - 5][y + 2] == self.land and \
                                cellmap[x - 5][
                                    y + 3] == self.land and (
                                cellmap[x - 5][y + 4] == self.land) and cellmap[x - 5][y + 5] == self.land and \
                                cellmap[x - 4][
                                    y - 5] == self.land and (
                                cellmap[x - 3][y - 5] == self.land) and cellmap[x - 2][y - 5] == self.land and \
                                cellmap[x - 1][
                                    y - 5] == self.land and (
                                cellmap[x][y - 5] == self.land) and cellmap[x + 1][y - 5] == self.land and \
                                cellmap[x + 2][
                                    y - 5] == self.land and (
                                cellmap[x + 3][y - 5] == self.land) and cellmap[x + 4][y - 5] == self.land and \
                                cellmap[x + 5][
                                    y - 5] == self.land and (
                                cellmap[x - 4][y + 5] == self.land) and cellmap[x - 3][y + 5] == self.land and \
                                cellmap[x - 2][
                                    y + 5] == self.land and cellmap[x - 1][y + 5] == self.land and (
                                cellmap[x][y + 5] == self.land) and cellmap[x + 1][y + 5] == self.land and \
                                cellmap[x + 2][
                                    y + 5] == self.land and (
                                cellmap[x + 3][y + 5] == self.land) and cellmap[x + 4][y + 5] == self.land and \
                                cellmap[x + 5][
                                    y + 5] == self.land and (
                                cellmap[x + 5][y - 5] == self.land) and cellmap[x + 5][y - 4] == self.land and \
                                cellmap[x + 5][
                                    y - 3] == self.land and (
                                cellmap[x + 5][y - 2] == self.land) and cellmap[x + 5][y - 1] == self.land and \
                                cellmap[x + 5][
                                    y] == self.land and (
                                cellmap[x + 5][y + 1] == self.land) and cellmap[x + 5][y + 2] == self.land and \
                                cellmap[x + 5][
                                    y + 3] == self.land and (
                                cellmap[x + 5][y + 4] == self.land):
                            mapcolor[x][y] = (255, 255, 255)

    def render_map(self, noise_map, river_threshold, land_threshold, mountain_threshold):
        for x in range(len(noise_map)):
            for y in range(len(noise_map[0])):
                # color = (int(255 * (noise_map[x][y] + 1) / 2),) * 3
                value = noise_map[x][y]
                if value < river_threshold:
                    color = (0, 0, 255)  # Blue for rivers
                    self.cell_map[x][y] = self.river
                    self.map_color[x][y] = color
                elif value < land_threshold:
                    color = (255, 255, 255)  # White for land
                    self.cell_map[x][y] = self.land
                    self.map_color[x][y] = color
                elif value < mountain_threshold:
                    t = (value - land_threshold) / (mountain_threshold - land_threshold)
                    # print(t)
                    color = (139 * t, 69 * t, 19 * t)  # Smooth transition from white to brown
                    self.cell_map[x][y] = self.change
                    self.map_color[x][y] = color
                else:
                    color = (139, 69, 19)
                    self.cell_map[x][y] = self.mountain
                    self.map_color[x][y] = color

        self.delete_small(self.cell_map, self.map_color)

        map_color_bgr = np.array(self.map_color, dtype=np.uint8)[:, :, ::-1]
        cv2.imwrite("picture\map.jpg", map_color_bgr)
