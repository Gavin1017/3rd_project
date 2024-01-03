import pygame
import random
from pygame.locals import *
import sys
from noise import snoise2
import numpy as np
import cv2
import math

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Perlin Noise Map")
clock = pygame.time.Clock()


class Player:
    def __init__(self, the_width, the_height):
        self.position = [random.randint(0, 800), random.randint(0, 600)]
        self.width = the_width
        self.height = the_height
        # self.position = [300, 400]
        self.speed = 5
        self.pic = pygame.image.load("picture\\player.png")
        self.rect = self.pic.get_rect()
        self.left_available = True
        self.right_available = True
        self.top_available = True
        self.down_available = True
        self.left_pic = pygame.image.load("picture\\left.png")
        self.right_pic = pygame.image.load("picture\\right.png")
        self.top_pic = pygame.image.load("picture\\top.png")
        self.down_pic = pygame.image.load("picture\\down.png")
        self.shoot_direction = 0

        self.attack = 10  # 基础攻击
        self.defense = 2  # 基础防御
        self.hp = 100
        self.equipments = []

        # self.bullet = bullet

    def move(self, keyup):
        kp = pygame.key.get_pressed()
        # print(self.rect)
        # print(self.position)
        if kp[pygame.K_a] and self.left_available:
            self.position[0] = self.position[0] - self.speed
        if kp[pygame.K_d] and self.right_available:
            self.position[0] = self.position[0] + self.speed
        if kp[pygame.K_s] and self.down_available:
            self.position[1] = self.position[1] + self.speed
        if kp[pygame.K_w] and self.top_available:
            self.position[1] = self.position[1] - self.speed

        if self.position[1] - self.rect.bottom / 2 <= 0:  # top
            self.top_available = False
        else:
            self.top_available = True
        if self.position[1] + self.rect.bottom / 2 >= self.height:  # down
            self.down_available = False
        else:
            self.down_available = True
        if self.position[0] - self.rect.right / 2 <= 0:  # left
            self.left_available = False
        else:
            self.left_available = True
        if self.position[0] + self.rect.right / 2 >= self.width:  # Right
            self.right_available = False
        else:
            self.right_available = True

    def shooting_direction(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.shoot_direction = math.atan2(mouse_y - self.position[1], mouse_x - self.position[0])
        if -(math.pi / 4) <= self.shoot_direction <= (math.pi / 4):
            self.pic = self.right_pic
            self.rect = self.pic.get_rect()
        if (math.pi / 4) <= self.shoot_direction <= (3 * math.pi / 4):
            self.pic = self.down_pic
            self.rect = self.pic.get_rect()
        if (3 * math.pi / 4) <= self.shoot_direction <= math.pi or -math.pi <= self.shoot_direction <= -(
                3 * math.pi / 4):
            self.pic = self.left_pic
            self.rect = self.pic.get_rect()
        if -(3 * math.pi / 4) <= self.shoot_direction <= -(math.pi / 4):
            self.pic = self.top_pic
            self.rect = self.pic.get_rect()

    def calculate_attribute(self):
        for equipment in self.equipments:
            self.attack += equipment.attack
            self.defense += equipment.defense


class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.radius = 5
        self.speed = 5
        self.range = 300
        self.distance = 0

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.distance += self.speed  # 更新移动距离

    def is_out_of_range(self):
        return self.distance >= self.range

    def draw(self, the_screen):
        pygame.draw.circle(the_screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius)

    def change_radius(self, value):
        self.radius = value

    def change_speed(self, value):
        self.speed = value

    def change_range(self, value):
        self.range = value


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.health = 100  # 假设敌人有100点生命值
        self.defence = 2
        self.attack = 10
        self.pic = pygame.image.load("picture\\player.png")
        self.rect = self.pic.get_rect()

    def hit(self, damaged):
        self.health -= damaged-self.defence  # 每次被击中减少10点生命值
        if self.health <= 0:
            return True  # 如果生命值归零，返回True
        return False

    def draw(self, screen1):
        pygame.draw.rect(screen1, (0, 166, 255), (self.x, self.y, self.size, self.size))


    def check_collision(self, bullet):
        # 简单的矩形碰撞检测
        if self.x < bullet.x < self.x + self.size and self.y < bullet.y < self.y + self.size:
            return True
        return False



class Map:
    def __init__(self, the_width, the_height):
        self.width = the_width
        self.height = the_height
        self.cell_map = [[0 for y in range(the_width)] for x in range(the_height)]  # 地形
        self.map_color = [[0 for y in range(the_width)] for x in range(the_height)]  # 地形颜色
        self.river = 0
        self.land = 1
        self.mountain = 2
        self.change = 4

    def generate_noise_map(self, map_width, map_height, scale, octaves, persistence, lacunarity, seed):
        noise_map = [[0 for y in range(map_width)] for x in range(map_height)]
        for x in range(map_height):
            for y in range(map_width):
                sample_x = x / scale
                sample_y = y / scale
                value = snoise2(sample_x, sample_y, octaves=octaves, persistence=persistence,
                                lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=seed)
                noise_map[x][y] = value
        return noise_map

    def delete_small(self, cellmap, mapcolor):
        #  判断cell_map上下左右来决定对应的颜色
        for x in range(len(cellmap)):
            for y in range(len(cellmap[0])):
                if (x >= 5 and y >= 5) and (x <= len(cellmap) - 6 and y >= 5) and (
                        x >= 5 and y <= len(cellmap[0]) - 6) and (
                        x <= len(cellmap) - 6 and y <= len(cellmap[0]) - 6):
                    if cellmap[x][y] == self.change or cellmap[x][y] == self.river:
                        if cellmap[x - 5][y - 5] == self.land and cellmap[x - 5][y - 4] == self.land and cellmap[x - 5][
                            y - 3] == self.land and (
                                cellmap[x - 5][y - 2] == self.land) and cellmap[x - 5][y - 1] == self.land and \
                                cellmap[x - 5][
                                    y] == self.land and (
                                cellmap[x - 5][y + 1] == self.land) and cellmap[x - 5][y + 2] == self.land and \
                                cellmap[x - 5][
                                    y + 3] == self.land and (
                                cellmap[x - 5][y + 4] == self.land) and cellmap[x - 5][y + 5] == self.land and \
                                cellmap[x - 4][
                                    y - 5] == self.land and (
                                cellmap[x - 3][y - 5] == self.land) and cellmap[x - 2][y - 5] == self.land and \
                                cellmap[x - 1][
                                    y - 5] == self.land and (
                                cellmap[x][y - 5] == self.land) and cellmap[x + 1][y - 5] == self.land and \
                                cellmap[x + 2][
                                    y - 5] == self.land and (
                                cellmap[x + 3][y - 5] == self.land) and cellmap[x + 4][y - 5] == self.land and \
                                cellmap[x + 5][
                                    y - 5] == self.land and (
                                cellmap[x - 4][y + 5] == self.land) and cellmap[x - 3][y + 5] == self.land and \
                                cellmap[x - 2][
                                    y + 5] == self.land and cellmap[x - 1][y + 5] == self.land and (
                                cellmap[x][y + 5] == self.land) and cellmap[x + 1][y + 5] == self.land and \
                                cellmap[x + 2][
                                    y + 5] == self.land and (
                                cellmap[x + 3][y + 5] == self.land) and cellmap[x + 4][y + 5] == self.land and \
                                cellmap[x + 5][
                                    y + 5] == self.land and (
                                cellmap[x + 5][y - 5] == self.land) and cellmap[x + 5][y - 4] == self.land and \
                                cellmap[x + 5][
                                    y - 3] == self.land and (
                                cellmap[x + 5][y - 2] == self.land) and cellmap[x + 5][y - 1] == self.land and \
                                cellmap[x + 5][
                                    y] == self.land and (
                                cellmap[x + 5][y + 1] == self.land) and cellmap[x + 5][y + 2] == self.land and \
                                cellmap[x + 5][
                                    y + 3] == self.land and (
                                cellmap[x + 5][y + 4] == self.land):
                            mapcolor[x][y] = (255, 255, 255)

    def render_map(self, noise_map, river_threshold, land_threshold, mountain_threshold):
        for x in range(len(noise_map)):
            for y in range(len(noise_map[0])):
                # color = (int(255 * (noise_map[x][y] + 1) / 2),) * 3
                value = noise_map[x][y]
                if value < river_threshold:
                    color = (0, 0, 255)  # Blue for rivers
                    self.cell_map[x][y] = self.river
                    self.map_color[x][y] = color
                elif value < land_threshold:
                    color = (255, 255, 255)  # White for land
                    self.cell_map[x][y] = self.land
                    self.map_color[x][y] = color
                elif value < mountain_threshold:
                    t = (value - land_threshold) / (mountain_threshold - land_threshold)
                    # print(t)
                    color = (139 * t, 69 * t, 19 * t)  # Smooth transition from white to brown
                    self.cell_map[x][y] = self.change
                    self.map_color[x][y] = color
                else:
                    color = (139, 69, 19)
                    self.cell_map[x][y] = self.mountain
                    self.map_color[x][y] = color

        self.delete_small(self.cell_map, self.map_color)

        map_color_bgr = np.array(self.map_color, dtype=np.uint8)[:, :, ::-1]
        cv2.imwrite("picture\map.jpg", map_color_bgr)


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
    # player_bullet = Bullet()
    player = Player(width, height)
    keydown = ""
    keyup = ""
    player_bullets = []

    # 生成一些敌人
    enemies = [Enemy(100, 100), Enemy(200, 200)]

    # 特定事件
    special_event_triggered = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 1:  # 检测左键点击
            #         mouse_x, mouse_y = pygame.mouse.get_pos()
            #         print(f"Left mouse button clicked at ({mouse_x}, {mouse_y})")
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
                player_bullets.append(Bullet(player.position[0], player.position[1], angle))
            # 按下空格键触发特定事件
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                special_event_triggered = True
        # 如果特定事件被触发，改变所有子弹的属性
        if special_event_triggered:
            for bullet in player_bullets:
                bullet.change_speed(5)  # 增加速度
                bullet.change_radius(10)  # 增加半径


        player.move(keyup)
        player.shooting_direction()

        # 更新子弹
        for bullet in player_bullets[:]:
            bullet.update()
            if bullet.is_out_of_range():
                player_bullets.remove(bullet)

        # 检测敌人和子弹的碰撞
        for bullet in player_bullets[:]:
            for enemy in enemies[:]:
                if enemy.check_collision(bullet):
                    player_bullets.remove(bullet)
                    if enemy.hit(player.attack):  # 如果敌人被击败
                        enemies.remove(enemy)


        screen.fill((0, 0, 0))
        screen.blit(map, (0, 0))
        screen.blit(player.pic,
                    (player.position[0] - player.rect.right / 2, player.position[1] - player.rect.bottom / 2))
        #
        # screen.blit(pygame.transform.smoothscale(player.pic, (int(player_rect[2]), int(player_rect[3])) ),
        #             (player.position[0], player.position[1])) # 放大或者缩小
        # 绘制子弹
        for bullet in player_bullets:
            bullet.draw(screen)
        # 绘制敌人
        for enemy in enemies:
            screen.blit(enemy.pic,
                        (enemy.x - enemy.rect.right / 2, enemy.y - enemy.rect.bottom / 2))
            # enemy.draw(screen)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
