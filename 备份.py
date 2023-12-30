import pygame
import random
from noise import snoise2

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Perlin Noise Map")
clock = pygame.time.Clock()

river_threshold = -0.2  # 用于分类河流的阈值
land_threshold = 0.0  # 用于分类陆地的阈值
mountain_threshold = 0.2  # 用于分类高山的阈值

cell_map = [[0 for y in range(height)] for x in range(width)]

# river = 0
# land = 1
# mountain = 2
# change = 4


def generate_noise_map(map_width, map_height, scale, octaves, persistence, lacunarity, seed):
    noise_map = [[0 for y in range(map_height)] for x in range(map_width)]
    for x in range(map_width):
        for y in range(map_height):
            sample_x = x / scale
            sample_y = y / scale
            value = snoise2(sample_x, sample_y, octaves=octaves, persistence=persistence,
                            lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=seed)
            noise_map[x][y] = value

    return noise_map


def interpolate(a, b, t):
    return a * (1 - t) + b * t


def render_map(map_screen, noise_map):
    for x in range(len(noise_map)):
        for y in range(len(noise_map[0])):
            # color = (int(255 * (noise_map[x][y] + 1) / 2),) * 3

            value = noise_map[x][y]
            if value < river_threshold:
                color = (0, 0, 255)  # Blue for rivers
                # cell_map[x][y] = river
            elif value < land_threshold:

                color = (255, 255, 255)  # White for land
                # cell_map[x][y] = land
            elif value < mountain_threshold:
                t = (value - land_threshold) / (mountain_threshold - land_threshold)
                # print(t)
                color = (139 * t, 69 * t, 19 * t)  # Smooth transition from white to brown
                # cell_map[x][y] = change
            else:
                color = (139, 69, 19)
                # cell_map[x][y] = mountain

            pygame.draw.rect(map_screen, color, (x, y, 1, 1))


def main():
    scale = 150
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0
    seed = random.randint(0, 100)

    noise_map = generate_noise_map(width, height, scale, octaves, persistence, lacunarity, seed)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 检测左键点击
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    print(f"Left mouse button clicked at ({mouse_x}, {mouse_y})")

        screen.fill((0, 0, 0))
        render_map(screen, noise_map)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
