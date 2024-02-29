# import numpy as np
#
#
# def find_corners(arr):
#     rows, cols = arr.shape
#     positions = {'最左上': None, '最右上': None, '最左下': None, '最右下': None}
#
#     # 搜索最左上
#     for i in range(rows):
#         for j in range(cols):
#             if arr[i, j] == 0:
#                 positions['最左上'] = (i, j)
#                 break
#         if positions['最左上'] is not None:
#             break
#
#     # 搜索最右上
#     for i in range(rows):
#         for j in range(cols - 1, -1, -1):
#             if arr[i, j] == 0:
#                 positions['最右上'] = (i, j)
#                 break
#         if positions['最右上'] is not None:
#             break
#
#     # 搜索最左下
#     for i in range(rows - 1, -1, -1):
#         for j in range(cols):
#             if arr[i, j] == 0:
#                 positions['最左下'] = (i, j)
#                 break
#         if positions['最左下'] is not None:
#             break
#
#     # 搜索最右下
#     for i in range(rows - 1, -1, -1):
#         for j in range(cols - 1, -1, -1):
#             if arr[i, j] == 0:
#                 positions['最右下'] = (i, j)
#                 break
#         if positions['最右下'] is not None:
#             break
#
#     return positions
#
#
# # 示例数组
# arr = np.array([[1, 0, 0, 1],
#                 [1, 0, 1, 0],
#                 [0, 1, 1, 1],
#                 [1, 0, 1, 0]])
#
# positions = find_corners(arr)
# for position, coords in positions.items():
#     print(f"{position}的位置是: {coords}")

# import numpy as np
# from scipy.ndimage import label, find_objects
# import random
#
# # 假设labeled_array是经过label函数处理后的标记数组，n_labels是标记的总数
# # 例如：labeled_array, n_labels = label(your_data)
# your_data = np.array([[1, 0, 0, 1],
#                 [1, 0, 1, 0],
#                 [0, 0, 1, 1],
#                 [1, 0, 1, 0]])
#
#
# labeled_array, n_labels = label(1 - your_data)
# print(labeled_array)
# # 使用find_objects找到每个标记的切片对象
#
# def find_init_position(your_data):
#     tem = 1-your_data
#     array, n_labels = label(tem)
#
#     index_dict = {}
#     for i in range(array.shape[0]):
#         for j in range(array.shape[1]):
#             num = array[i, j]
#             if num != 0:
#                 if num not in index_dict:
#                     index_dict[num] = []
#                 index_dict[num].append((i, j))
#
#     # 对于每个数字随机选择一个索引
#     random_indices = {}
#     for num, indices in index_dict.items():
#         random_indices[num] = random.choice(indices)
#
#     return random_indices
#
# print(find_init_position(your_data))
# import numpy as np
#
#
# cave_position =[(2,3), (1,2), (1,3) ]
#
# b= [[1,1,1,1],
#              [0,1,0,1],
#              [0,1,0,1]]
#
# for x in cave_position:
#     if b[x[0],x[1]] != 0:
#         cave_position.remove(x)
# print(cave_position)
import numpy as np

# 假设这是你的两个二维数组
array1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
array2 = np.array([[1, 20, 3], [4, 50, 6], [70, 8, 90]])

# 使用numpy.where找到不同元素的索引
diff_indices = np.where(array1 != array2)

# 打印不同元素的索引
print('不同元素的索引:', list(zip(diff_indices[0], diff_indices[1])))
print(array1[1][2])


