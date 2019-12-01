import pygame
import time
import random

_display = pygame.display


class MainGame(object):
    screen_width = 1000  # 游戏界面宽度
    screen_height = 600  # 游戏界面的高度
    Player = 1
    Tank_p1 = None  # 坦克对象
    Tank_p2 = None
    Base = None
    window = None  # 窗口对象
    EnemyTank_list = []
    Level = 1  # 关卡
    P1_bullet_list = []  # p1子弹列表
    P2_bullet_list = []  # p2
    EnemyTank_bullet_list = []
    Brick_list = []
    Iron_list = []
    Grass_list = []

    def __init__(self):
        self.bblit = Blit()
        self.creatItem = CreatItem()
        self.evenCtrl = EventCtrl()
        self.initScreen()

    def initScreen(self):  # 初始界面
        pygame.init()
        MainGame.window = _display.set_mode([MainGame.screen_width, MainGame.screen_height])
        pygame.display.set_caption("Battle Tank")
        init_image = pygame.image.load("img/init.png")
        select_image = pygame.transform.smoothscale(pygame.image.load("IMG/Select.png"), (50, 50))
        title_image = pygame.image.load("IMG/BATTLETANK.jpg")
        single_player_image = pygame.image.load("IMG/SINGLE.jpg")
        double_player_image = pygame.image.load("IMG/DOUBLE.jpg")
        setting_image = pygame.image.load("IMG/SETTING.jpg")
        MainGame.window.blit(init_image, (0, 0))
        MainGame.window.blit(title_image, (280, 120))
        MainGame.window.blit(select_image, (350, 300))
        MainGame.window.blit(select_image, (350, 380))
        MainGame.window.blit(select_image, (350, 460))
        MainGame.window.blit(single_player_image, (420, 300))
        MainGame.window.blit(double_player_image, (420, 380))
        MainGame.window.blit(setting_image, (420, 460))
        pygame.display.flip()
        while True:
            event = self.evenCtrl.getInitEvent()
            if event == 1 or event == 2:
                self.startGame()
            elif event == 3:
                self.gameSetting()
            time.sleep(0.01)
            _display.update()

    def startGame(self):  # 游戏界面
        Music().palyGroundMusic()
        self.start_time = time.time()
        self.creatItem.creatEnemyTank()
        self.creatItem.creatMyTank(MainGame.Player)
        self.creatItem.creatBrick()
        self.creatItem.creatIron()
        self.creatItem.creatGrass()
        self.creatItem.creatBase()

        while True:
            MainGame.window.fill(pygame.Color(0, 0, 0))
            if self.Base.alive is False or (self.Tank_p1.hp == 0 and self.Tank_p2.hp == 0):
                self.gameOver()
            if self.Tank_p1 and self.Tank_p1.hp != 0:
                self.Tank_p1.displayTank()
            if self.Tank_p2 and self.Tank_p2.hp != 0:
                self.Tank_p2.displayTank()

            if self.Tank_p1 and not self.Tank_p1.stop:
                self.Tank_p1.move()
                self.Tank_p1.hitBrick()
                self.Tank_p1.hitIron()
                self.Tank_p1.hitEnemyTank()
            if self.Tank_p2 and not self.Tank_p2.stop:
                self.Tank_p2.move()
                self.Tank_p2.hitBrick()
                self.Tank_p2.hitIron()
                self.Tank_p2.hitEnemyTank()
            self.bblit.blitEnemyTank()
            self.evenCtrl.getGameEvent()
            self.bblit.blitBrick()
            self.bblit.blitIron()
            self.bblit.blitBase()
            self.bblit.blitEnemyBullet()
            self.bblit.blitMyBullet()
            self.bblit.blitGrass()
            if len(self.EnemyTank_list) == 0:
                self.nextGame()
            time.sleep(0.008)
            _display.update()  # 获取更新

    def nextGame(self):
        end_time = time.time()
        MainGame.window.fill(pygame.Color(0, 0, 0))
        init_image = pygame.image.load("img/init.png")
        level_image = pygame.image.load("img/msg.jpg")
        time_image = pygame.image.load("img/time.jpg")
        MainGame.window.blit(init_image, (0, 0))
        MainGame.window.blit(level_image, (350, 200))
        MainGame.window.blit(time_image, (350, 370))
        level_font = pygame.font.SysFont("华文行楷", 55)
        level_fmt = level_font.render(str(self.Level), True, (227, 227, 227))
        MainGame.window.blit(level_fmt, (500, 200))
        time_font = pygame.font.SysFont("华文行楷", 50)
        time_fmt = time_font.render(str(int(end_time - self.start_time)), True, (227, 227, 227))
        MainGame.window.blit(time_fmt, (470, 370))
        pygame.display.flip()
        while True:
            time.sleep(1)
            self.Level += 1
            self.startGame()

    def gameOver(self):  # 结算界面
        print("游戏结束")
        MainGame.window.fill(pygame.Color(0, 0, 0))
        Music().playEndMusic()
        pain_image = pygame.image.load("img/pain.png")
        MainGame.window.blit(pain_image, (0, 0))
        pygame.display.flip()
        time.sleep(5)
        MainGame.window.fill(pygame.Color(0, 0, 0))
        init_image = pygame.image.load("img/init.png")
        MainGame.window.blit(init_image, (0, 0))
        gameover_image = pygame.image.load("IMG/Gameover.jpg")
        level_over_image = pygame.image.load("IMG/LevelSum.jpg")
        MainGame.window.blit(gameover_image, (350, 200))
        MainGame.window.blit(level_over_image, (350, 370))
        level_font = pygame.font.SysFont("华文行楷", 55)
        level_fmt = level_font.render(str(self.Level - 1), True, (227, 227, 227))
        MainGame.window.blit(level_fmt, (630, 370))
        pygame.display.flip()
        while True:
            self.evenCtrl.getOverEvent()
            time.sleep(0.01)
            _display.update()

    def gameSetting(self):
        print("游戏设置")
        MainGame.window.fill(pygame.Color(0, 0, 0))
        init_image = pygame.image.load("img/init.png")
        MainGame.window.blit(init_image, (0, 0))
        title_image = pygame.image.load("IMG/BATTLETANK.jpg")
        select_image = pygame.transform.smoothscale(pygame.image.load("IMG/Select.png"), (50, 50))
        openmusic_image = pygame.image.load("IMG/openmusic.jpg")
        closemusic_image = pygame.image.load("IMG/closemusic.jpg")
        return_image = pygame.image.load("IMG/return.jpg")
        MainGame.window.blit(init_image, (0, 0))
        MainGame.window.blit(title_image, (280, 120))
        MainGame.window.blit(select_image, (350, 300))
        MainGame.window.blit(select_image, (350, 380))
        MainGame.window.blit(select_image, (350, 460))
        MainGame.window.blit(openmusic_image, (420, 300))
        MainGame.window.blit(closemusic_image, (420, 380))
        MainGame.window.blit(return_image, (420, 460))
        pygame.display.flip()
        while True:
            if self.evenCtrl.getSettingEvent() == 3:
                self.initScreen()
            time.sleep(0.01)
            _display.update()


class EventCtrl:
    def getInitEvent(self):
        self.eventlist = pygame.event.get()
        for event in self.eventlist:
            if event.type == pygame.QUIT:
                print("退出游戏")
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x in range(420, 620) and y in range(300, 350):
                    print("单人游戏")
                    MainGame.Player = 1
                    return 1
                elif x in range(420, 620) and y in range(380, 430):
                    print("双人游戏")
                    MainGame.Player = 2
                    return 2
                elif x in range(420, 515) and y in range(460, 510):
                    print("设置")
                    return 3
        return 0

    def getGameEvent(self):  # 获取所有事件
        self.eventlist = pygame.event.get()
        for event in self.eventlist:
            if event.type == pygame.QUIT:
                print("退出游戏")
                exit()
            if event.type == pygame.KEYUP:  # 键盘按钮抬起 上下左右
                if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w or event.key == pygame.K_s:
                    if MainGame.Tank_p1 and MainGame.Tank_p1.alive:
                        MainGame.Tank_p1.stop = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP \
                        or event.key == pygame.K_DOWN:
                    if MainGame.Tank_p2 and MainGame.Tank_p2.alive:
                        MainGame.Tank_p2.stop = True

            if event.type == pygame.KEYDOWN:  # 事件类型为按下
                if MainGame.Tank_p1 and MainGame.Tank_p1.alive:
                    if event.key == pygame.K_a:  # 左
                        MainGame.Tank_p1.direction = "L"
                        MainGame.Tank_p1.stop = False
                    if event.key == pygame.K_d:
                        MainGame.Tank_p1.direction = "R"
                        MainGame.Tank_p1.stop = False
                    if event.key == pygame.K_w:
                        MainGame.Tank_p1.direction = "U"
                        MainGame.Tank_p1.stop = False
                    if event.key == pygame.K_s:
                        MainGame.Tank_p1.direction = "D"
                        MainGame.Tank_p1.stop = False
                    if event.key == pygame.K_SPACE:  # 发射子弹
                        if len(MainGame.P1_bullet_list) < 1:  # 控制子弹数量
                            m = Bullet(MainGame.Tank_p1)
                            MainGame.P1_bullet_list.append(m)

                if MainGame.Tank_p2 and MainGame.Tank_p2.alive:
                    if event.key == pygame.K_LEFT:  # 左
                        MainGame.Tank_p2.direction = "L"
                        MainGame.Tank_p2.stop = False
                    if event.key == pygame.K_RIGHT:
                        MainGame.Tank_p2.direction = "R"
                        MainGame.Tank_p2.stop = False
                    if event.key == pygame.K_UP:
                        MainGame.Tank_p2.direction = "U"
                        MainGame.Tank_p2.stop = False
                    if event.key == pygame.K_DOWN:
                        MainGame.Tank_p2.direction = "D"
                        MainGame.Tank_p2.stop = False
                    if event.key == pygame.K_KP0:  # 发射子弹
                        if len(MainGame.P2_bullet_list) < 1:  # 控制子弹数量
                            m = Bullet(MainGame.Tank_p2)
                            MainGame.P2_bullet_list.append(m)

    def getOverEvent(self):
        self.eventlist = pygame.event.get()
        for event in self.eventlist:
            if event.type == pygame.QUIT:
                print("退出游戏")
                exit()

    def getSettingEvent(self):
        self.eventlist = pygame.event.get()
        for event in self.eventlist:
            if event.type == pygame.QUIT:
                print("退出游戏")
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x in range(420, 620) and y in range(300, 350):
                    print("开启音乐")
                    Music().playmusic()
                elif x in range(420, 620) and y in range(380, 430):
                    print("关闭音乐")
                    Music().stopmusic()
                elif x in range(420, 515) and y in range(460, 510):
                    print("返回")
                    return 3
        return 0


class CreatItem:
    def creatEnemyTank(self):
        for i in range(8):
            left = random.randint(0, 20)
            MainGame.EnemyTank_list.append(EnemyTank(left * 50, 0, 1))
        for i in range(7):
            left = random.randint(0, 20)
            MainGame.EnemyTank_list.append(EnemyTank(left * 50, 0, 2))
        for i in range(4 + MainGame.Level):
            left = random.randint(0, 20)
            MainGame.EnemyTank_list.append(EnemyTank(left * 50, 0, 3))
        random.shuffle(MainGame.EnemyTank_list)

    def creatMyTank(self, player):
        MainGame.Tank_p1 = MyTank(350, 550, 1)
        MainGame.Tank_p2 = MyTank(550, 550, 2)
        MainGame.Tank_p2.hp = 0
        if player == 2:
            MainGame.Tank_p2.hp = 1

    def creatBrick(self):
        basewall = [Brick(400, 550), Brick(400, 500), Brick(450, 500), Brick(500, 500), Brick(500, 550)]
        MainGame.Brick_list.extend(basewall)
        for i in range(20):
            x = random.randint(0, 20)
            y = random.randint(1, 11)
            if x in range(7, 13) and y in range(9, 13):
                i -= 1
                continue
            brick = Brick(50 * x, 50 * y)
            MainGame.Brick_list.append(brick)

    def creatIron(self):
        for i in range(15):
            x = random.randint(0, 20)
            y = random.randint(1, 11)
            if x in range(7, 13) and y in range(9, 13):
                i -= 1
                continue
            iron = Iron(50 * x, 50 * y)
            MainGame.Iron_list.append(iron)

    def creatGrass(self):
        for i in range(10):
            x = random.randint(0, 20)
            y = random.randint(1, 11)
            if x in range(7, 13) and y in range(9, 13):
                i -= 1
                continue
            grass = Grass(50 * x, 50 * y)
            MainGame.Grass_list.append(grass)

    def creatBase(self):
        MainGame.Base = Base(450, 550)


class Blit:
    def blitBrick(self):
        for brick in MainGame.Brick_list:
            if brick.alive:
                brick.displayBrick()
            else:
                MainGame.Brick_list.remove(brick)

    def blitIron(self):
        for iron in MainGame.Iron_list:
            iron.displayIron()

    def blitGrass(self):
        for grass in MainGame.Grass_list:
            grass.displayGrass()

    def blitBase(self):
        MainGame.Base.displayBase()

    def blitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list[:6]:
            if eTank.hp > 0:
                eTank.displayTank()
                eTank.randMove()
                eTank.hitBrick()
                eTank.hitIron()
                ebullet = eTank.shot()
                if ebullet:
                    MainGame.EnemyTank_bullet_list.append(ebullet)
            else:
                MainGame.EnemyTank_list.remove(eTank)

    def blitEnemyBullet(self):
        for ebullet in MainGame.EnemyTank_bullet_list:
            if ebullet.alive:
                ebullet.display_bullet()
                ebullet.bulletMove()
                ebullet.hitBrick()
                ebullet.hitIron()
                ebullet.hitBase()
                if MainGame.Tank_p1.alive:
                    ebullet.hitMyTank()
            else:
                MainGame.EnemyTank_bullet_list.remove(ebullet)

    def blitMyBullet(self):  # 显示子弹
        for bullet in MainGame.P1_bullet_list:
            if bullet.alive:
                bullet.display_bullet()
                bullet.bulletMove()
                bullet.hitEnemyTank()
                bullet.hitBrick()
                bullet.hitIron()
                bullet.hitBullet()
            else:
                MainGame.P1_bullet_list.remove(bullet)

        for bullet in MainGame.P2_bullet_list:
            if bullet.alive:
                bullet.display_bullet()
                bullet.bulletMove()
                bullet.hitEnemyTank()
                bullet.hitBrick()
                bullet.hitIron()
                bullet.hitBullet()
            else:
                MainGame.P2_bullet_list.remove(bullet)


class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Tank(BaseItem):  # 坦克父类
    def __init__(self):
        self.hp = 1

    def move(self):
        self.oldtop = self.rect.top
        self.oldleft = self.rect.left
        if self.direction == "U":
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == "D":
            if self.rect.top < MainGame.screen_height - self.rect.height:
                self.rect.top += self.speed
        elif self.direction == "L":
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == "R":
            if self.rect.left < MainGame.screen_width - self.rect.width:
                self.rect.left += self.speed

    def stay(self):
        self.rect.left = self.oldleft
        self.rect.top = self.oldtop

    def hitBrick(self):
        for brick in MainGame.Brick_list:
            if pygame.sprite.collide_rect(brick, self):
                self.stay()

    def hitIron(self):
        for iron in MainGame.Iron_list:
            if pygame.sprite.collide_rect(iron, self):
                self.stay()

    def shot(self):
        return Bullet(self)

    def displayTank(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)


class MyTank(Tank):
    def __init__(self, left, top, ty):
        if ty == 1:
            self.images = {"U": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_YU.png"), (50, 50)),
                           "D": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_YD.png"), (50, 50)),
                           "L": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_YL.png"), (50, 50)),
                           "R": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_YR.png"), (50, 50))}
        elif ty == 2:
            self.images = {"U": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_PU.png"), (50, 50)),
                           "D": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_PD.png"), (50, 50)),
                           "L": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_PL.png"), (50, 50)),
                           "R": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_PR.png"), (50, 50))}
        self.direction = "U"
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.hp = 1
        self.speed = 2
        self.stop = True
        self.oldtop = self.rect.top
        self.oldleft = self.rect.left

    def hitEnemyTank(self):
        for etank in MainGame.EnemyTank_list[:6]:
            if pygame.sprite.collide_rect(etank, self):
                self.stay()
                etank.stay()


class EnemyTank(Tank):  # 敌方坦克
    def __init__(self, left, top, ty):
        if ty == 1:
            self.images = {"U": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_BU.png"), (50, 50)),
                           "D": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_BD.png"), (50, 50)),
                           "L": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_BL.png"), (50, 50)),
                           "R": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_BR.png"), (50, 50))}
            self.speed = 2
            self.hp = 2
        elif ty == 2:
            self.images = {"U": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_GU.png"), (50, 50)),
                           "D": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_GD.png"), (50, 50)),
                           "L": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_GL.png"), (50, 50)),
                           "R": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_GR.png"), (50, 50))}
            self.speed = 3
            self.hp = 1
        elif ty == 3:
            self.images = {"U": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_RU.png"), (50, 50)),
                           "D": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_RD.png"), (50, 50)),
                           "L": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_RL.png"), (50, 50)),
                           "R": pygame.transform.smoothscale(pygame.image.load("IMG/Tank_RR.png"), (50, 50))}
            self.speed = 1.5
            self.hp = 3

        self.direction = ["U", "D", "L", "R"][random.randint(0, 3)]
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top

        self.stop = True

    def randMove(self):
        mov = random.randint(0, 30)
        if mov == 0:
            self.direction = ["U", "D", "L", "R"][random.randint(0, 3)]
        self.move()

    def shot(self):
        s = random.randint(1, 100)
        if s < 2:
            return Bullet(self)


class Bullet(BaseItem):  # 子弹
    def __init__(self, tank):
        self.images = {"U": pygame.transform.smoothscale(pygame.image.load("IMG/Bullet_PU.png"), (30, 50)),
                       "D": pygame.transform.smoothscale(pygame.image.load("IMG/Bullet_PD.png"), (30, 50)),
                       "L": pygame.transform.smoothscale(pygame.image.load("IMG/Bullet_PL.png"), (50, 30)),
                       "R": pygame.transform.smoothscale(pygame.image.load("IMG/Bullet_PR.png"), (50, 30))}
        self.direction = tank.direction
        self.image = self.images[self.direction]
        # 子弹速度
        self.speed = 4
        self.maxdistance = 200
        self.alive = True
        self.rect = self.image.get_rect()  # 子弹对象的坐标
        if self.direction == "U":
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == "D":
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + self.rect.height
        elif self.direction == "L":
            self.rect.left = tank.rect.left - self.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.height / 2
        elif self.direction == "R":
            self.rect.left = tank.rect.left + self.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.height / 2

    def bulletMove(self):
        if self.maxdistance <= 0:
            self.alive = False

        elif self.direction == "U":
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.alive = False
        elif self.direction == "D":  # 触碰墙壁
            if self.rect.top < MainGame.screen_height - self.rect.height:  # 屏幕高度 - 子弹的高度
                self.rect.top += self.speed
            else:
                self.alive = False
        elif self.direction == "L":
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.alive = False
        elif self.direction == "R":
            if self.rect.left < MainGame.screen_width - self.rect.width:
                self.rect.left += self.speed
            else:
                self.alive = False
        self.maxdistance -= self.speed

    def hitEnemyTank(self):
        for etank in MainGame.EnemyTank_list[:6]:
            if pygame.sprite.collide_rect(etank, self):  # 相撞测试
                self.alive = False
                etank.hp -= 1

    def hitMyTank(self):
        if pygame.sprite.collide_rect(self, MainGame.Tank_p1):
            MainGame.Tank_p1.hp -= 1
            self.alive = False
        elif pygame.sprite.collide_rect(self, MainGame.Tank_p2):
            MainGame.Tank_p2.hp -= 1
            self.alive = False

    def hitBrick(self):
        for brick in MainGame.Brick_list:
            if pygame.sprite.collide_rect(brick, self):
                self.alive = False
                brick.hp = 0
                brick.live = False

    def hitIron(self):
        for iron in MainGame.Iron_list:
            if pygame.sprite.collide_rect(iron, self):
                self.alive = False

    def hitBullet(self):
        for ebullet in MainGame.EnemyTank_bullet_list:
            if pygame.sprite.collide_rect(ebullet, self):
                ebullet.alive = False
                self.alive = False

    def hitBase(self):
        if pygame.sprite.collide_rect(MainGame.Base, self):
            MainGame.Base.live = False

    def display_bullet(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)


class Brick:
    def __init__(self, left, top):
        self.image = pygame.image.load("img/Brick.png")
        self.rect = self.image.get_rect()

        self.rect.left = left
        self.rect.top = top
        self.alive = True

    def displayBrick(self):
        MainGame.window.blit(self.image, self.rect)


class Iron:
    def __init__(self, left, top):
        self.image = pygame.image.load("img/Iron.png")
        self.rect = self.image.get_rect()

        self.rect.left = left
        self.rect.top = top

    def displayIron(self):
        MainGame.window.blit(self.image, self.rect)


class Grass:
    def __init__(self, left, top):
        self.image = pygame.transform.smoothscale(pygame.image.load("IMG/Grass.png"), (50, 50))
        self.rect = self.image.get_rect()

        self.rect.left = left
        self.rect.top = top

    def displayGrass(self):
        MainGame.window.blit(self.image, self.rect)


class Base:
    def __init__(self, left, top):
        self.image = pygame.transform.smoothscale(pygame.image.load("IMG/Base.png"), (50, 50))
        self.rect = self.image.get_rect()

        self.rect.left = left
        self.rect.top = top
        self.alive = True

    def displayBase(self):
        MainGame.window.blit(self.image, self.rect)


class Music:
    def palyGroundMusic(self):
        pygame.mixer.init()
        pygame.mixer.music.load("IMG/Groundmusic.mp3")
        pygame.mixer.music.play(-1, 0)

    def playEndMusic(self):
        pygame.mixer.init()
        pygame.mixer.music.load("IMG/Endmusic.mp3")
        pygame.mixer.music.play(1, 0)

    def stopmusic(self):
        pygame.mixer.music.set_volume(0)

    def playmusic(self):
        pygame.mixer.music.set_volume(1)


maingame = MainGame()
