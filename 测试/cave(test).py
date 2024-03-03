import pygame
import sys

pygame.init()

# 窗口设置
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 加载地图
background = pygame.image.load('D:/pycharm/project/project/3rd_project/picture/map.jpg')  # 替换为你的地图文件路径
bg_rect = background.get_rect()

# 玩家设置
player = pygame.Rect(screen_width // 2, screen_height // 2, 50, 50)  # 玩家初始位置在屏幕中心
player_speed = 5

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 玩家移动控制
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.y -= player_speed
        if player.y < 0:  # 防止玩家移出地图
            player.y = 0
    if keys[pygame.K_DOWN]:
        player.y += player_speed
        if player.y > bg_rect.height - player.height:  # 防止玩家移出地图
            player.y = bg_rect.height - player.height
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
        if player.x < 0:  # 防止玩家移出地图
            player.x = 0
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
        if player.x > bg_rect.width - player.width:  # 防止玩家移出地图
            player.x = bg_rect.width - player.width

    # 摄像机跟随玩家
    camera_x = min(max(player.x - screen_width / 2, 0), bg_rect.width - screen_width)
    camera_y = min(max(player.y - screen_height / 2, 0), bg_rect.height - screen_height)

    # 绘制背景和玩家
    screen.fill(BLACK)
    screen.blit(background, (-camera_x, -camera_y))
    pygame.draw.rect(screen, WHITE, player.move(-camera_x, -camera_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
