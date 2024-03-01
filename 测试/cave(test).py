import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置颜色
black = (0, 0, 0)
white = (255, 255, 255)
grey = (100, 100, 100)
light_grey = (200, 200, 200)

# 设置字体
font = pygame.font.Font(None, 36)

# 控制键设置
key_settings = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT
}

# 修改键位的函数
def change_key(setting_key):
    screen.fill(black)
    waiting_text = font.render(f'Press new key for {setting_key}...', True, white)
    screen.blit(waiting_text, (100, 100))
    pygame.display.update()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key_settings[setting_key] = event.key
                waiting_for_key = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# 绘制可点击文本
def draw_clickable_text(text, position, mouse_pos, is_hovering):
    color = light_grey if is_hovering else grey
    text_render = font.render(text, True, white)
    text_rect = text_render.get_rect(topleft=position)
    pygame.draw.rect(screen, color, text_rect.inflate(20, 10))
    screen.blit(text_render, position)
    return text_rect

# 绘制按钮并返回其rect
def draw_button(text, center, mouse_pos, color=black):
    text_render = font.render(text, True, white)
    text_rect = text_render.get_rect(center=center)
    pygame.draw.rect(screen, color, text_rect.inflate(20, 10))  # 绘制按钮背景
    screen.blit(text_render, text_rect)
    return text_rect

# 设置界面
def settings_menu():
    running = True
    while running:
        screen.fill(black)
        mouse_pos = pygame.mouse.get_pos()

        # 显示和修改当前控制键
        for i, (k, v) in enumerate(key_settings.items()):
            key_name = pygame.key.name(v)
            text = f'{k.capitalize()}: {key_name}'
            is_hovering = draw_clickable_text(text, (100, 50 + i*50), mouse_pos, draw_clickable_text(text, (100, 50 + i*50), mouse_pos, False).collidepoint(mouse_pos)).collidepoint(mouse_pos)
            if is_hovering and pygame.mouse.get_pressed()[0]:
                change_key(k)
                pygame.time.wait(500)  # 防止立即捕捉到鼠标点击作为按键

        back_button_rect = draw_button('返回主菜单', (screen_width - 150, screen_height - 50), mouse_pos, grey)
        if back_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
# 主菜单
def main_menu():
    menu = True
    while menu:
        screen.fill(black)
        mouse_pos = pygame.mouse.get_pos()

        settings_button_rect = draw_button('config', (screen_width / 2, screen_height / 2), mouse_pos, grey)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and settings_button_rect.collidepoint(mouse_pos):
                settings_menu()

        pygame.display.update()

main_menu()
