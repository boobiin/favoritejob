import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船并获取其外接矩形
        self.image = pygame.image.load(
            'D:\\python\\alien_invasion\\images\\ship.bmp')
        self.rect = self.image.get_rect()

        # screen的外接矩形确定位置
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center中存储最小数值（即中心初始位置）
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        # 移动标志,和key_down key_up联用
        # 如果监测到 key_down事件，则置moving_right为 true
        # 否则,置为false
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """根据移动标志调整飞船的位置"""
        # 加上屏幕边缘判断条件
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        if self.moving_up and self.rect.bottom > 48:
            self.bottom -= self.ai_settings.ship_speed_factor
        
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.ai_settings.ship_speed_factor

        # 根据self.center更新rect对象
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def blitme(self):
        """在指定位置绘制飞船"""
        # 根据self.rect 指定的位置将图像绘制到屏幕上
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom