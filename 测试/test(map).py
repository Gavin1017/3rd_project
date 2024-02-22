import pygame
import cellpylib as cpl
import numpy as np

# # 初始化 Pygame
pygame.init()
#
# # 地图尺寸
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# 细胞自动机配置
cell_size = 10  # 每个细胞的像素尺寸
cols, rows = width // cell_size, height // cell_size # cols=80, rows = 60

# 初始化细胞自动机矩阵


initial_condition = np.random.choice([0, 1], size=(cols, rows), p=[0.4, 0.6])
# 将第一行和最后一行的所有元素设置为1
initial_condition[0, :] = 1
initial_condition[-1, :] = 1

# 将第一列和最后一列的所有元素设置为1
initial_condition[:, 0] = 1
initial_condition[:, -1] = 1


cellular_automaton = cpl.init_simple2d(cols, rows)

# print(initial_condition.shape)
# print(cellular_automaton.shape)
# print("___________________")
cellular_automaton[0] = initial_condition
# print(cellular_automaton[0])

# 应用细胞自动机规则
def rule(grid,c,t):
    threshold = 4
    total_sum = grid.sum() - grid[1, 1]

    if total_sum <=threshold:
        cell = 0
    else:
        cell = 1
    return cell

# 例如，使用元胞自动机的洞穴生成规则
cave_map = cpl.evolve2d(cellular_automaton, timesteps=5, apply_rule=lambda n, c, t: rule(n, c, t))

def flood_fill(matrix, x, y, threshold):
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
            matrix[r[0],r[1]] = 1 - original_value

    return matrix, has_judged

final_matrix = cave_map[-1].copy()
all_judged = []
the_threshold = 5
for x in range(cave_map[-1].shape[0]):
    for y in range(cave_map[-1].shape[1]):
        if (x, y) not in all_judged:
            final_matrix, judged = flood_fill(final_matrix, x, y, the_threshold)
            all_judged = all_judged + judged

cave_map = final_matrix


# print(type(cave_map))
# 游戏主循环
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
            color = (255, 255, 255) if cave_map[col, row] == 0 else (0, 0, 0)
            pygame.draw.rect(screen, color, (col*cell_size, row*cell_size, cell_size, cell_size))

    # 更新屏幕显示
    pygame.display.flip()

pygame.quit()
