import pygame
from random import randint, choice
import random


class Map:
    def __init__(self, width, height, surface, enemy):
        self.width = width
        self.height = height
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]

        self.player_pos = [1, 1]
        self.block_size = 20
        self.surface = surface

        self.picture = pygame.image.load("picture\\key.jpg")
        self.seed = random.randint(0, 100)
        self.selected_positions = []

        self.enemy = enemy
        self.time = 60

        self.player_pic = pygame.image.load("picture\\player_down.png")
        self.player_down = pygame.image.load("picture\\player_down.png")
        self.player_top = pygame.image.load("picture\\player_top.png")
        self.player_left = pygame.image.load("picture\\player_left.png")
        self.player_right = pygame.image.load("picture\\player_right.png")

    def resetMap(self, value):
        for y in range(self.height):
            for x in range(self.width):
                self.setMap(x, y, value)

    def setMap(self, x, y, value):
        if value == 0:
            self.map[y][x] = 0
        elif value == 1:
            self.map[y][x] = 1

    def isVisited(self, x, y):
        return self.map[y][x] != 1

    def picture_scale(self):
        self.picture = pygame.transform.scale(self.picture, (self.block_size, self.block_size))

    def zero_pos(self):
        zero_positions = [(j, i) for i, row in enumerate(self.map) for j, value in enumerate(row) if
                          value == 0]
        if (1, 1) in zero_positions:
            zero_positions.remove((1,1))
        if (self.width-2, self.height-2) in zero_positions:
            zero_positions.remove((self.width-2, self.height-2))
        self.selected_positions = random.sample(zero_positions, 3) if len(zero_positions) >= 3 else zero_positions

    # def showMap(self):
    #     for row in self.map:
    #         s = ''
    #         for entry in row:
    #             if entry == 0:
    #                 s += ' 0'
    #             elif entry == 1:
    #                 s += ' #'
    #             else:
    #                 s += ' X'
    #         print(s)

    def draw_maze(self):

        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)
                if cell == 1:  # 墙壁
                    pygame.draw.rect(self.surface, (0, 0, 0), rect)
                else:  # 通路
                    pygame.draw.rect(self.surface, (255, 255, 255), rect)

        for i in self.selected_positions:  # 吃掉钥匙
            if self.player_pos[0] == i[0] and self.player_pos[1] == i[1]:
                self.selected_positions.remove(i)
                self.time += 10
            self.surface.blit(self.picture, (i[0] * self.block_size, i[1] * self.block_size))
        if len(self.selected_positions) == 0:  # 当三把钥匙都吃掉，生成最后一把钥匙（出口）
            self.surface.blit(self.picture, ((self.width-2) * self.block_size, (self.width-2) * self.block_size))

    def check_finish(self):
        if len(self.selected_positions) == 0 and self.player_pos == [self.width-2,self.width-2]:
            return True
        else:
            return False

    def draw_player(self):
        # rect = pygame.Rect(self.player_pos[0] * self.block_size, self.player_pos[1] * self.block_size, self.block_size,
        #                    self.block_size)
        # pygame.draw.rect(self.surface, (255, 0, 0), rect)

        player_pic = pygame.transform.scale(self.player_pic, (self.block_size, self.block_size))
        self.surface.blit(player_pic, (self.player_pos[0] * self.block_size, self.player_pos[1] * self.block_size))

    def move_player(self, direction):
        x, y = self.player_pos
        if direction == 'UP' and self.map[y - 1][x] == 0:
            self.player_pos[1] -= 1
            self.player_pic = self.player_top
        elif direction == 'DOWN' and self.map[y + 1][x] == 0:
            self.player_pos[1] += 1
            self.player_pic = self.player_down
        elif direction == 'LEFT' and self.map[y][x - 1] == 0:
            self.player_pos[0] -= 1
            self.player_pic = self.player_left
        elif direction == 'RIGHT' and self.map[y][x + 1] == 0:
            self.player_pos[0] += 1
            self.player_pic = self.player_right

# find unvisited adjacent entries of four possible entris
# then add random one of them to checklist and mark it as visited
def checkAdjacentPos(map, x, y, width, height, checklist):
    directions = []
    if x > 0:
        if not map.isVisited(2 * (x - 1) + 1, 2 * y + 1):
            directions.append(0)

    if y > 0:
        if not map.isVisited(2 * x + 1, 2 * (y - 1) + 1):
            directions.append(1)

    if x < width - 1:
        if not map.isVisited(2 * (x + 1) + 1, 2 * y + 1):
            directions.append(2)

    if y < height - 1:
        if not map.isVisited(2 * x + 1, 2 * (y + 1) + 1):
            directions.append(3)

    if len(directions):
        direction = choice(directions)
        # print("(%d, %d) => %s" % (x, y, str(direction)))
        if direction == 0:
            map.setMap(2 * (x - 1) + 1, 2 * y + 1, 0)
            map.setMap(2 * x, 2 * y + 1, 0)
            checklist.append((x - 1, y))
        elif direction == 1:
            map.setMap(2 * x + 1, 2 * (y - 1) + 1, 0)
            map.setMap(2 * x + 1, 2 * y, 0)
            checklist.append((x, y - 1))
        elif direction == 2:
            map.setMap(2 * (x + 1) + 1, 2 * y + 1, 0)
            map.setMap(2 * x + 2, 2 * y + 1, 0)
            checklist.append((x + 1, y))
        elif direction == 3:
            map.setMap(2 * x + 1, 2 * (y + 1) + 1, 0)
            map.setMap(2 * x + 1, 2 * y + 2, 0)
            checklist.append((x, y + 1))
        return True
    else:
        # if not find any unvisited adjacent entry
        return False


# random prim algorithm
def randomPrim(map, width, height):
    # startX, startY = (randint(0, width - 1), randint(0, height - 1))
    startX, startY = 1, 1
    # map.setMap(2 * startX + 1, 2 * startY + 1, 0)
    checklist = []
    checklist.append((startX, startY))
    # print(choice(checklist))
    while bool(len(checklist)):
        # select a random entry from checklist
        entry = choice(checklist)
        if not checkAdjacentPos(map, entry[0], entry[1], width, height, checklist):
            # the entry has no unvisited adjacent entry, so remove it from checklist
            checklist.remove(entry)


def doRandomPrim(map):
    # set all entries of map to wall(the number is 1)
    map.resetMap(1)
    randomPrim(map, (map.width - 1) // 2, (map.height - 1) // 2)

# def run():
#     WIDTH = 25
#     HEIGHT = 25
#     map = Map(WIDTH, HEIGHT)
#     doRandomPrim(map)
#     map.showMap()
#     print(map.map)
#
# run()
