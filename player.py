import math
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, stepps = 100, color = (255, 0, 255), screenWidth =500, screenHeight=500, speedRate = 1):
        pygame.sprite.Sprite.__init__(self)

        self.posx: int = screenWidth//2
        self.posy: int = screenHeight//2
        self.stepps = stepps
        self.color = color
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.rect = pygame.Rect(self.posx, self.posy, 2, 2)
        self.speedRate = speedRate

        # self.image = pygame.image.load("0-fococlipping-standard.png")
        # self.image = pygame.transform.scale(self.image, (self.image.get_width() * 0.4, self.image.get_height() * 0.4))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), 5, 5)
        #screen.blit(self.image, (self.posx, self.posy))

    def 计算(self, timespan, key):
        step = timespan * self.stepps / 1000.0
        stepx = 0
        stepy = 0
        x轴移动 = 0
        y轴移动 = 0
        if key == 1:
            y轴移动 = -1
        elif key == 2:
            y轴移动 = 1
        elif key == 3:
            x轴移动 = -1
        elif key == 4:
            x轴移动 = 1
        
        if x轴移动!=0 and y轴移动!=0:
            # 如果两个轴都移动了，速度不能叠加，要按照等腰直角三角形的形式，斜边的速度要减到和直角边长度一样
            stepx = math.sqrt((step * step)/2) * x轴移动
            stepy = math.sqrt((step * step)/2) * y轴移动
        elif x轴移动!=0 or y轴移动!=0:
            stepx = step * x轴移动
            stepy = step * y轴移动
        self.posx = (self.posx + stepx * self.speedRate) % self.screenWidth
        self.posy = (self.posy + stepy * self.speedRate) % self.screenHeight
        self.rect = pygame.Rect(self.posx, self.posy, 10, 10)
        # print(key, self.posx, self.posy)
