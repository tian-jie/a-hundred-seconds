import math
import pygame


class bullet(pygame.sprite.Sprite):
    def __init__(self, posx: int= 100, posy: int = 100, stepps = 100, angle = 60, color = (255, 0, 255), speedRate = 1, board_size = (600, 600)) :
        pygame.sprite.Sprite.__init__(self)

        self.posx: int = posx
        self.posy: int = posy
        self.stepps = stepps
        self.angle = angle
        self.color = color
        self.speedRate = speedRate
        self.board_size = board_size
        self.rect = pygame.Rect(posx, posy, 2, 2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), 5, 5)

    def 计算(self, timespan):
        step = timespan * self.stepps / 1000.0
        radians = math.radians(self.angle)
        stepy = step * math.sin(radians) * self.speedRate
        stepx = step * math.cos(radians) * self.speedRate
        
        self.posx = (self.posx + stepx) % self.board_size[0]
        self.posy = (self.posy + stepy) % self.board_size[1]
        if(self.posx < 0):
            self.posx = self.board_size[0]-1
        if(self.posy < 0):
            self.posy = self.board_size[1]-1
        self.rect = pygame.Rect(self.posx, self.posy, 10, 10)
