"""
Author : Shivang
Purpose: Space Clash pygame
"""


import pygame
import random
import time

FPS = 60
fps = pygame.time.Clock()
pygame.init()
# pygame.mixer.init()
screen = pygame.display.set_mode((480, 600))
pygame.display.set_caption("SpaceClash")
im = pygame.image.load("shum_assests/rocket.png")
pygame.display.set_icon(im)
bg_music = pygame.mixer.music.load('shum_assests/cool.mp3')

print("\nJust Shoot and Gain!\nDeveloper-sivangbagri@gamil.com\n ")


def draw_shield(surface, x, y, pct):
    if pct < 0: pct = 0
    bar_length = 100
    bar_height = 10
    fill = pct
    out_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(screen, (0, 255, 0), fill_rect)
    pygame.draw.rect(screen, (0, 0, 0), out_rect, 2)


def boss_health(surface, x, y, pcent):
    b_length = 100
    b_height = 10
    fill = pcent
    outer = pygame.Rect(x, y, b_length, b_height)
    inner = pygame.Rect(x, y, fill, b_height)
    pygame.draw.rect(screen, (255, 0, 0), inner)
    pygame.draw.rect(screen, (0, 0, 0), outer, 2)


def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        screen.blit(img, img_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(playerim, (40, 40)).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = 12
        # pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)
        self.rect.center = (240, 568)
        self.speedx = 0
        self.shield = 100
        self.hidden = False
        self.lives = 3
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        # boss fight
        if scorev > 500:
            self.shield_change = .1
            self.shield -= self.shield_change
        # timeout for powerup
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > 5000:
            self.power = 1
            self.power_time = pygame.time.get_ticks()

        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.center = (240, 568)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.speedx = +4
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.speedx = -4
            if event.key == pygame.K_SPACE:
                self.shoot()
            if event.key == pygame.K_TAB:
                player.shield += 5
                if player.shield > 100: player.shield = 100
        if event.type == pygame.KEYUP:
            self.speedx = 0
        self.rect.x += self.speedx
        if self.rect.right > 480:
            self.rect.right = 480
        elif self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > 250:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            elif self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet2)

    def hide(self):
        # hides temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (1000, 1000)


boss_im = pygame.image.load("shum_assests/boss1.png")


class Bose(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_im
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(1, 470)
        self.rect.y = random.randint(0, 50)
        self.speedx = 3
        self.health = 100

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > 480:
            self.speedx = -5
        elif self.rect.left < 0:
            self.speedx = +5


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(mob_images)
        self.rect = self.image.get_rect()
        # pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)
        self.radius = 11
        self.rect.x = random.randint(0, 470)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(1, 5)

    def update(self):
        # self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > 600:
            self.rect.x = random.randint(0, 470)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(1, 5)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bulletim
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -20

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_im[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > 600:
            self.kill()


font2 = pygame.font.Font('shum_assests/BRLNSR.ttf', 64)

# def game_txt():
#     gameover = font2.render("SHUMP", True, (255, 255, 255))
#     by = font3.render('Arrow to move,Space to fire', True, (255, 255, 255))
#     screen.blit(gameover, (240, 150))
#     screen.blit(by, (240, 600))


# def show_go():
#     game_txt()
#     # pygame.draw.text(screen, "SHMUP!", 64, 240, 600 / 4)
#     # pygame.draw.text(screen, 'Arrow to move,Space to fire', 22, 240, 600)
#     # pygame.draw.text(screen, "Press akey to begin", 18, 240, 600 * 3 / 4)
#     pygame.display.update()
#     waiting = True
#     while waiting:
#         fps.tick(FPS)
#         for e in pygame.event.get():
#             if e.type == pygame.QUIT:
#                 pygame.quit()
#             if e.type == pygame.KEYUP:
#                 waiting = False


# class Explosion(pygame.sprite.Sprite):
#     def __init__(self, center, size):
#         pygame.sprite.Sprite.__init__(self)
#         self.size = size
#         self.image = explo_im[self.size][0]
#         self.rect = self.image.get_rect()
#         self.rect.center = center
#         self.frame = 0
#         self.last_update = pygame.time.get_ticks()
#         self.frame_rate = 50
#
#     def update(self):
#         now = pygame.time.get_ticks()
#         if now - self.last_update > self.frame_rate:
#             self.frame_rate = now
#             self.frame += 1
#             if self.frame == len(explo_im[self.size]):
#                 self.kill()
#             else:
#                 center = self.rect.center
#                 self.image = explo_im[self.size][self.frame]
#                 self.rect = self.image.get_rect()
#                 self.rect.center = center

# explo = pygame.image.load("shum_assests/regularExplosion01.png")

font = pygame.font.Font('shum_assests/BRLNSR.ttf', 25)

background = pygame.image.load("shum_assests/bg.jpg").convert()
background_rect = background.get_rect()
playerim = pygame.image.load("shum_assests/playership.png")
mini_im = pygame.transform.scale(playerim, (25, 19))
bulletim = pygame.image.load("shum_assests/laser.png")
bulletim2 = pygame.image.load("shum_assests/laser2.png")
mob_images = []
mob_list = ['shum_assests/m (2).png', 'shum_assests/m (4).png', 'shum_assests/m (5).png', 'shum_assests/m (7).png',
            'shum_assests/m (14).png', 'shum_assests/m (15).png', 'shum_assests/m (17).png',
            'shum_assests/meteor.png']
powerup_im = {}
powerup_im['shield'] = pygame.image.load("shum_assests/pill_yellow.png")
powerup_im['gun'] = pygame.image.load("shum_assests/bolt_gold.png")

for i in mob_list:
    mob_images.append(pygame.image.load(i))


# explo_im = {'lg': [], 'sm': []}
# for i in range(0, 9):
#     filename = 'regularExplosion0{}.png'.format(1)
#     img = pygame.image.load(filename).convert()
#     img_lg = pygame.transform.scale(img, (75, 75))
#     explo_im['lg'].append(img_lg)
#     img_sm = pygame.transform.scale(img, (32, 32))
#     explo_im['sm'].append(img_sm)
#
# all_sprites = pygame.sprite.Group()
# player = Player()
# power_ups = pygame.sprite.Group()
# all_sprites.add(player)
# mobs = pygame.sprite.Group()
# bullets = pygame.sprite.Group()
# for i in range(45):
#     m = Mob()
#     all_sprites.add(m)
#     mobs.add(m)

def score_val(x, y):
    score = font.render(str(scorev), True, (255, 255, 255))
    screen.blit(score, (x, y))


def score_after(x, y):
    score = font.render(str(scorev), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over(x, y):
    end = font2.render("GAME OVER!", True, (200, 0, 0))
    screen.blit(end, (x, y))


def copyright(x, y):
    end2 = font.render("Created by Shivang", True, (200, 200, 200))
    screen.blit(end2, (x, y))


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
boss = Bose()
Boss_group = pygame.sprite.Group()

for i in range(45):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
scorev = 0
pygame.mixer.music.play(-1)
run = True
while run:

    screen.fill((0, 0, 0))
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    all_sprites.update()
    # bullet hit mob
    hitss = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hitss:
        if random.random() > 0.9:  # generates random no. blw 0,1
            pow = Pow(hit.rect.center)
            power_ups.add(pow)
            all_sprites.add(pow)

        sound = pygame.mixer.Sound("shum_assests/EXPLOSION BANG 04.ogg")
        sound.play()
        scorev += 1
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        # boss entry
    slow = False
    if scorev > 500:
        score_after(1000, 1000)
        sound.stop()
        boss_health(screen, 5, 20, boss.health)
        all_sprites.remove(mobs)
        Boss_group.add(boss)
        all_sprites.add(boss)
    if boss.health <= 0 or player.shield <= 0:
        game_over(50, 300)
        copyright(50, 380)
    hitS = pygame.sprite.groupcollide(bullets, Boss_group, True, False)
    for h in hitS:
        boss.health -= 3
        if boss.health <= 0:
            boss.health = 0
            # run=False
    # mob hit player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)  # (   ,   ,delete,)
    blow_sound = pygame.mixer.Sound("shum_assests/rifle.wav")
    if hits:
        player.shield -= 5
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        if player.shield <= 0:
            blow_sound.play()
            player.hide()
            player.lives -= 1
            player.shield = 100
        if player.lives == 0:
            game_over(50, 300)
            copyright(50, 380)
            time.sleep(1)
            run = False

    col = pygame.sprite.spritecollide(player, power_ups, True)
    for hit in col:
        if hit.type == 'shield':
            player.shield += 5
            if player.shield >= 100: player.shield = 100
        elif hit.type == 'gun':
            player.powerup()

    draw_shield(screen, 5, 5, player.shield)
    draw_lives(screen, 470 - 80, 5, player.lives, mini_im)
    if scorev < 500:
        score_val(230, 4)

    pygame.display.update()
    fps.tick(FPS)
