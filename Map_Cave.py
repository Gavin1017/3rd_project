import pygame
import cellpylib as cpl
import numpy as np
import cv2
from scipy.ndimage import label, find_objects
from skimage.draw import line
from skimage.graph import route_through_array
clock = pygame.time.Clock()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
cell_size = 10
cols, rows = width // cell_size, height // cell_size # cols=80, rows = 60

class Cave:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.sell_size = cell_size

        # cols=80, rows = 60
        self.cols = width // cell_size
        self.rows = height // cell_size
        self.initial_condition = 0
        self.cave_map = []
        self.matrix = [[]] # final result

    def initial(self):
        # 初始化细胞自动机矩阵
        initial_condition = np.random.choice([0, 1], size=(self.cols, self.rows), p=[0.4, 0.6])
        # 将第一行和最后一行的所有元素设置为1
        initial_condition[0, :] = 1
        initial_condition[-1, :] = 1

        # 将第一列和最后一列的所有元素设置为1
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

    def cellular_automaton(self,steps):
        cellular_automaton = cpl.init_simple2d(self.cols, self.rows)
        cellular_automaton[0] = self.initial_condition
        # 例如，使用元胞自动机的洞穴生成规则
        cave_map = cpl.evolve2d(cellular_automaton, timesteps=steps, apply_rule=lambda n, c, t: self.rule(n, c, t))
        self.cave_map = cave_map

    def flood_fill(self, matrix, x, y, threshold):
        # 获取原始值以便我们知道需要填充哪些区域
        original_value = matrix[x, y]
        has_judged = []
        # 初始化区域大小和一个栈来存储所有需要访问的像素
        area_size = 0
        stack = [(x, y)]
        height, row = matrix.shape
        # 当栈不为空时处理所有相邻像素
        while stack:
            # print("judged:", has_judged)
            # print("the stack:", stack)
            # print("-------------")
            x, y = stack.pop()
            if matrix[x, y] == original_value:
                has_judged.append((x, y))
                area_size += 1
                # 将所有相邻像素添加到栈中
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

    def final_map(self,threshold):
        final_matrix = self.cave_map[-1].copy()
        all_judged = []
        the_threshold = threshold
        for x in range(self.cave_map[-1].shape[0]):
            for y in range(self.cave_map[-1].shape[1]):
                if (x, y) not in all_judged:
                    final_matrix, judged = self.flood_fill(final_matrix, x, y, the_threshold)
                    all_judged = all_judged + judged
        self.matrix = final_matrix

    def save(self):
        # 放大倍数
        scale_factor = 10

        # 使用 repeat 函数沿着两个轴放大数组
        scaled_array = np.repeat(np.repeat(self.matrix, scale_factor, axis=0), scale_factor, axis=1)
        scaled_array = scaled_array.T

        save_pic = np.array(scaled_array)
        color_array = np.full((*save_pic.shape, 3), 255)
        color_array[save_pic == 1] = (0, 0, 0)
        color_array[save_pic == 0] = (255, 255, 255)

        cv2.imwrite("picture\cave.jpg", color_array)

    def connect_components(self):
        tem_matrix = 1 - self.matrix
        labeled_array, num_features = label(tem_matrix)
        slices = find_objects(labeled_array)
        # 如果组件少于2个，不需要连通
        if num_features < 2:
            return labeled_array

        # 找到所有组件的中心点
        centroids = []
        for sl in slices:
            if sl is not None:
                center = [int((sl[i].start + sl[i].stop - 1) / 2) for i in range(len(sl))]
                centroids.append(center)

        # 使用最小生成树算法来找到连接所有组件的最少边的集合
        # 由于这里的情况比较简单，我们可以简化算法，直接连通所有中心点
        for i in range(len(centroids)):
            for j in range(i + 1, len(centroids)):
                start, end = centroids[i], centroids[j]
                # 使用图像中的路径规划算法找到最佳路径
                indices, weight = route_through_array(labeled_array == 0, start, end, fully_connected=False)
                # print(indices)
                indices = np.array(indices).T

                labeled_array[indices[0], indices[1]] = 1  # 使用标记值1填充路径

        binary_array = (labeled_array != 0).astype(int)
        self.matrix = 1 - binary_array

thecave = Cave(800, 600, 10)
thecave.initial()
thecave.cellular_automaton(5) # step of the cellular automaton
thecave.final_map(10) # the threshold of the area
thecave.connect_components()
# thecave.save()
labeled, features = label(thecave.matrix)
# cave = pygame.image.load("picture\cave.jpg")


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 清屏
    screen.fill((0, 0, 0))

    # 渲染细胞自动机生成的洞穴地图
    for row in range(rows):
        for col in range(cols):
            color = (255, 255, 255) if thecave.matrix[col, row] == 0 else (0, 0, 0)
            pygame.draw.rect(screen, color, (col*cell_size, row*cell_size, cell_size, cell_size))
    # screen.blit(cave,(0,0))
    # 更新屏幕显示
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
