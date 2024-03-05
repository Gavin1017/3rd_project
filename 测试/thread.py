import pygame
import threading
import numpy as np
# 假设AStarSearch是你的A*算法实现
from test import a_star_search, Node
import random

# 初始化Pygame
pygame.init()

# 创建窗口
screen = pygame.display.set_mode((1200, 800))

# 设置标题
pygame.display.set_caption("A* Pathfinding with Multithreading")

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 地图设置
# grid = np.ones((30, 40))  # 示例网格
rows, cols = 1200, 800
grid = np.array([[random.randint(1, 4) for _ in range(cols)] for _ in range(rows)])

grid = np.array(grid)

start_pos = (0, 0)  # 起点位置
end_pos = (300, 400)  # 终点位置
path = []  # 路径存放位置


# A*搜索的后台执行
def async_astar_search(start, end, grid):
    global path
    start_node = Node(start[0], start[1])
    end_node = Node(end[0], end[1])
    path = a_star_search(grid, start_node, end_node)
    print("Path found:", path)


# 在新线程中启动A*搜索
thread = threading.Thread(target=async_astar_search, args=(start_pos, end_pos, grid))
thread.start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # 在这里绘制地图和路径等
    # 示例：绘制起点和终点
    pygame.draw.circle(screen, GREEN, start_pos, 5)
    pygame.draw.circle(screen, RED, end_pos, 5)

    # 绘制路径
    for point in path:
        pygame.draw.circle(screen, WHITE, point, 3)

    pygame.display.flip()

# 等待A*算法线程完成
thread.join()

pygame.quit()
