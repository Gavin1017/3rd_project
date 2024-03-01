import pygame
import cellpylib as cpl
import numpy as np
import cv2
from scipy.ndimage import label, find_objects
# from skimage.draw import line
from skimage.graph import route_through_array
import random

# clock = pygame.time.Clock()
# width, height = 800, 600
# screen = pygame.display.set_mode((width, height))
# cell_size = 10
# cols, rows = width // cell_size, height // cell_size  # cols=80, rows = 60


class Cave:
    def __init__(self, width, height, cell_size, enemy):
        self.width = width
        self.height = height
        self.sell_size = cell_size

        # cols=80, rows = 60
        self.cols = width // cell_size
        self.rows = height // cell_size
        self.initial_condition = 0
        self.cave_map: np.ndarray = np.array([])
        self.unconnected_cave: np.ndarray = np.array([])  # have not connected

        self.matrix: np.ndarray = np.array([])  # final result
        self.enemy = enemy

    def initial(self):
        # init the matrix of the cellular automaton
        initial_condition = np.random.choice([0, 1], size=(self.cols, self.rows), p=[0.35, 0.65])
        # make the first and final row to be 1
        initial_condition[0, :] = 1
        initial_condition[-1, :] = 1

        # make the first and final column to be 1
        initial_condition[:, 0] = 1
        initial_condition[:, -1] = 1
        self.initial_condition = initial_condition

    def rule(self, grid, c, t):
        threshold = 4
        total_sum = grid.sum() - grid[1, 1]

        if total_sum <= threshold:
            cell = 0
        else:
            cell = 1
        return cell

    def cellular_automaton(self, steps):
        cellular_automaton = cpl.init_simple2d(self.cols, self.rows)
        cellular_automaton[0] = self.initial_condition
        # use the "cpl.evolve2d" to get the cave
        cave_map = cpl.evolve2d(cellular_automaton, timesteps=steps, apply_rule=lambda n, c, t: self.rule(n, c, t))
        self.cave_map = cave_map

    def flood_fill(self, matrix, x, y, threshold):

        # get original matrix so that which area is needed to be filled
        original_value = matrix[x, y]
        has_judged = []

        # initial the matrix to save all the elements
        area_size = 0
        stack = [(x, y)]
        height, row = matrix.shape
        # if the stack is not empty, deal with all the elements
        while stack:

            x, y = stack.pop()
            if matrix[x, y] == original_value:
                has_judged.append((x, y))
                area_size += 1

                # append all the neighbour to the stack
                if x - 1 >= 0 and ((x - 1, y) not in has_judged) and matrix[x - 1][y] == original_value and (
                        (x - 1, y) not in stack):
                    stack.append((x - 1, y))
                if x + 1 <= height - 1 and ((x + 1, y) not in has_judged) and matrix[x + 1][y] == original_value and (
                        (x + 1, y) not in stack):
                    stack.append((x + 1, y))
                if y - 1 >= 0 and ((x, y - 1) not in has_judged) and matrix[x][y - 1] == original_value and (
                        (x, y - 1) not in stack):
                    stack.append((x, y - 1))
                if y + 1 <= row - 1 and ((x, y + 1) not in has_judged) and matrix[x][y + 1] == original_value and (
                        (x, y + 1) not in stack):
                    stack.append((x, y + 1))
        if area_size <= threshold:
            for r in has_judged:
                matrix[r[0], r[1]] = 1 - original_value

        return matrix, has_judged

    def final_map(self, threshold):
        final_matrix = self.cave_map[-1].copy()
        all_judged = []
        the_threshold = threshold
        for x in range(self.cave_map[-1].shape[0]):
            for y in range(self.cave_map[-1].shape[1]):
                if (x, y) not in all_judged:
                    final_matrix, judged = self.flood_fill(final_matrix, x, y, the_threshold)
                    all_judged = all_judged + judged
        self.unconnected_cave = final_matrix.T.copy()
        self.matrix = final_matrix.T.copy()

    # the save function does not be used
    def save(self):
        # zoom up
        scale_factor = 10

        # use repeat to zoom up
        scaled_array = np.repeat(np.repeat(self.matrix, scale_factor, axis=0), scale_factor, axis=1)
        # scaled_array = scaled_array.T
        return scaled_array
        # save_pic = np.array(scaled_array)
        # color_array = np.full((*save_pic.shape, 3), 255)
        # color_array[save_pic == 1] = (0, 0, 0)
        # color_array[save_pic == 0] = (255, 255, 255)
        #
        # cv2.imwrite("picture\cave.jpg", color_array)

    def connect_components(self):

        tem_matrix = 1 - self.matrix
        labeled_array, num_features = label(tem_matrix)
        slices = find_objects(labeled_array)
        # if label is less than 2, not need to connect
        if num_features < 2:
            return labeled_array

        # find the center of all the components
        centroids = []
        for sl in slices:
            if sl is not None:
                center = [int((sl[i].start + sl[i].stop - 1) / 2) for i in range(len(sl))]
                centroids.append(center)

        # Use the minimum spanning tree algorithm to find the set of the fewest edges that connects all components

        for i in range(len(centroids)):
            for j in range(i + 1, len(centroids)):
                start, end = centroids[i], centroids[j]
                # use "route_through_array" to find the best path
                indices, weight = route_through_array(labeled_array == 0, start, end, fully_connected=False)
                # print(indices)
                indices = np.array(indices).T

                labeled_array[indices[0], indices[1]] = 1  # use 1 to fill the path

        binary_array = (labeled_array != 0).astype(int)
        self.matrix = 1 - binary_array

    def block(self):
        diff_indices = np.where(self.unconnected_cave != self.matrix)
        block_list = list(zip(diff_indices[0], diff_indices[1]))
        for x in block_list:
            self.matrix[x[0], x[1]] = 2


def find_init_position(your_data):
    tem = 1-your_data
    array, n_labels = label(tem)

    index_dict = {}
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            num = array[i, j]
            if num != 0:
                if num not in index_dict:
                    index_dict[num] = []
                index_dict[num].append((i, j))

    # 对于每个数字随机选择一个索引
    random_indices = {}
    for num, indices in index_dict.items():
        random_indices[num] = random.choice(indices)

    return random_indices


class Enemy:
    def __init__(self, position, cave_map, size, surface, cell_size):
        self.position = [position[0], position[1]]  # 按照像素来确定位置
        self.hp = 100
        self.attack = 34
        self.cave = cave_map
        self.size = size
        self.surface = surface
        self.cd = 0  # 4 second cd
        self.invincible_after_injured = 0  # 受伤后有2s的无敌时间
        self.pic = pygame.image.load("picture\\cave_monster.jpg")
        self.cell_size = cell_size

    def move(self, direction, bomb_list):
        "'UP', 'DOWN', 'LEFT', 'RIGHT'"

        x, y = self.position
        i = 0
        if len(bomb_list) != 0:
            if direction == 'UP' and self.cave[x - 1][y] == 0:
                for bomb in bomb_list:
                    if x - 1 != bomb.position[0] / self.cell_size or y != bomb.position[1] / self.cell_size:
                        i += 1
                if i == len(bomb_list):
                    self.position[0] -= 1
            elif direction == 'DOWN' and self.cave[x + 1][y] == 0:
                for bomb in bomb_list:
                    if x + 1 != bomb.position[0] / self.cell_size or y != bomb.position[1] / self.cell_size:
                        i += 1
                if i == len(bomb_list):
                    self.position[0] += 1
            elif direction == 'LEFT' and self.cave[x][y - 1] == 0:
                for bomb in bomb_list:
                    if y - 1 != bomb.position[1] / self.cell_size or x != bomb.position[0] / self.cell_size:
                        i += 1
                if i == len(bomb_list):
                    self.position[1] -= 1
            elif direction == 'RIGHT' and self.cave[x][y + 1] == 0:
                for bomb in bomb_list:
                    if y + 1 != bomb.position[1] / self.cell_size or x != bomb.position[0] / self.cell_size:
                        i += 1
                if i == len(bomb_list):
                    self.position[1] += 1
        else:
            if direction == 'UP' and self.cave[x - 1][y] == 0:
                self.position[0] -= 1
            elif direction == 'DOWN' and self.cave[x + 1][y] == 0:
                self.position[0] += 1
            elif direction == 'LEFT' and self.cave[x][y - 1] == 0:
                self.position[1] -= 1
            elif direction == 'RIGHT' and self.cave[x][y + 1] == 0:
                self.position[1] += 1

    def draw(self):
        scaled_image = pygame.transform.scale(self.pic, (self.cell_size, self.cell_size))
        self.surface.blit(scaled_image, (self.position[1]*self.size, self.position[0]*self.size))

class Player:
    def __init__(self, position, cave_map, size, surface, cell_size):  # 这里position是按照numpy数组来，而不是横纵坐标.size是player大小
        self.position = [position[0], position[1]]  # 按照像素来确定位置
        self.hp = 100
        self.attack = 34
        self.cave = cave_map
        self.size = size
        self.surface = surface
        self.cd = 0  # 4 second cd
        self.invincible_after_injured = 0  # 受伤后有2s的无敌时间
        self.cell_size = cell_size

        self.pic = pygame.image.load("picture\\player_down.png")
        self.player_down = pygame.image.load("picture\\player_down.png")
        self.player_top = pygame.image.load("picture\\player_top.png")
        self.player_left = pygame.image.load("picture\\player_left.png")
        self.player_right = pygame.image.load("picture\\player_right.png")

    def move(self, direction, bomb_list):
        x, y = self.position
        i = 0
        if len(bomb_list) != 0:
            if direction == 'UP' and self.cave[x - 1][y] == 0:
                self.pic = self.player_top
                for bomb in bomb_list:
                    if x-1 != bomb.position[0]/self.cell_size or y != bomb.position[1]/self.cell_size:
                        i += 1
                if i == len(bomb_list):
                    self.position[0] -= 1
            elif direction == 'DOWN' and self.cave[x + 1][y] == 0:
                self.pic = self.player_down
                for bomb in bomb_list:
                    if x+1!=bomb.position[0]/self.cell_size or y != bomb.position[1]/self.cell_size:
                        i+=1
                if i == len(bomb_list):
                    self.position[0] += 1
            elif direction == 'LEFT' and self.cave[x][y - 1] == 0:
                self.pic = self.player_left
                for bomb in bomb_list:
                    if y-1 != bomb.position[1]/self.cell_size or x != bomb.position[0]/self.cell_size:
                        i += 1
                if i == len(bomb_list):
                    self.position[1] -= 1
            elif direction == 'RIGHT' and self.cave[x][y + 1] == 0:
                self.pic = self.player_right
                for bomb in bomb_list:
                    if y+1 != bomb.position[1]/self.cell_size or x != bomb.position[0]/self.cell_size:
                        i += 1
                if i == len(bomb_list):
                    self.position[1] += 1
        else:
            if direction == 'UP' and self.cave[x - 1][y] == 0:
                self.pic = self.player_top
                self.position[0] -= 1
            elif direction == 'DOWN' and self.cave[x + 1][y] == 0:
                self.pic = self.player_down
                self.position[0] += 1
            elif direction == 'LEFT' and self.cave[x][y - 1] == 0:
                self.pic = self.player_left
                self.position[1] -= 1
            elif direction == 'RIGHT' and self.cave[x][y + 1] == 0:
                self.pic = self.player_right
                self.position[1] += 1

    def draw(self,):
        scaled_image = pygame.transform.scale(self.pic, (self.cell_size, self.cell_size))
        self.surface.blit(scaled_image, (self.position[1]*self.size, self.position[0]*self.size))
    def update_map(self, new_map):
        self.cave = new_map

class Bomb:
    def __init__(self, position, owner, cell_size):
        self.position = position  # 为原本numpy数组的cell_size倍
        self.range = 1  # 爆炸范围默认十字
        self.explosion_time = 3  # 爆炸时间默认3s
        self.owner = owner  # 炸弹的主人
        self.remaining_time = self.explosion_time  # 炸弹剩余时间
        self.bomb_pic = pygame.image.load("picture\\bomb.png")
        self.flame_pic = pygame.image.load("picture\\bomb_fire.png")
        self.flame_time = 2  # 火焰留存时间2s
        self.cell_size = cell_size

    def check_collision(self, player: Player, enemy_position_list: list):
        collided = []
        if player.position[0] == self.position[0]/self.cell_size and self.position[1]/self.cell_size-self.range <=player.position[1]<=self.position[1]/self.cell_size+self.range:
            collided.append(player)
        elif player.position[1] == self.position[1]/self.cell_size and self.position[0]/self.cell_size-self.range <=player.position[0]<=self.position[0]/self.cell_size+self.range:
            collided.append(player)

        for x in enemy_position_list:
            if x.position[0] == self.position[0]/self.cell_size and self.position[1]/self.cell_size-self.range <=x.position[1]<=self.position[1]/self.cell_size+self.range:
                collided.append(x)
            elif x.position[1] == self.position[1]/self.cell_size and self.position[0]/self.cell_size-self.range <=x.position[0]<=self.position[0]/self.cell_size+self.range:
                collided.append(x)

        return collided, self.owner

    def draw_before_explosion(self, surface):
        self.bomb_pic = pygame.transform.scale(self.bomb_pic, (self.cell_size, self.cell_size))

        surface.blit(self.bomb_pic, (self.position[1], self.position[0]))

    def draw_after_explosion(self, surface):
        self.flame_pic = pygame.transform.scale(self.flame_pic, (self.cell_size, self.cell_size))
        surface.blit(self.flame_pic, (self.position[1], self.position[0]))
        for x in range(self.range):
            surface.blit(self.flame_pic, (self.position[1], self.position[0]+x*self.cell_size+self.cell_size))
            surface.blit(self.flame_pic, (self.position[1], self.position[0]-x*self.cell_size-self.cell_size))
            surface.blit(self.flame_pic, (self.position[1]+x*self.cell_size+self.cell_size, self.position[0]))
            surface.blit(self.flame_pic, (self.position[1]-x*self.cell_size-self.cell_size, self.position[0]))

    def check_block_collision(self, cave_map):
        if cave_map[int(self.position[0]/self.cell_size)][int(self.position[1]/self.cell_size)] == 2:
            cave_map[self.position[0]/self.cell_size][self.position[1]/self.cell_size] = 0
        for x in range(self.range):
            if int(self.position[0]/self.cell_size+x+1) < cave_map.shape[0]:  # 最下面判断是否超出
                if cave_map[int(self.position[0] / self.cell_size + x + 1)][int(self.position[1] / self.cell_size)] == 2:
                    cave_map[int(self.position[0]/self.cell_size+x+1)][int(self.position[1]/self.cell_size)] = 0
            else:
                if cave_map[cave_map.shape[0]-1][int(self.position[1] / self.cell_size)] == 2:
                    cave_map[cave_map.shape[0]-1][int(self.position[1]/self.cell_size)] = 0

            if int(self.position[0]/self.cell_size-x-1) >= 0:  # 最上面判断是否超出
                if cave_map[int(self.position[0] / self.cell_size - x - 1)][int(self.position[1] / self.cell_size)] == 2:
                    cave_map[int(self.position[0]/self.cell_size - x - 1)][int(self.position[1]/self.cell_size)] = 0
            else:
                if cave_map[0][int(self.position[1] / self.cell_size)] == 2:
                    cave_map[0][int(self.position[1]/self.cell_size)] = 0

            if int(self.position[1]/self.cell_size+x+1) < cave_map.shape[1]:  # 最右面判断是否超出
                if cave_map[int(self.position[0] / self.cell_size)][int(self.position[1] / self.cell_size+x+1)] == 2:
                    cave_map[int(self.position[0]/self.cell_size)][int(self.position[1]/self.cell_size+x+1)] = 0
            else:
                if cave_map[int(self.position[0]/self.cell_size)][int(cave_map.shape[1]-1/self.cell_size)] == 2:
                    cave_map[int(self.position[0]/self.cell_size)][int(cave_map.shape[1]-1/self.cell_size)] = 0

            if int(self.position[1]/self.cell_size-x-1) >= 0:  # 最左面判断是否超出
                if cave_map[int(self.position[0] / self.cell_size)][int(self.position[1] / self.cell_size)-x-1] == 2:
                    cave_map[int(self.position[0]/self.cell_size)][int(self.position[1]/self.cell_size)-x-1] = 0
            else:
                if cave_map[int(self.position[0]/self.cell_size)][0] == 2:
                    cave_map[int(self.position[0]/self.cell_size)][0] = 0

            # if int(self.position[0]/self.cell_size+x+1) < cave_map.shape[0] \
            #     or int(self.position[0]/self.cell_size-x-1) >= 0 \
            #     or int(self.position[1]/self.cell_size+x+1) < cave_map.shape[1] \
            #     or int(self.position[1]/self.cell_size-x-1) >= 0:
            #     if cave_map[int(self.position[0]/self.cell_size+x+1)][int(self.position[1]/self.cell_size)] == 2:
            #         cave_map[int(self.position[0]/self.cell_size+x+1)][int(self.position[1]/self.cell_size)] = 0
            #     if cave_map[int(self.position[0]/self.cell_size-x-1)][int(self.position[1]/self.cell_size)] == 2:
            #         cave_map[int(self.position[0]/self.cell_size-x-1)][int(self.position[1]/self.cell_size)] = 0
            #     if cave_map[int(self.position[0]/self.cell_size)][int(self.position[1]/self.cell_size+x+1)] == 2:
            #         cave_map[int(self.position[0]/self.cell_size)][int(self.position[1]/self.cell_size+x+1)] = 0
            #     if cave_map[int(self.position[0]/self.cell_size)][int(self.position[1]/self.cell_size-x-1)] == 2:
            #         cave_map[int(self.position[0]/self.cell_size)][int(self.position[1]/self.cell_size-x-1)] = 0
            # elif int(self.position[0]/self.cell_size+x+1) >= cave_map.shape[0]:
            #     if cave_map[int(cave_map.shape[0])-1][int(self.position[1]/self.cell_size)] == 2:
            #         cave_map[int(cave_map.shape[0])-1][int(self.position[1]/self.cell_size)] = 0
            #     if cave_map[int(self.position[0]/self.cell_size-x-1)][int(self.position[1]/self.cell_size)] == 2:
            #         cave_map[int(self.position[0]/self.cell_size-x-1)][int(self.position[1]/self.cell_size)] = 0
            #     if cave_map[int(self.position[0]/self.cell_size)][int(self.position[1]/self.cell_size+x+1)] == 2:
            #         cave_map[int(self.position[0]/self.cell_size)][int(self.position[1]/self.cell_size+x+1)] = 0
            #     if cave_map[int(self.position[0]/self.cell_size)][int(self.position[1]/self.cell_size-x-1)] == 2:
            #         cave_map[int(self.position[0]/self.cell_size)][int(self.position[1]/self.cell_size-x-1)] = 0
            #

        return cave_map

