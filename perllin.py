import pygame
import random
from pygame.locals import *
import sys
from noise import snoise2
import numpy as np
import cv2
import math

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Perlin Noise Map")
clock = pygame.time.Clock()


class Player:
    def __init__(self, the_width, the_height):
        # self.position = [random.randint(0, 600), random.randint(0, 600)]
        self.width = the_width
        self.height = the_height
        self.position = [300, 400]
        self.speed = 5
        self.pic = pygame.image.load("picture\\player.png")
        # self.pic = ""
        self.rect = self.pic.get_rect()
        self.left_available = True
        self.right_available = True
        self.top_available = True
        self.down_available = True
        self.left_pic = pygame.image.load("picture\\left.png")
        self.right_pic = pygame.image.load("picture\\right.png")
        self.top_pic = pygame.image.load("picture\\top.png")
        self.down_pic = pygame.image.load("picture\\down.png")

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

        if self.position[1]-self.rect.bottom/2 <= 0:  # top
            self.top_available = False
        else:
            self.top_available = True
        if self.position[1] + self.rect.bottom/2 >= self.height:  # down
            self.down_available = False
        else:
            self.down_available = True
        if self.position[0] - self.rect.right/2 <= 0:  # left
            self.left_available = False
        else:
            self.left_available = True
        if self.position[0] + self.rect.right/2 >= self.width:  # Right
            self.right_available = False
        else:
            self.right_available = True

    def shooting_direction(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        shoot_direction = math.atan2(mouse_y - self.position[1], mouse_x - self.position[0])
        if -(math.pi/4) <= shoot_direction <= (math.pi/4):
            self.pic = self.right_pic
            self.rect = self.pic.get_rect()
        if (math.pi/4) <= shoot_direction <= (3*math.pi/4):
            self.pic = self.down_pic
            self.rect = self.pic.get_rect()
        if (3*math.pi/4) <= shoot_direction <= math.pi or -math.pi <= shoot_direction <= -(3*math.pi/4):
            self.pic = self.left_pic
            self.rect = self.pic.get_rect()
        if -(3*math.pi/4) <= shoot_direction <= -(math.pi/4):
            self.pic = self.top_pic
            self.rect = self.pic.get_rect()


class Map:
    def __init__(self, the_width, the_height):
        # self.noise_map = []
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
                    # print(x)
                    # print(y)
                    # print(cellmap[x][y])
                    # print("__________________________")
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


def main():
    scale = 150
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0
    seed = random.randint(0, 100)

    the_river_threshold = -0.2  # 用于分类河流的阈值
    the_land_threshold = 0.0  # 用于分类陆地的阈值
    the_mountain_threshold = 0.2  # 用于分类高山的阈值
    noise_map = []

    the_map = Map(width, height)
    noise_map = the_map.generate_noise_map(width, height, scale, octaves, persistence, lacunarity, seed)
    the_map.render_map(noise_map, the_river_threshold, the_land_threshold, the_mountain_threshold)
    map = pygame.image.load("picture\map.jpg")

    player = Player(width, height)
    keydown = ""
    keyup = ""

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
        player.move(keyup)
        player.shooting_direction()
        # player_rect = player.pic.get_rect()
        # print(player_rect)
        # screen.fill((0, 0, 0))
        screen.blit(map, (0, 0))


        screen.blit(player.pic, (player.position[0]-player.rect.right/2, player.position[1]-player.rect.bottom/2))

        # screen.blit(pygame.transform.smoothscale(player.pic, (int(player_rect[2]), int(player_rect[3]))),
        #             (player.position[0], player.position[1]))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
