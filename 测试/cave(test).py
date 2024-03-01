import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
def show_pause_menu(screen):
    font = pygame.font.Font(None, 36)
    text_surface = font.render('Paused - Press C to Continue, Q to Quit', True, (255, 255, 255))
    x = (screen.get_width() - text_surface.get_width()) / 2
    y = (screen.get_height() - text_surface.get_height()) / 2
    screen.blit(text_surface, (x, y))
    pygame.display.flip()


running = True
paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
            elif event.key == pygame.K_c and paused:
                paused = False
            elif event.key == pygame.K_q and paused:
                running = False

    if paused:
        show_pause_menu(screen)
    else:
        screen.fill((0, 0, 0))  # 游戏的其他绘图逻辑
        # 在这里添加游戏的绘制逻辑
        pygame.display.flip()

    clock.tick(60)  # 控制游戏循环速率

pygame.quit()
