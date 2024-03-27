import random
import sys
import time

import numpy as np
import pygame

from bullet import bullet
from player import Player

class ManInsistGame():
    def __init__(self, enemyCount = 20, speedRate = 1, board_size = (1000, 1000), silentMode = False, seed = 0):
        # 初始化Pygame
        pygame.init()

        # 加载图片
        # images = []
        # for i in range(10):
        #     img = pygame.image.load(str(i)+"-fococlipping-standard.png")
        #     img.get_rect().center = (400, 300)
        #     images.insert(i, img)

        self.敌人数量 = enemyCount
        self.屏幕宽度 = board_size[0]
        self.屏幕高度 = board_size[1]
        self.silentMode = silentMode
        if not silentMode:
            self.font01 = pygame.font.Font("AlibabaHealthFont2.0CN-45R.ttf", 80)
            self.font02 = pygame.font.Font("AlibabaHealthFont2.0CN-45R.ttf", 30)
            self.font03 = pygame.font.Font("AlibabaHealthFont2.0CN-45R.ttf", 70)
        self.speedRate = speedRate
        self.bullets = []
        
        self.status = "ready"
        self.seed_value = seed

        random.seed(seed) # Set random seed.

        # 创建窗口
        if(not self.silentMode):
            self.screen = pygame.display.set_mode(board_size)
        
        self.reset()

    def reset(self):
        self.running = True
        self.status = "ready"
        self.gameDuration = 0
        self.bullets.clear()
        self.all_sprites = pygame.sprite.Group()
        # 初始化子弹
        for i in range(self.敌人数量):
            newBullet = bullet(0, random.randint(10, self.屏幕宽度-10), 150, random.randint(0, 360), color=(255, 255, 255), speedRate=self.speedRate, board_size=(self.屏幕宽度, self.屏幕高度))
            self.bullets.append(newBullet)
            self.all_sprites.add(newBullet)

        # 初始化游戏控制的人
        self.player = Player(stepps = 100, color = (255, 0, 0), speedRate=self.speedRate, screenWidth=self.屏幕宽度, screenHeight=self.屏幕高度)


    def step(self, timespan, action):
        self.status = "playing"
        self.gameDuration += timespan
        running = True

        for i in range(self.敌人数量):
            self.bullets[i].计算(timespan)

        self.player.计算(timespan= timespan, key=action)

        info ={
            "player_pos": np.array((self.player.posx, self.player.posy)),
            "game_duration": self.gameDuration,
            # "is_success": running
        }

        return info
    
    def render(self):
        if(self.silentMode):
            return
        
        self.screen.fill((0,0,0))
        self.player.draw(self.screen)
        for i in range(self.敌人数量):
            self.bullets[i].draw(self.screen)

        # 更新窗口显示
        pygame.display.flip()
        
        # 碰撞检测
        self.all_sprites.update()
        if pygame.sprite.spritecollideany(self.player, self.all_sprites):
            running = False
            self.status = "gameover"
            # print("碰撞了！坚持的秒数：" + str(self.gameDuration*self.speedRate/1000))


    def drawReady(self, key):
        # 按下F1按键开始游戏
        if key[pygame.K_F1]:
            self.status = "playing"
        
        self.screen.fill((0,0,0))
        surface1 =  self.font01.render("按下F1开始游戏", True, (255,255,0))
        self.screen.blit(surface1, ((self.屏幕宽度 - surface1.get_width())/2, (self.屏幕高度 - surface1.get_width())/3))
        pygame.display.flip()


    def drawGameover(self, key):
        self.screen.fill((0,0,0))

        surface1 =  self.font01.render("游戏结束", True, (255,255,0))
        self.screen.blit(surface1, ((self.屏幕宽度 - surface1.get_width())/2, 100))
        surface2 = self.font02.render("你坚持了 ", True, (255,255,0))
        surface3 = self.font03.render(str(self.gameDuration * self.speedRate /1000), True, (255,0,0))
        surface4 = self.font02.render("秒", True, (255,255,0))
        surface2Width = surface2.get_width()
        surface3Width = surface3.get_width()
        surface4Width = surface4.get_width()
        surface2Left = (self.屏幕宽度-surface2Width-surface3Width-surface4Width - 20)/2
        surface3Left = surface2Left+surface2Width
        surface4Left = surface3Left + surface3Width + 20
        self.screen.blit(surface2, (surface2Left, 400))
        self.screen.blit(surface3, (surface3Left, 360))
        self.screen.blit(surface4, (surface4Left, 400))
        # 更新窗口显示
        pygame.display.flip()

        # 按下F1按键开始游戏
        if key[pygame.K_F1]:
            self.reset()
            self.status = "playing"
        

if __name__ == "__main__":

    game = ManInsistGame(board_size=(800, 800), enemyCount=100, silentMode=False)
    game.reset()
    
    timer = pygame.time.Clock()

    last100FrameTime = pygame.time.get_ticks()-10
    lastFrameTime = pygame.time.get_ticks()
    startTime = lastFrameTime
    frame = 0
    fps=60

    # 创建主循环
    while True:

        currentTime = pygame.time.get_ticks()
        timeDiff = currentTime - lastFrameTime
        #gameDuration = (currentTime - startTime) * self.speedRate
        
        key = pygame.key.get_pressed()

        if game.status == "ready":
            game.drawReady(key)
        elif game.status == "gameover":
            game.drawGameover(key)
        elif game.status == "playing":
            action = 0
            if key[pygame.K_w]:
                action = 1
            if key[pygame.K_s]:
                action = 2
            if key[pygame.K_a]:
                action = 3
            if key[pygame.K_d]:
                action = 4
            done, info = game.step(timeDiff, action)
            if done:
                print("碰撞了！坚持的秒数：" + str(game.gameDuration*game.speedRate/1000))
                game.status = "gameover"

            game.render()
        # 根据过去100帧计算平均帧率
        if frame%fps == 0:
            pygame.display.set_caption("fps: "+str(int(fps*1000/(currentTime-last100FrameTime))))
            last100FrameTime = currentTime
        lastFrameTime = currentTime
        frame = frame + 1

        timer.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

