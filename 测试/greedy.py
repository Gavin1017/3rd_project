# class RPGEnemyTracker:
#     def __init__(self, map_grid, terrain_costs):
#         """
#         map_grid: 二维列表，表示地图的地形布局，其中的数字1, 2, 3, 4代表不同地形
#         terrain_costs: 字典，表示不同地形编号对应的移动速度因子（成本）
#         """
#         self.map_grid = map_grid
#         self.terrain_costs = terrain_costs
#         self.directions = [(0,1), (1,0), (0,-1), (-1,0)]  # 可以移动的方向，分别是右、下、左、上
#
#     def get_terrain_cost(self, x, y):
#         """获取指定位置的地形成本"""
#         return self.terrain_costs[self.map_grid[x][y]]
#
#     def find_next_step(self, enemy_pos, target_pos):
#         """
#         使用贪心算法找到下一步的最佳移动方向
#         enemy_pos: 敌人当前的位置，形式为 (x, y)
#         target_pos: 目标的位置，形式为 (x, y)
#         """
#         min_cost = float('inf')
#         next_step = None
#         for direction in self.directions:
#             new_x = enemy_pos[0] + direction[0]
#             new_y = enemy_pos[1] + direction[1]
#
#             # 检查新位置是否在地图范围内
#             if 0 <= new_x < len(self.map_grid) and 0 <= new_y < len(self.map_grid[0]):
#                 cost = self.get_terrain_cost(new_x, new_y)
#                 if cost < min_cost:
#                     min_cost = cost
#                     next_step = (new_x, new_y)
#
#         return next_step
#
# # 示例：
# terrain_costs = {1: 1, 2: 2, 3: 3, 4: 4}  # 假设数字1, 2, 3, 4分别对应的成本
# map_grid = [
#     [1, 3, 2],
#     [4, 1, 2],
#     [3, 2, 1]
# ]
#
# tracker = RPGEnemyTracker(map_grid, terrain_costs)
# enemy_pos = (2, 0)  # 敌人起始位置
# target_pos = (0, 2)  # 目标位置
#
# # 模拟追踪过程
# for _ in range(10):  # 假定最多移动5步
#     enemy_pos = tracker.find_next_step(enemy_pos, target_pos)
#     if enemy_pos:
#         print(f"敌人移动到 {enemy_pos}")
#         if enemy_pos == target_pos:
#             print("敌人已到达目标位置")
#             break
#     else:
#         print("没有可移动的路径")
#         break
class test:
    def __init__(self):
        self.x = 3
        self.y = 4

a = test()

print(a.x)
for x in range(5):
    print("a的属性：",a.x)
    print(x)