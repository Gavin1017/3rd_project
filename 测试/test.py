# import heapq
#
#
# class Node:
#     def __init__(self, x, y, cost=1):
#         self.x = x
#         self.y = y
#         self.cost = cost
#         self.parent = None
#         self.g = 0
#         self.h = 0
#         self.f = 0
#
#     def __lt__(self, other):
#         return self.f < other.f
#
#
# def heuristic(a, b):
#     # 曼哈顿距离，适用于四方向移动
#     return abs(a.x - b.x) + abs(a.y - b.y)
#
#
# def a_star_search(grid, start, end):
#     open_list = []
#     closed_set = set()
#
#     heapq.heappush(open_list, start)
#
#     while open_list:
#         current_node = heapq.heappop(open_list)
#
#         if (current_node.x, current_node.y) in closed_set:
#             continue
#
#         if current_node.x == end.x and current_node.y == end.y:
#             path = []
#             while current_node:
#                 path.append((current_node.x, current_node.y))
#                 current_node = current_node.parent
#             return path[::-1]
#
#         closed_set.add((current_node.x, current_node.y))
#
#         for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:  # 四方向移动
#             x, y = current_node.x + dx, current_node.y + dy
#
#             if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and (x, y) not in closed_set:
#                 neighbor = Node(x, y, grid[x][y])
#                 neighbor.parent = current_node
#                 neighbor.g = current_node.g + neighbor.cost
#                 neighbor.h = heuristic(neighbor, end)
#                 neighbor.f = neighbor.g + neighbor.h
#
#                 if (neighbor.x, neighbor.y) not in [(n.x, n.y) for n in open_list]:
#                     heapq.heappush(open_list, neighbor)
#
#     return None
#
# #
# # # 示例用法
# # grid = [
# #     [1, 1, 1, 1],
# #     [1, 1, 0, 1],
# #     [3, 2, 3, 1],
# #     [1, 1, 1, 1]
# # ]
# #
# # # import random
# # # import time
# # import numpy as np
# # # begin = time.time()
# # # # 创建一个二维列表，尺寸为1200x800
# # # rows, cols = 120, 80
# # # grid = np.array([[random.randint(1, 4) for _ in range(cols)] for _ in range(rows)])
# # #
# # grid = np.array(grid)
# # start = Node(0, 0)
# # end = Node(3, 3)
# # path = a_star_search(grid, start, end)
# # #
# # print("Path:", path)
# # # print("总时间： ",time.time()-begin)

import numpy as np
#
# # 假设arr是你的二维numpy数组
# arr = np.array([[0, 1, 2], [2, 1, 0]])
#
# # # 使用np.where函数
# # arr = np.where(arr==1, 1000, np.where(arr==2, 50, 1))
#
# # 或者使用条件索引
# arr[arr == 1] = 1000
# arr[arr == 2] = 50
# arr[arr == 0] = 1
#
# print(arr)

# map = np.array([[0, 1, 2], [2, 1, 0]])
# list = [[0, 1, 2], [2, 1, 0]]
# for x in len(list):
#     print(x)


import numpy as np
#
# b = [1,2,3,4,5,6]
# a = b.copy()
#
# i=1
# for x in a:
#     if x == i:
#         b.remove(x)
#     i+=1
#
# print("a",b)
#
import pygame
import sys

# 初始化pygame
pygame.init()

# 设置窗口
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("玩家血条展示")

# 设置颜色
red = (255, 0, 0)
white = (255, 255, 255)

# 玩家血量
max_health = 100  # 玩家的最大血量
current_health = 75  # 玩家当前血量，这个值可以根据游戏逻辑变化

# 血条位置和尺寸
bar_width = 200
bar_height = 20
bar_x = (screen_width - bar_width) / 2  # 血条水平居中
bar_y = 10  # 血条距离屏幕顶部的距离

# 设置字体
font = pygame.font.SysFont(None, 30)

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # 使用黑色填充屏幕

    # 绘制血条背景
    pygame.draw.rect(screen, white, (bar_x, bar_y, bar_width, bar_height))

    # 计算当前血量的宽度比例
    health_width = (current_health / max_health) * bar_width

    # 绘制当前血量
    pygame.draw.rect(screen, red, (bar_x, bar_y, health_width, bar_height))

    # 显示血量文本
    health_text = font.render(f"{current_health} / {max_health}", True, red)
    screen.blit(health_text, (bar_x + (bar_width / 2) - (health_text.get_width() / 2), bar_y))

    pygame.display.flip()

# 退出pygame
pygame.quit()
sys.exit()






