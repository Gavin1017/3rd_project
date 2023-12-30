import random
import pygame
import noise

WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))

def generate_noise(count):

    noise = list()
    for i in range(count):
        noise.append(random.random())
    return noise

def draw_line(pos1,pos2):
    # draw a single line from pos1 to pos2

    pygame.draw.line(screen,(255,0,0),pos1,pos2,1)

heights = [random.randint(0,100) for i in range(11)]
gradients = [random.randint(0,255) for i in range(11)]

def lerp(y1,y2,w):

    return y1 + (y2 - y1) * w

def twist(x):
    # 3t^2 - 2t^3

    return x**2 * (3 - 2 * x)


def twist2(x):
    # 3t^2 - 2t^3

    return x**3 * (6 * x**2 - 15 * x + 10)

def get_noise():

    noise = list()
    pos = list()
    for idx in range(10):
        # print(idx)
        for _x in range(100):
            x = _x/100
            y1 = gradients[idx] * x + heights[idx]
            y2 = gradients[idx + 1] * (x - 1) + heights[idx+1]
            w = twist2(x)
            noise.append(lerp(y1,y2,w))
            pos.append(idx * 100 + _x)
    return noise,pos


noise,pos = get_noise()

print(noise)
print(pos)

def update():
    # 绘制所有的点

    for idx in range(len(noise)):
        screen.set_at((pos[idx],int(noise[idx]) + 200),(255,0,0))

def main_loop():

    while 1:
        screen.fill((255,255,255))
        update()
        pygame.display.flip()
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                exit(0)


main_loop()


