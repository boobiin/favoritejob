import pygame
from settings import Settings
from ship import Ship
from pygame.sprite import Group
import game_functions as gf
from game_stats import GameStats
from button import Button
from Scoreboard import Scoreboard


def run_game():

    # 初始化pygame, 设置和屏幕对象

    # pygame.init() 初始化背景设置
    pygame.init()

    # settings类的实例化
    ai_settings = Settings()

    # pygame.display.set_mode()用于创建一个名字为screen的显示窗口
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))

    # pygame.display.set_caption 设置屏幕标题
    pygame.display.set_caption("Alien Invasion")

    # 创建一个用于统计游戏信息的实例，并且创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建一个用于存储子弹和外星人的编组
    bullets = Group()
    aliens = Group()

    # 创建一个外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 开始游戏的主循环
    while True:

        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets)

        if stats.game_active:
            # 飞船更新状态
            ship.update()

            # 子弹更新状态
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              bullets)

            # 更新外星人状态
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens,
                             bullets)

        # 重绘屏幕, 飞船，并且使屏幕可见
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                         play_button)


run_game()
