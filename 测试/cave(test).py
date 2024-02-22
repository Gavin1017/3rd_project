# import numpy as np
# from scipy.ndimage import label, find_objects
# from scipy.spatial.distance import cdist
# from skimage.draw import line
#
# # 定义反转后的输入数组
# input_array_inverted = np.array([[0, 1, 1, 1, 0],
#                                  [0, 0, 0, 1, 1],
#                                  [1, 1, 0, 0, 0],
#                                  [1, 1, 0, 0, 1]])
# # input_array_inverted = np.array(
# # [[0, 1, 1, 1, 0],
# #  [0, 1, 0 ,1, 1],
# #  [1, 1 ,0 ,1, 0],
# #  [1, 1 ,0 ,0, 1]])
#
# # def connect_components(array):
# #     labeled_array, num_features = label(array)
# #     print("labeled:", labeled_array)
# #     print("number_features:", num_features)
# #     if num_features <= 1:
# #         return array  # 没有足够的组件来连接
# #
# #     slices = find_objects(labeled_array)
# #     print("slice:", slices)
# #     centroids = [(int((sl[0].start + sl[0].stop - 1) / 2), int((sl[1].start + sl[1].stop - 1) / 2)) for sl in slices if sl]
# #
# #     # 对每一对组件，计算中心点之间的距离
# #     distances = cdist(centroids, centroids)
# #
# #     # 寻找距离最短的一对组件
# #     min_dist = np.inf
# #     min_pair = (None, None)
# #     for i in range(len(distances)):
# #         for j in range(i+1, len(distances)):
# #             if distances[i, j] < min_dist:
# #                 min_dist = distances[i, j]
# #                 min_pair = (i, j)
# #
# #     if min_pair == (None, None):
# #         return labeled_array  # 没有找到可以连接的组件
# #
# #     # 计算应该连接的组件的中心点
# #     point1, point2 = centroids[min_pair[0]], centroids[min_pair[1]]
# #
# #     # 绘制直线连接这两点
# #     rr, cc = line(point1[0], point1[1], point2[0], point2[1])
# #     array[rr, cc] = 1  # 使用非背景值来填充路径
# #
# #     return array
#
# # 连通组件
# def connect_all_components(array):
#     labeled_array, num_features = label(array)
#
#     if num_features <= 1:
#         return array  # 没有足够的组件来连接
#
#     slices = find_objects(labeled_array)
#
#     print(slices)
#     centroids = [(int((sl[0].start + sl[0].stop - 1) / 2), int((sl[1].start + sl[1].stop - 1) / 2)) for sl in slices]
#     # print(centroids)
#     # 对每个组件，找到并连接最近的组件
#     for i, centroid in enumerate(centroids):
#         print("i:",i)
#         print("centroid:", centroid)
#         distances = np.sqrt([(centroid[0] - c[0]) ** 2 + (centroid[1] - c[1]) ** 2 for c in centroids])
#         distances[i] = np.inf  # 排除自身
#         min_distance_index = np.argmin(distances)
#
#         # 绘制连接最近组件的线
#         if distances[min_distance_index] != np.inf:
#             point1 = centroid
#             point2 = centroids[min_distance_index]
#             rr, cc = line(point1[0], point1[1], point2[0], point2[1])
#             array[rr, cc] = 1
#
#     return array
#
#
# connected_array = connect_all_components(input_array_inverted)
# print(connected_array)
#

# 由于之前的代码执行状态被重置，重新加载图像和定义必要的函数
# import numpy as np
# from scipy.ndimage import label, find_objects
# from skimage.draw import line
# from skimage.graph import route_through_array
#
# # 从用户上传的文件中加载图像数据
# # 因为这个环境中不能直接打开图像，我将基于用户提供的信息重建数组
# input_array_inverted = np.array([[0, 1, 1, 1, 0],
#                                  [0, 1, 0, 1, 1],
#                                  [1, 0, 0, 0, 0],
#                                  [1, 1, 1, 1, 1]])
#
# # 使用 label 函数来标记数组中的组件
# labeled_array, num_features = label(input_array_inverted)
# slices = find_objects(labeled_array)
#
#
# # 连通所有组件的函数
# def connect_components(labeled_array, num_features, slices):
#     """
#     连接所有标记的组件
#     """
#     # 如果组件少于2个，不需要连通
#     if num_features < 2:
#         return labeled_array
#
#     # 找到所有组件的中心点
#     centroids = []
#     for sl in slices:
#         if sl is not None:
#             center = [int((sl[i].start + sl[i].stop - 1) / 2) for i in range(len(sl))]
#             centroids.append(center)
#
#     # 使用最小生成树算法来找到连接所有组件的最少边的集合
#     # 由于这里的情况比较简单，我们可以简化算法，直接连通所有中心点
#     for i in range(len(centroids)):
#         for j in range(i + 1, len(centroids)):
#             start, end = centroids[i], centroids[j]
#             # 使用图像中的路径规划算法找到最佳路径
#             indices, weight = route_through_array(labeled_array == 0, start, end, fully_connected=False)
#             # print(indices)
#             indices = np.array(indices).T
#             print(labeled_array)
#
#             labeled_array[indices[0], indices[1]] = 1  # 使用标记值1填充路径
#
#     binary_array = (labeled_array != 0).astype(int)
#     return binary_array
#
#
# # 连接组件并显示结果
# connected_array = connect_components(labeled_array, num_features, slices)
# print(type(connected_array[0][0]))
#
# print(connected_array)


import pygame
import math

def draw_rounded_rect(surface, color, rect, corner_radius):
    ''' Draw a rectangle with rounded corners.
    We use anti-aliased circles to make the corners smoother
    '''
    if corner_radius < 0:
        raise ValueError("corner_radius must be >= 0")
    if corner_radius > min(rect.size) / 2:
        raise ValueError("corner_radius must be <= half the rectangle size")

    # The rectangle edges without the corners
    pygame.draw.rect(surface, color, rect.inflate(-2*corner_radius, 0), border_radius=corner_radius)
    pygame.draw.rect(surface, color, rect.inflate(0, -2*corner_radius), border_radius=corner_radius)

    # The corner circles
    corner_rect = pygame.Rect(0, 0, 2 * corner_radius, 2 * corner_radius)
    for corner in (rect.topleft, rect.topright, rect.bottomleft, rect.bottomright):
        corner_rect.center = corner
        pygame.draw.ellipse(surface, color, corner_rect)

# Example usage:
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Define the rectangle and corner radius
rect = pygame.Rect(100, 100, 200, 100)
corner_radius = 20

# Call this function instead of pygame.draw.rect


pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 清屏
    screen.fill((0, 0, 0))

    draw_rounded_rect(screen, (255, 0, 0), rect, corner_radius)

    # 更新屏幕显示
    pygame.time.Clock().tick(60)
    pygame.display.flip()

pygame.quit()
