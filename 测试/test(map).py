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

# cave_map = np.repeat(cave_map, 10, axis=1)
#
# cave_map = np.repeat(cave_map, 10, axis=2)
print(cave_map.shape)

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
            color = (255, 255, 255) if cave_map[-1][col, row] == 0 else (0, 0, 0)
            pygame.draw.rect(screen, color, (col*cell_size, row*cell_size, cell_size, cell_size))

    # 更新屏幕显示
    pygame.display.flip()

pygame.quit()
