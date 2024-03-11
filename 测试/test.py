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

# 初始化变量
list1 = [(2,3), (3,4)]
list2 = [(7,8), (9,10)]
a = list1 + list2
print(a)
