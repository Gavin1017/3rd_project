import time

import pygame
import random
from pygame.locals import *
import sys
from noise import snoise2
import numpy as np
import cv2
import math
from scipy.ndimage import label, find_objects
from skimage.graph import route_through_array
from Player import *
from Bullet import *
from Enemy import *
from Map import *
import Map_Maze
import Map_Cave
import random
import Astar

pygame.init()
# width, height = 800, 600
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PCG Game")
clock = pygame.time.Clock()

# 控制键设置
key_settings = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d
}

init_surface = pygame.Surface(screen.get_size())
init_surface.fill((255, 255, 255))
main_surface = pygame.Surface(screen.get_size())

config_surface = pygame.Surface(screen.get_size())

maze_surface = pygame.Surface(screen.get_size())
maze_lines = []

cave_surface = pygame.Surface(screen.get_size())
bomb_list = []
cave_enemy_list = []
fire_list = []

pause_surface = pygame.Surface(screen.get_size())
# init_surface.fill((255,255,255))

congratulation_surface = pygame.Surface(screen.get_size())

failed_surface = pygame.Surface(screen.get_size())


def main():
    # 地图参数
    scale = 150
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0
    seed = random.randint(0, 100)

    the_river_threshold = -0.2  # 用于分类河流的阈值
    the_land_threshold = 0.0  # 用于分类陆地的阈值
    the_mountain_threshold = 0.2  # 用于分类高山的阈值
    noise_map = []

    # 绘制地图
    the_map = Map(width, height)
    noise_map = the_map.generate_noise_map(width, height, scale, octaves, persistence, lacunarity, seed)
    the_map.render_map(noise_map, the_river_threshold, the_land_threshold, the_mountain_threshold)
    map = pygame.image.load("picture\map.jpg")
    # 生成玩家和子弹

    player = Player(width, height)
    keydown = ""
    keyup = ""
    player_bullets = []

    # 生成一些敌人和子弹
    main_enemy_number = random.randint(1, 3)
    # main_enemy_number = 1
    enemies = []
    for x in range(main_enemy_number):
        enemies.append(Enemy(random.randint(100, 1000), random.randint(100, 700), pygame.time.get_ticks()))
    enemy_bullets = []

    # 状态机判断当前实在主地图还是分地图。主地图是0，分地图为1，2，3...
    map_state = 0
    now_state = 0  # 如果暂停，则保存当前状态

    # 声明地图迷宫
    map_maze = ""

    # tick时间
    all_tick = 0
    start_ticks = pygame.time.get_ticks()  # 当前时间

    running = True
    while running:
        all_tick += 1/60
        if map_state == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        now_state = map_state
                        map_state = 3

                if event.type == KEYDOWN:
                    keydown = event.key
                else:
                    keydown = None
                if event.type == KEYUP:
                    keyup = event.key
                else:
                    keyup = None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    angle = math.atan2(mouse_y - player.position[1], mouse_x - player.position[0])
                    player_bullets.append(Bullet(player.position[0], player.position[1], angle, player))

            enemy_positions = []
            for enemy in enemies:
                enemy_positions.append((enemy.x, enemy.y))

            # 判断玩家移动和速度
            player.move(keyup, key_settings)
            player.shooting_direction()

            if the_map.map_color[player.position[1]][player.position[0]] == (0, 0, 255):
                player.speed = 1
            elif the_map.map_color[player.position[1]][player.position[0]] == (255, 255, 255):
                player.speed = 4
            elif the_map.map_color[player.position[1]][player.position[0]] == (139, 69, 19):
                player.speed = 3
            else:
                player.speed = 2
            # print(player.position)


            # 更新子弹
            for bullet in player_bullets[:]:
                bullet.update()
                if bullet.is_out_of_range():
                    player_bullets.remove(bullet)

            for enemy_bullet in enemy_bullets[:]:
                enemy_bullet.update()
                if enemy_bullet.is_out_of_range():
                    enemy_bullets.remove(enemy_bullet)


            break_flag = False
            # 检测敌人和子弹的碰撞
            for bullet in player_bullets[:]:
                for enemy in enemies[:]:
                    if enemy.check_collision(bullet):
                        player_bullets.remove(bullet)
                        enemy.health -= player.attack
                        break

                    if enemy.health <= 0:
                        enemy.health = 100  # 复活
                        map_state = random.randint(1, 2)  # 需要切换random(后面请改成random.randint(1,3))
                        # map_state = 2
                        if map_state == 1:

                            maze_width = 25
                            maze_height = 25
                            map_maze = Map_Maze.Map(maze_width, maze_height, maze_surface, enemy)
                            Map_Maze.doRandomPrim(map_maze)
                            map_maze.picture_scale()
                            map_maze.zero_pos()
                            #  绘制字体
                            font = pygame.font.SysFont(None, 28)

                            # 想要显示的文本
                            full_text = 'The victory condition for this maze is to navigate from the starting point ' \
                                        'in the upper left corner to the destination in the lower right corner. You ' \
                                        'need to find three keys at different locations within the maze for the final ' \
                                        'exit to appear. The entire maze has a time limit; you must complete it ' \
                                        'within one minute. However, each time you obtain a key, an additional ten ' \
                                        'seconds will be added to the clock. Good Luck Have Fun.'

                            # 设置每行的最大像素宽度
                            max_line_width = 250
                            # 分割文本到多行
                            words = full_text.split(' ')
                            maze_lines.clear()
                            current_line = ''

                            # 标题
                            maze_lines.append("            Map Maze")

                            for word in words:
                                # 如果加上新单词后超过了最大宽度，则当前行结束，开始新行
                                if font.size(current_line + word)[0] > max_line_width:
                                    maze_lines.append(current_line.strip())
                                    current_line = word + ' '
                                else:
                                    current_line += word + ' '
                            maze_lines.append(current_line.strip())  # 添加最后一行
                        elif map_state == 2:
                            cave_time = 0
                            cell_size = 15
                            bomb_list = []
                            fire_list = []
                            cave_enemy_list = []
                            bomb_range = 0

                            # cols, rows = width // cell_size, height // cell_size  # cols=80, rows = 60
                            thecave = Map_Cave.Cave(width, height, cell_size, enemy)
                            thecave.initial()
                            thecave.cellular_automaton(5)  # step of the cellular automaton
                            thecave.final_map(10)  # the threshold of the area
                            thecave.connect_components()
                            thecave.block()

                            cave_position = Map_Cave.find_init_position(thecave.unconnected_cave)
                            # print("---------------------")
                            cave_player = Map_Cave.Player(cave_position[1], thecave.matrix, cell_size, cave_surface, cell_size)
                            # print(cave_player.position)
                            enemy_number = random.randint(2, 4) # 记得修改
                            # enemy_number = 1
                            enemy_position_values = list(cave_position.values())[1:]
                            cave_enemy_list_pos = random.choices(enemy_position_values, k=enemy_number)
                            for enemy_pos in cave_enemy_list_pos:
                                cave_enemy_list.append(Map_Cave.Enemy(enemy_pos, thecave.matrix, cell_size, cave_surface, cell_size ))
                        break_flag = True
                        break
                if break_flag == True:
                    break

            for enemy_bullet in enemy_bullets[:]:
                if player.check_collision(enemy_bullet):
                    player.hp -= enemy_bullet.owner.attack
                    enemy_bullets.remove(enemy_bullet)

            main_surface.fill((0, 0, 0))
            main_surface.blit(map, (0, 0))
            main_surface.blit(player.pic,
                              (player.position[0] - player.rect.right / 2, player.position[1] - player.rect.bottom / 2))

            # 绘制子弹
            for bullet in player_bullets:
                bullet.draw(main_surface)

            for enemy_bullet in enemy_bullets:
                enemy_bullet.draw(main_surface)

            # 移动敌人
            current_ticks = pygame.time.get_ticks()
            for enemy in enemies:
                enemy_position = [enemy.x, enemy.y]
                distance = np.linalg.norm(np.array(enemy_position) - np.array(player.position))
                shooting_elapsed_time = current_ticks - enemy.shooting_time
                moving_elapsed_time = current_ticks - enemy.moving_time
                if distance > 500:
                    enemy.random_move(moving_elapsed_time, width, height)
                    if moving_elapsed_time >= 1000:
                        enemy.moving_time = pygame.time.get_ticks()
                elif distance <= 500:

                    if player.position[0] - enemy.x > 150:
                        enemy.pic = enemy.right_pic
                        enemy.x += enemy.speed
                    if player.position[0] - enemy.x < -150:
                        enemy.pic = enemy.left_pic
                        enemy.x -= enemy.speed
                    if player.position[1] - enemy.y > 150:
                        enemy.pic = enemy.down_pic
                        enemy.y += enemy.speed
                    if player.position[1] - enemy.y < -150:
                        enemy.pic = enemy.top_pic
                        enemy.y -= enemy.speed

                    if distance <= 300:
                        if shooting_elapsed_time >= 1000:
                            enemy_angle = math.atan2(player.position[1] - enemy.y, player.position[0] - enemy.x)
                            enemy_bullets.append(Bullet(enemy.x, enemy.y, enemy_angle, enemy))
                            enemy.shooting_time = pygame.time.get_ticks()



                if 0 <= enemy.x < width and 0 <= enemy.y < height:
                    if the_map.map_color[enemy.y][enemy.x] == (0, 0, 255): # 河流
                        enemy.speed = 1
                    elif the_map.map_color[enemy.y][enemy.x] == (255, 255, 255): # 陆地
                        enemy.speed = 4
                    elif the_map.map_color[enemy.y][enemy.x] == (139, 69, 19): # 山
                        enemy.speed = 3
                    else:  # 交汇
                        enemy.speed = 2

            now_main_enemy_number = len(enemies)
            if now_main_enemy_number >= 2:
                for x in range(now_main_enemy_number):
                    if x <= now_main_enemy_number-2:
                        if enemies[x].check_enemy_collision(enemies[x+1]):
                            enemies[x + 1].x += 1
                            enemies[x + 1].y += 1
                            if enemies[x + 1].x >= width:
                                enemies[x + 1].x = width - 1
                            if enemies[x + 1].y >= height:
                                enemies[x + 1].y = width - 1

            # 绘制敌人
            for enemy in enemies:
                main_surface.blit(enemy.pic,
                                  (enemy.x - enemy.rect.right / 2, enemy.y - enemy.rect.bottom / 2))

            if player.hp <= 0:  # 判断血条来跳出是否结束或这重启（未完成）
                # running = False
                map_state = 5
            elif len(enemies) <= 0:
                map_state = 4
                # running = False
            #  展示玩家血条
            max_health = 100
            # 血条位置和尺寸
            bar_width = 200
            bar_height = 20
            bar_x = (width - bar_width) / 2  # 血条水平居中
            bar_y = 10  # 血条距离屏幕顶部的距离
            font = pygame.font.SysFont(None, 30)
            # 绘制血条背景
            pygame.draw.rect(main_surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))

            # 计算当前血量的宽度比例
            health_width = (player.hp / max_health) * bar_width

            # 绘制当前血量
            pygame.draw.rect(main_surface, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))

            # 显示血量文本
            health_text = font.render(f"{player.hp} / {max_health}", True, (255, 0, 0))
            main_surface.blit(health_text, (bar_x + (bar_width / 2) - (health_text.get_width() / 2), bar_y))

            screen.blit(main_surface, (0, 0))
            pygame.display.flip()
            clock.tick(60)
        elif map_state == 1:
            maze_surface.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        now_state = map_state
                        map_state = 3
                # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # 返回到主页面
                #     map_state = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == key_settings['up']:
                        map_maze.move_player('UP')
                    elif event.key == key_settings['down']:
                        map_maze.move_player('DOWN')
                    elif event.key == key_settings['left']:
                        map_maze.move_player('LEFT')
                    elif event.key == key_settings['right']:
                        map_maze.move_player('RIGHT')

            fontline = pygame.font.SysFont(None, 28)
            y = 10  # 初始y坐标
            # 设置每行的最大像素宽度
            max_line_width = 250

            for line in maze_lines:
                title_surface = fontline.render(line, True, (255, 255, 255))
                title_rect = title_surface.get_rect(x=maze_surface.get_width() - max_line_width - 10,
                                                    y=y)
                maze_surface.blit(title_surface, title_rect)
                y += title_rect.height  # 更新y坐标，为下一行腾出空间

            # 绘制迷宫和玩家
            map_maze.draw_maze()
            map_maze.draw_player()
            finish = map_maze.check_finish()

            if finish:
                map_state = 0
                enemies.remove(map_maze.enemy)

            map_maze.time -= 1 / 60
            # map_maze.time = int(map_maze.time)
            # print(int(map_maze.time))
            if int(map_maze.time) <= 0:
                player.hp -= 34  # 如果没有完成，则扣除玩家的hp值
                map_state = 0

            time_str = '{:02d}'.format(int(map_maze.time)) + "s"
            font = pygame.font.SysFont(None, 48)
            text = font.render(time_str, True, (255, 255, 255))

            # text_rect = text.get_rect(x=600, y=500)
            text_rect = text.get_rect()

            right_bottom_x = width * 0.98 - text_rect.width  # 右下角的X位置
            right_bottom_y = height * 0.98 - text_rect.height

            # maze_surface.blit(text, text_rect)
            maze_surface.blit(text, (right_bottom_x, right_bottom_y))


            # 更新屏幕
            screen.blit(maze_surface, (0, 0))
            pygame.display.flip()
            clock.tick(60)

            # map_maze.showMap()
        elif map_state == 2:
            # print(cave_player.position)
            # print("对应的", thecave.matrix[cave_player.position[0], cave_player.position[1]])
            # cave_surface.fill((0, 0, 0))
            # cell_size = 10
            cols, rows = width // cell_size, height // cell_size  # cols=80, rows = 60


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        now_state = map_state
                        map_state = 3

                if event.type == pygame.KEYDOWN:
                    if event.key == key_settings['up']:
                        cave_player.move('UP', bomb_list)
                        # cave_enemy_list[0].move('UP', bomb_list)
                    elif event.key == key_settings['down']:
                        cave_player.move('DOWN', bomb_list)
                        # cave_enemy_list[0].move('DOWN', bomb_list)
                    elif event.key == key_settings['left']:
                        cave_player.move('LEFT', bomb_list)
                        # cave_enemy_list[0].move('LEFT', bomb_list)
                    elif event.key == key_settings['right']:
                        cave_player.move('RIGHT', bomb_list)
                        # cave_enemy_list[0].move('RIGHT', bomb_list)

                    if event.key == pygame.K_j and cave_player.cd <= 0:
                        bomb_position = cave_player.position.copy()
                        bomb_position = (bomb_position[0]*cell_size, bomb_position[1]*cell_size)
                        bomb_list.append(Map_Cave.Bomb(bomb_position, cave_player, cell_size))
                        if 0 <= cave_time < 30:
                            cave_player.cd = 4
                        elif 30 <= cave_time < 60:
                            cave_player.cd = 3.5
                        elif 60 <= cave_time < 120:
                            cave_player.cd = 3
                        else:
                            cave_player.cd = 2.5

            cave_surface.fill((0, 0, 0))

            # 渲染细胞自动机生成的洞穴地图
            for row in range(rows):
                for col in range(cols):

                    if thecave.matrix[row][col] == 0:
                        color = (255, 255, 255)  # 白色路径
                    elif thecave.matrix[row][col] == 1:
                        color = (0, 0, 0)  # 黑色墙壁
                    elif thecave.matrix[row][col] == 2:  # 棕色障碍物
                        color = (165, 42, 42)
                    pygame.draw.rect(cave_surface, color, (col * cell_size, row * cell_size, cell_size, cell_size))
            # screen.blit(cave,(0,0))
            # update the cave surface
            cave_player.draw()

            # 判断无敌帧和炸弹cd
            if cave_player.cd > 0:
                cave_player.cd -= 1/60
            if cave_player.invincible_after_injured > 0:
                cave_player.invincible_after_injured -= 1/60
            # if cave_player.invincible_after_injured > 0:
            #     cave_player.invincible_after_injured -= 1/60
            shuliang = 0
            # 绘制炸弹
            for bomb in bomb_list:
                bomb.draw_before_explosion(cave_surface)
                bomb.remaining_time -= 1 / 60
                if bomb.remaining_time <= 0:
                    bomb_list.remove(bomb)
                    fire_list.append(bomb)
                if 0 <= cave_time < 30:  # 如果大于一定时间，炸弹的范围会变大
                    bomb.range = 1
                    bomb_range = 1
                elif 30 <= cave_time < 60:
                    bomb.range = 2
                    bomb_range = 2
                elif 60 <= cave_time < 120:
                    bomb.range = 3
                    bomb_range = 3
                else:
                    bomb.range = 4
                    bomb_range = 4


            # 每隔一定时间来进行判断敌人移动
            for enemy in cave_enemy_list:
                shuliang +=1
                # print("enemy: "+str(shuliang)+str("  ")+str(enemy.state))
                if enemy.time >= 0.4:  # 判断经过了多少时间，来看是否需要进行计算。
                    enemy.time = 0
                    cave_map = np.copy(enemy.cave)

                    # 炸弹的位置
                    for bomb_pos in bomb_list:
                        # print("炸弹位置：",(bomb_pos.position[0]/bomb_pos.cell_size, bomb_pos.position[1]/bomb_pos.cell_size))
                        cave_map[int(bomb_pos.position[0]/bomb_pos.cell_size)][int(bomb_pos.position[1]/bomb_pos.cell_size)] = 100


                    cave_map[cave_map == 1] = 10000000  # 设置非常大的数值来作为墙壁，a*算法就不会走这条路
                    cave_map[cave_map == 2] = 10  # 障碍物
                    cave_map[cave_map == 0] = 1  # 路
                    start_pos = Astar.Node(enemy.position[0], enemy.position[1])  # 敌人所在位置
                    end_pos = Astar.Node(cave_player.position[0], cave_player.position[1])  # 玩家所在位置
                    distance = Astar.heuristic(start_pos, end_pos)

                    if distance > 0:
                        enemy_player_path = Astar.a_star_search(cave_map, start_pos, end_pos)

                        if enemy.state == 0:
                            if cave_map[enemy_player_path[1][0]][enemy_player_path[1][1]] != 10 and distance >=3:  # 如果下一步不是障碍物
                                # next_action = enemy_player_path[1]
                                enemy_rest = cave_enemy_list.copy()
                                enemy_rest.remove(enemy)
                                has_enemy = False
                                has_bomb = False
                                for x in enemy_rest:
                                    if [enemy_player_path[1][0], enemy_player_path[1][1]] == x.position:
                                        has_enemy = True
                                for y in bomb_list:
                                    if [enemy_player_path[1][0], enemy_player_path[1][1]] == [y.position[0]/y.cell_size,y.position[1]/y.cell_size]:
                                        has_bomb = True
                                if has_enemy!=True and has_bomb!=True:
                                    enemy.next_position = [enemy_player_path[1][0], enemy_player_path[1][1]]
                                    enemy.position = [enemy_player_path[1][0], enemy_player_path[1][1]]
                                elif has_bomb == True:
                                    enemy.state = 2
                                elif has_enemy:
                                    enemy.state = 0

                            elif cave_map[enemy_player_path[1][0]][enemy_player_path[1][1]] == 10 or ((cave_player.position[1] -enemy.position[1] == 0 or cave_player.position[0] - enemy.position[0] == 0) and distance < 5):
                                enemy_bomb_position = enemy.position.copy()
                                enemy_bomb_position = (enemy_bomb_position[0] * cell_size, enemy_bomb_position[1] * cell_size)
                                bomb_list.append(Map_Cave.Bomb(enemy_bomb_position, enemy, cell_size))
                                enemy.last_bomb = bomb_list[-1]

                                enemy.state = 10
                        elif enemy.state == 10 or enemy.state == 2:
                            l = bomb_range+1
                            cx = []
                            cy = []
                            if enemy.state == 10:
                                cx = enemy.position[0]
                                cy = enemy.position[1]
                            elif enemy.state == 2:
                                cx = enemy_player_path[1][0]
                                cy = enemy_player_path[1][1]
                            # 计算正方形所有坐标
                            square_coords = [(x, y) for x in range(cx - l, cx + l + 1) for y in
                                             range(cy - l, cy + l + 1)]

                            # 计算十字形坐标
                            cross_coords = [(cx, y) for y in range(cy - l, cy + l + 1)] + [(x, cy) for x in
                                                                                           range(cx - l, cx + l + 1)]
                            # 去除重复的中心点坐标
                            cross_coords = list(set(cross_coords))

                            # 从正方形坐标中去除十字形坐标，得到除十字外的正方形坐标
                            exclusive_square_coords = [coord for coord in square_coords if coord not in cross_coords]


                            # print("十字坐标：", exclusive_square_coords)
                            # print("--------------")
                            # print("敌人的坐标：", enemy.position)

                            # 长条
                            tem_list = []
                            large_cross_coords = [(cx, y) for y in range(cy - 11, cy + 11 + 1)] + [(x, cy) for x in
                                                                                           range(cx - 11, cx + 11 + 1)]
                            minus_list = list(set(large_cross_coords) - set(cross_coords))

                            all_list = exclusive_square_coords + minus_list
                            # 提前消除大于边界的坐标
                            tem_arr = np.array(all_list)
                            # print("地图类型：",type(enemy.cave))
                            indicesx = (tem_arr[:, 0] >= 0) & (tem_arr[:, 0] < enemy.cave.shape[0])
                            indicesy = (tem_arr[:, 1] >= 0) & (tem_arr[:, 1] < enemy.cave.shape[1])
                            combined_indices = indicesx & indicesy
                            filtered_arr = tem_arr[combined_indices]
                            all_list = list(filtered_arr)

                            for coord in all_list:
                                if enemy.cave[coord[0]][coord[1]] != 1 and enemy.cave[coord[0]][coord[1]] != 2:
                                    tem_list.append(coord)

                            # for coord in exclusive_square_coords:
                            #     if enemy.cave[coord[0]][coord[1]] != 1 and enemy.cave[coord[0]][coord[1]] != 2:
                            #         tem_list.append(coord)
                            # i = 0
                            final_path = []
                            now_pos = Astar.Node(enemy.position[0], enemy.position[1])
                            # goal_pos = Astar.Node(tem_list[0][0], tem_list[0][1])
                            # goal_path = Astar.a_star_search(cave_map, now_pos, goal_pos)
                            # final_path = goal_path

                            # i = 0  # 防止越界
                            for coord in tem_list:
                                i = 0
                                # now_pos = Astar.Node(enemy.position[0], enemy.position[1])
                                goal_pos = Astar.Node(coord[0], coord[1])
                                goal_path = Astar.a_star_search(cave_map, now_pos, goal_pos)
                                goal_path.pop(0)
                                if i == 0:
                                    for check_path in goal_path:
                                        # print("路是什么", cave_map[check_path[0]][check_path[1]])
                                        if cave_map[check_path[0]][check_path[1]] == 10 or cave_map[check_path[0]][check_path[1]] == 10000000 or cave_map[check_path[0]][check_path[1]] == 100:
                                            i = 1

                                if i != 1:
                                    if len(final_path) == 0:
                                        final_path = goal_path
                                        i = 0
                                    elif len(final_path) != 0:
                                        if len(goal_path) <= len(final_path):
                                            final_path = goal_path
                                            i = 0

                            if len(final_path) != 0:
                                enemy.next_position = final_path
                                # next_is_bomb = False
                                # for all_bomb in bomb_list:
                                #
                                #     if [enemy.next_position[0][0], enemy.next_position[0][1]] == [int(all_bomb.position[0]/all_bomb.cell_size),int(all_bomb.position[1]/all_bomb.cell_size)]:
                                #         next_is_bomb = True
                                #
                                # if not next_is_bomb:
                                enemy.position = [enemy.next_position[0][0], enemy.next_position[0][1]]
                                enemy.next_position.pop(0)
                                # print(enemy.next_position)
                                enemy.state = 11
                            else:
                                enemy.next_position = []
                        elif enemy.state == 11:
                            # print(enemy.next_position)
                            if len(enemy.next_position) != 0:
                                enemy.position = [enemy.next_position[0][0], enemy.next_position[0][1]]
                                enemy.next_position.pop(0)
                            else:

                                if enemy.last_bomb.remaining_time + enemy.last_bomb.flame_time<=0:
                                    enemy.state = 0
                enemy.time += 1 / 60

            # 绘制敌人
            for enemy in cave_enemy_list:
                enemy.draw()
                if enemy.invincible_after_injured > 0:
                    enemy.invincible_after_injured -= 1 / 60
                if enemy.hp <=0:
                    cave_enemy_list.remove(enemy)

            # print(cave_time)
            # 绘制爆炸效果
            for fire in fire_list:
                fire.draw_after_explosion(cave_surface)
                fire.flame_time -= 1/60
                who_collided, bomb_owner = fire.check_collision(cave_player, cave_enemy_list)
                thecave.matrix = fire.check_block_collision(thecave.matrix.copy())

                # print("谁被炸了：", len(who_collided))
                # print("谁的炸弹: ", bomb_owner)
                if fire.flame_time <= 0:
                    fire_list.remove(fire)

                for collided in who_collided:
                    if collided.invincible_after_injured <= 0:
                        collided.hp -= bomb_owner.attack
                        collided.invincible_after_injured = 2
            # 判断玩家和敌人的hp值
            if cave_player.hp <= 0:
                map_state = 0
                player.hp -= 50  # 主界面玩家的hp
            if len(cave_enemy_list) <= 0:
                enemies.remove(thecave.enemy)
                map_state = 0

            # 更新敌人内置地图
            for enemy in cave_enemy_list:
                enemy.update_map(thecave.matrix)

            cave_time += 1/60
            cave_player.update_map(thecave.matrix)  #更新玩家地图

            #  展示玩家血条
            max_health = 100
            # 血条位置和尺寸
            bar_width = 200
            bar_height = 20
            bar_x = (width - bar_width) / 2  # 血条水平居中
            bar_y = 10  # 血条距离屏幕顶部的距离
            font = pygame.font.SysFont(None, 30)
            # 绘制血条背景
            pygame.draw.rect(cave_surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))

            # 计算当前血量的宽度比例
            health_width = (cave_player.hp / max_health) * bar_width

            # 绘制当前血量
            pygame.draw.rect(cave_surface, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))

            # 显示血量文本
            health_text = font.render(f"{cave_player.hp} / {max_health}", True, (255, 0, 0))
            cave_surface.blit(health_text, (bar_x + (bar_width / 2) - (health_text.get_width() / 2), bar_y))



            screen.blit(cave_surface, (0, 0))
            clock.tick(60)
            pygame.display.flip()
        elif map_state == 3:
            pause_surface.fill((0, 0, 0))

            font = pygame.font.Font(None, 36)
            black = (0, 0, 0)
            white = (255, 255, 255)
            red = (255, 0, 0)
            dark_red = (200, 0, 0)
            def draw_button(text, center, mouse_pos, default_color=black, hover_color=red):
                text_render = font.render(text, True, white)
                text_rect = text_render.get_rect(center=center)
                button_color = hover_color if text_rect.collidepoint(mouse_pos) else default_color
                pygame.draw.rect(pause_surface, button_color, text_rect.inflate(20, 10))  # 绘制带有padding的按钮背景
                pause_surface.blit(text_render, text_rect)
                return text_rect

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
            title_text = font.render('Pause', True, white)
            title_rect = title_text.get_rect(center=(width / 2, 100))
            pause_surface.blit(title_text, title_rect)
            mouse_pos = pygame.mouse.get_pos()

            start_button_rect = draw_button('Continue', (width / 2, 250), mouse_pos, black, dark_red)

            quit_button_rect = draw_button('Main Menu', (width / 2, 300), mouse_pos, black, dark_red)

            exit_button_rect = draw_button('Exit', (width / 2, 350), mouse_pos, black, dark_red)

            if start_button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    pygame.time.wait(500)
                    map_state = now_state
            if quit_button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    pygame.time.wait(500)
                    break
            if exit_button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    pygame.quit()
                    sys.exit()

            # show_pause_menu(pause_surface)

            screen.blit(pause_surface, (0,0))
            clock.tick(60)
            pygame.display.update()

        elif map_state == 4:
            congratulation_surface.fill((0, 0, 0))
            font = pygame.font.SysFont(None, 55)
            text = font.render("Congratulation!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width / 2, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()

            congratulation_surface.blit(text, text_rect)

            def draw_button(text, center, mouse_pos, default_color=(0,0,0), hover_color=(255, 0, 0)):
                text_render = font.render(text, True, (255, 255, 255))
                text_rect = text_render.get_rect(center=center)
                button_color = hover_color if text_rect.collidepoint(mouse_pos) else default_color
                pygame.draw.rect(congratulation_surface, button_color, text_rect.inflate(20, 10))  # 绘制带有padding的按钮背景
                congratulation_surface.blit(text_render, text_rect)
                return text_rect

            mouse_pos = pygame.mouse.get_pos()
            # 绘制结束游戏按钮，并检测鼠标悬停
            mainmenu_button_rect = draw_button('Main Menu', (width / 2, 300), mouse_pos, (0, 0, 0), (200, 0, 0))
            quit_button_rect = draw_button('Finish', (width / 2, 350), mouse_pos, (0,0,0), (200, 0, 0))


            if quit_button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    pygame.quit()
                    sys.exit()

            if mainmenu_button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    running =False
                    pygame.time.wait(500)

            screen.blit(congratulation_surface, (0, 0))
            clock.tick(60)
            pygame.display.update()

        elif map_state == 5:
            failed_surface.fill((0, 0, 0))
            font = pygame.font.SysFont(None, 55)
            text = font.render("Failed...Try again!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width / 2, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()

            failed_surface.blit(text, text_rect)

            def draw_button(text, center, mouse_pos, default_color=(0, 0, 0), hover_color=(255, 0, 0)):
                text_render = font.render(text, True, (255, 255, 255))
                text_rect = text_render.get_rect(center=center)
                button_color = hover_color if text_rect.collidepoint(mouse_pos) else default_color
                pygame.draw.rect(failed_surface, button_color, text_rect.inflate(20, 10))  # 绘制带有padding的按钮背景
                failed_surface.blit(text_render, text_rect)
                return text_rect

            mouse_pos = pygame.mouse.get_pos()
            # 绘制结束游戏按钮，并检测鼠标悬停
            mainmenu_button_rect = draw_button('Main Menu', (width / 2, 300), mouse_pos, (0, 0, 0), (200, 0, 0))
            quit_button_rect = draw_button('Finish', (width / 2, 350), mouse_pos, (0, 0, 0), (200, 0, 0))

            if quit_button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    pygame.quit()
                    sys.exit()

            if mainmenu_button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    running = False
                    pygame.time.wait(500)

            screen.blit(failed_surface, (0, 0))
            clock.tick(60)
            pygame.display.update()



def init():
    menu = True
    # 设置屏幕大小
    # width, height = 800, 600
    # screen = pygame.display.set_mode((width, height))

    # 设置颜色
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    dark_red = (200, 0, 0)
    grey = (100, 100, 100)
    light_grey = (200, 200, 200)

    # 设置字体
    font = pygame.font.Font(None, 36)

    def change_key(setting_key):
        screen.fill(black)
        waiting_text = font.render(f'Press new key for {setting_key}...', True, white)
        screen.blit(waiting_text, (100, 100))

        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_settings.values():
                        # 如果已经被使用，显示一条消息并重新请求输入
                        error_text = font.render('Error: Key already used!', True, white)
                        screen.blit(error_text, (100, 150))
                        pygame.display.update()
                        pygame.time.wait(1500)  # 等待1.5秒以便玩家阅读消息
                        # change_key(setting_key)  # 重新请求新键
                    else:
                        key_settings[setting_key] = event.key
                        waiting_for_key = False
            clock.tick(60)
            pygame.display.update()

    def draw_button(text, center, mouse_pos,  default_color=black, hover_color=red):
        text_render = font.render(text, True, white)
        text_rect = text_render.get_rect(center=center)
        button_color = hover_color if text_rect.collidepoint(mouse_pos) else default_color
        pygame.draw.rect(screen, button_color, text_rect.inflate(20, 10))  # 绘制带有padding的按钮背景
        screen.blit(text_render, text_rect)
        return text_rect

    def draw_clickable_text(text, position, mouse_pos, is_hovering):
        # config_surface.fill(black)
        color = light_grey if is_hovering else grey
        text_render = font.render(text, True, white)
        text_rect = text_render.get_rect(topleft=position)
        pygame.draw.rect(screen, color, text_rect.inflate(20, 10))
        screen.blit(text_render, position)
        return text_rect

    def settings_menu():
        running = True
        while running:
            # init_surface.fill(black)
            screen.fill(black)


            mouse_pos = pygame.mouse.get_pos()

            # 显示和修改当前控制键
            for i, (k, v) in enumerate(key_settings.items()):
                key_name = pygame.key.name(v)
                text = f'{k.capitalize()}: {key_name}'
                is_hovering = draw_clickable_text(text, (100, 50 + i * 50), mouse_pos,draw_clickable_text(text, (100, 50 + i * 50), mouse_pos,
                                                                      False).collidepoint(mouse_pos)).collidepoint(mouse_pos)
                if is_hovering and pygame.mouse.get_pressed()[0]:
                    change_key(k)
                    # pygame.time.wait(500)

                text_render = font.render(text, True, white)
                config_surface.blit(text_render, (100, 50 + i * 50))

            # 绘制返回按钮
            back_button_rect = draw_button('Back', (width - 150, height - 50), mouse_pos , grey, red)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and back_button_rect.collidepoint(mouse_pos):
                    running = False
            # 这里可以添加更多设置选项
            clock.tick(60)
            init_surface.blit(config_surface, (0, 0))
            pygame.display.update()

    while menu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(black)
        # init_surface.fill(black)  # 设置背景颜色

        # 绘制标题
        title_text = font.render('Procedural Content Generation', True, white)
        title_rect = title_text.get_rect(center=(width / 2, 100))
        screen.blit(title_text, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        # 绘制开始游戏按钮，并检测鼠标悬停
        start_button_rect = draw_button('Start', (width / 2, 250), mouse_pos, black, dark_red)

        # 绘制设置按钮，并检测鼠标悬停
        config_button_rect = draw_button('Config', (width / 2, 300), mouse_pos, black, dark_red)

        # 绘制结束游戏按钮，并检测鼠标悬停
        quit_button_rect = draw_button('Finish', (width / 2, 350), mouse_pos, black, dark_red)

        # 检测鼠标点击
        if start_button_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1:
                screen.fill(black)
                main()

                # menu = False  # 或者切换到游戏场景
        if config_button_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1:
                settings_menu()

        if quit_button_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1:
                pygame.quit()
                sys.exit()

        # screen.blit(init_surface,(0,0))
        clock.tick(60)
        pygame.display.update()


if __name__ == "__main__":
    init()
    # main()
