import math
from pygame import mixer
import pygame
import random
import button
from constants import *

screen_width = 600
screen_height = 650

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

black = pygame.color.THECOLORS["black"]
white = pygame.color.THECOLORS["white"]
red = pygame.color.THECOLORS["red"]
green = pygame.color.THECOLORS["green"]
blue = pygame.color.THECOLORS["blue"]
yellow = pygame.color.THECOLORS["yellow"]
pink = pygame.color.THECOLORS["pink"]
color = [green, yellow, pink]
color1 = random.randint(0, 255)
color2 = random.randint(0, 255)
color3 = random.randint(0, 255)
colorList = [color1, color2, color3]

explosion_fx = pygame.mixer.Sound("img/explosion.wav")
explosion_fx.set_volume(0.25)
explosion2_fx = pygame.mixer.Sound("img/explosion2.wav")
explosion2_fx.set_volume(0.25)
gamemusic_fx = pygame.mixer.Sound("img/m" + str(random.randint(1, 5)) + ".wav")
gamemusic_fx.set_volume(0.25)
laser_fx = pygame.mixer.Sound("img/laser.wav")
laser_fx.set_volume(0.25)
lose_fx = pygame.mixer.Sound("img/lose.wav")
lose_fx.set_volume(0.25)
win_fx = pygame.mixer.Sound("img/win.wav")
win_fx.set_volume(0.25)
item_fx = pygame.mixer.Sound("img/coin.wav")
item_fx.set_volume(0.25)


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.scale = scale
        self.alive = True
        self.last_shot = pygame.time.get_ticks()
        img = pygame.image.load(f'img/Boss2/Idle/6.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y - 20)
        self.health = 200
        self.remaining = 200
        self.direction_x = 1
        self.direction_y = 1
        self.last_boss_shot = pygame.time.get_ticks()
        self.timer = 200
        self.live = 3
        self.timereset = 200
        self.time = 200

    def update(self, screen, Explosion, explosion_group, bullet_group, spaceship, boom_group, Explosions, explosions_group, \
               meteor_group, meteor_group1, Item1, Item2, Item3, Item4, Item0, Box, item_group):
        self.check_alive()
        if self.alive:
            pygame.draw.rect(screen, red, (self.rect.x, (self.rect.top - 10), self.rect.width, 10))
            if self.remaining > 0:
                pygame.draw.rect(screen, green, (
                    self.rect.x, (self.rect.top - 10), int(self.rect.width * (self.remaining / self.health)), 10))
            if self.remaining <= 0 and self.live == 3:
                explosion_fx.play()
                explosion = Explosion(self.rect.centerx, self.rect.centery, 5)
                explosion_group.add(explosion)
                self.reset()
                self.live -= 1
                self.health = 300
                self.remaining = 300
                img = pygame.image.load(f'img/Boss2/Idle/0.png')
                self.image = pygame.transform.scale(img, (int(img.get_width() * 1.5), int(img.get_height() * 1.5)))
            if self.remaining <= 0 and self.live == 2:
                self.health = 400
                self.remaining = 400
                explosion_fx.play()
                explosion = Explosion(self.rect.centerx, self.rect.centery, 5)
                explosion_group.add(explosion)
                self.reset()
                self.live -= 1
                img = pygame.image.load(f'img/Boss2/Idle/3.png')
                self.image = pygame.transform.scale(img, (int(img.get_width() * 1.5), int(img.get_height() * 1.5)))
            if self.remaining <= 0 and self.live == 1:
                self.live -= 1
                self.kill()
        if pygame.sprite.spritecollide(self, bullet_group, True, pygame.sprite.collide_mask):
            if self.timereset < 0 and self.timer == 0:
                self.remaining -= 10
                if spaceship.crit > 0:
                    if random.randint(spaceship.crit, 100) == 100:
                        self.remaining -= 20
        for boom in boom_group:
            if pygame.sprite.spritecollide(self, boom_group, True):
                explosion_fx.play()
                explosions = Explosions(boom.rect.centerx, boom.rect.centery, 4)
                explosions_group.add(explosions)
                if self.timereset < 0 and self.timer == 0:
                    self.remaining -= 100
                for meteor in meteor_group:
                    if abs(meteor.rect.centerx - boom.rect.centerx) < 350 and abs(
                            meteor.rect.centery - boom.rect.centery) < 350:
                        meteor.health -= 10
                for meteor1 in meteor_group1:
                    if abs(meteor1.rect.centerx - boom.rect.centerx) < 350 and abs(
                            meteor1.rect.centery - boom.rect.centery) < 350:
                        meteor1.health -= 10
            else:
                if boom.time <= 1:
                    if self.timereset < 0 and self.timer == 0:
                        if abs(self.rect.centerx - boom.rect.centerx) < 350 and abs(
                                self.rect.centery - boom.rect.centery) < 350:
                            self.remaining -= 100
        if self.remaining <= 0:
            Bonus = [Item1, Item2, Item3, Item4, Item0, Box]
            bonus = random.choice(Bonus)(self.rect.centerx, self.rect.centery)
            item_group.add(bonus)

    def shoot(self, boss_group, Boss2_Bullets, boss_bullet_group, Boss1_Bullets, Boss_Bullets):
        time_now = pygame.time.get_ticks()
        if self.live == 3:
            if 100 < self.remaining <= 200:
                boss_cooldown = 500
                if time_now - self.last_boss_shot > boss_cooldown:
                    attacking_player = random.choice(boss_group.sprites())
                    boss_bullet1 = Boss2_Bullets(attacking_player.rect.centerx, attacking_player.rect.bottom, 0)
                    boss_bullet_group.add(boss_bullet1)
                    self.last_boss_shot = time_now
            if self.remaining <= 100:
                boss_cooldown = 1000
                if time_now - self.last_boss_shot > boss_cooldown:
                    for i in range(10):
                        attacking_player = random.choice(boss_group.sprites())
                        boss_bullet1 = Boss2_Bullets(attacking_player.rect.centerx, attacking_player.rect.bottom,
                                                     i * 36)
                        boss_bullet_group.add(boss_bullet1)
                    self.last_boss_shot = time_now
        if self.live == 2:
            if 150 < self.remaining <= 300:
                boss_cooldown = 250
                if time_now - self.last_boss_shot > boss_cooldown:
                    attacking_player = random.choice(boss_group.sprites())
                    boss_bullet1 = Boss1_Bullets(attacking_player.rect.centerx, attacking_player.rect.bottom, 0)
                    boss_bullet_group.add(boss_bullet1)
                    self.last_boss_shot = time_now
            if self.remaining <= 150:
                boss_cooldown = 1500
                if time_now - self.last_boss_shot > boss_cooldown:
                    for i in range(10):
                        attacking_player = random.choice(boss_group.sprites())
                        boss_bullet1 = Boss1_Bullets(attacking_player.rect.centerx, attacking_player.rect.bottom,
                                                     i * 36)
                        boss_bullet_group.add(boss_bullet1)
                    self.last_boss_shot = time_now
        if self.live == 1:
            if 200 < self.remaining <= 400:
                boss_cooldown = 200
                if time_now - self.last_boss_shot > boss_cooldown:
                    attacking_player = random.choice(boss_group.sprites())
                    boss_bullet1 = Boss_Bullets(attacking_player.rect.centerx, attacking_player.rect.bottom, 0)
                    boss_bullet_group.add(boss_bullet1)
                    self.last_boss_shot = time_now
            if self.remaining <= 200:
                boss_cooldown = 1000
                if time_now - self.last_boss_shot > boss_cooldown:
                    for i in range(10):
                        attacking_player = random.choice(boss_group.sprites())
                        boss_bullet1 = Boss_Bullets(attacking_player.rect.centerx, attacking_player.rect.bottom, i * 36)
                        boss_bullet_group.add(boss_bullet1)
                    self.last_boss_shot = time_now

    def reset(self):
        self.timereset = 200
        self.rect.x = int(screen_width / 2) - 120
        self.rect.y = screen_height - 700
        self.timer = 80
        self.alive = True

    def move(self, boss1):
        dx = 0
        dy = 0
        if not boss1.alive:
            if self.live == 3 and self.timereset < 0:
                if self.remaining <= 200:
                    dx += self.direction_x * 2
                    if self.rect.left + dx > screen_width:
                        dx = screen_width - self.rect.left
                        self.direction_x *= -1
                    if self.rect.right + dx < 0:
                        dx = - self.rect.right
                        self.direction_x *= -1
                if self.remaining <= 150:
                    dx += self.direction_x * 3
                    if self.rect.left + dx > screen_width:
                        dx = screen_width - self.rect.left
                        self.direction_x *= -1
                    if self.rect.right + dx < 0:
                        dx = - self.rect.right
                        self.direction_x *= -1
                if self.remaining <= 100:
                    dx += self.direction_x * 4
                    if self.rect.left + dx > screen_width:
                        dx = screen_width - self.rect.left
                        self.direction_x *= -1
                    if self.rect.right + dx < 0:
                        dx = - self.rect.right
                        self.direction_x *= -1
            if self.live == 2 and self.timereset < 0:

                dx += self.direction_x * 4
                dy += self.direction_y * 2
                if self.rect.left + dx > screen_width:
                    dx = screen_width - self.rect.left
                    self.direction_x *= -1
                if self.rect.right + dx < 0:
                    dx = - self.rect.right
                    self.direction_x *= -1
                if self.rect.bottom + dy > 500:
                    dy = 500 - self.rect.bottom
                    self.direction_y *= -1
                if self.rect.top + dy < 0:
                    dy = - self.rect.top
                    self.direction_y *= -1
            if self.live == 1 and self.timereset < 0:

                dx += self.direction_x * 6
                dy += self.direction_y * 4

                if self.rect.left + dx > screen_width:
                    dx = screen_width - self.rect.left
                    self.direction_x *= -1
                if self.rect.right + dx < 0:
                    dx = - self.rect.right
                    self.direction_x *= -1
                if self.rect.top + dy > screen_height:
                    dy = screen_height - self.rect.top
                    self.direction_y *= -1
                if self.rect.bottom + dy < 0:
                    dy = - self.rect.bottom
                    self.direction_y *= -1

        self.rect.x += dx
        self.rect.y += dy

    def auto_walk(self, boss1):
        if not boss1.alive:
            dy = 0
            self.timer -= 1
            self.timereset -= 1
            dy += 1.5
            if self.timer <= 0:
                self.timer = 0
                self.rect.y -= 0.5
            self.rect.y += dy

    def check_alive(self):
        if self.live == 0:
            self.alive = False


class Boss1(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.scale = scale
        self.alive = True
        self.last_shot = pygame.time.get_ticks()
        self.health = 200
        self.remaining = 200
        self.direction_x = 1
        self.direction_y = 1
        self.last_boss_shot = pygame.time.get_ticks()
        self.timer = 150
        self.live = 1
        self.timereset = 150
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load all images for the players
        animation_types = ['Idle', 'Death']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'img/Boss1/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/Boss1/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.center = (x, y - 20)

    def update(self, Item1, Item2, Item3, Item4, Item0 ,Explosion, explosion_group, screen, bullet_group, spaceship, boom_group, \
               Explosions, explosions_group, meteor_group, meteor_group1, item_group1, Box):
        self.check_alive(Explosion, explosion_group)
        self.update_animation()
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.top - 10), self.rect.width, 10))
        if self.remaining > 0:
            pygame.draw.rect(screen, green, (
                self.rect.x, (self.rect.top - 10), int(self.rect.width * (self.remaining / self.health)), 10))
        if pygame.sprite.spritecollide(self, bullet_group, True, pygame.sprite.collide_mask):
            if self.timereset < 0 and self.timer == 0:
                self.remaining -= 10
                if spaceship.crit > 0:
                    if random.randint(spaceship.crit, 100) == 100:
                        self.remaining -= 20
        for boom in boom_group:
            if pygame.sprite.spritecollide(self, boom_group, True):
                explosion_fx.play()
                explosions = Explosions(boom.rect.centerx, boom.rect.centery, 4)
                explosions_group.add(explosions)
                if self.timereset < 0 and self.timer == 0:
                    self.remaining -= 100
                for meteor in meteor_group:
                    if abs(meteor.rect.centerx - boom.rect.centerx) < 350 and abs(
                            meteor.rect.centery - boom.rect.centery) < 350:
                        meteor.health -= 10
                for meteor1 in meteor_group1:
                    if abs(meteor1.rect.centerx - boom.rect.centerx) < 350 and abs(
                            meteor1.rect.centery - boom.rect.centery) < 350:
                        meteor1.health -= 10
            else:
                if boom.time <= 1:
                    if self.timereset < 0 and self.timer == 0:
                        if abs(self.rect.centerx - boom.rect.centerx) < 350 and abs(
                                self.rect.centery - boom.rect.centery) < 350:
                            self.remaining -= 100
        if not self.alive:
            Bonus = [Item1, Item2, Item3, Item4, Item0, Box]
            bonus = random.choice(Bonus)(self.rect.centerx, self.rect.centery)
            item_group1.add(bonus)

    def shoot(self, boss1_group, Boss4_Bullets, boss1_bullet_group):
        time_now = pygame.time.get_ticks()
        if 150 < self.remaining <= 200:
            boss_cooldown = 500
            if time_now - self.last_boss_shot > boss_cooldown:
                attacking_player = random.choice(boss1_group.sprites())
                boss_bullet2 = Boss4_Bullets(attacking_player.rect.centerx, attacking_player.rect.bottom, 0)
                boss1_bullet_group.add(boss_bullet2)
                self.last_boss_shot = time_now
        if 100 < self.remaining <= 150:
            boss_cooldown1 = 1000
            if time_now - self.last_boss_shot > boss_cooldown1:
                for i in range(10):
                    attacking_player = random.choice(boss1_group.sprites())
                    boss_bullet2 = Boss4_Bullets(attacking_player.rect.centerx, attacking_player.rect.bottom, i * 36)
                    boss1_bullet_group.add(boss_bullet2)
                self.last_boss_shot = time_now
        if self.remaining <= 100:
            boss_cooldown1 = 1500
            if time_now - self.last_boss_shot > boss_cooldown1:
                for i in range(15):
                    attacking_player = random.choice(boss1_group.sprites())
                    boss_bullet2 = Boss4_Bullets(attacking_player.rect.centerx, attacking_player.rect.bottom, i * 24)
                    boss1_bullet_group.add(boss_bullet2)
                self.last_boss_shot = time_now

    def move(self):
        dx = 0
        dy = 0
        if 170 < self.remaining <= 200:
            if self.timereset < 0:
                dx += self.direction_x * 2
                if self.rect.left + dx > screen_width:
                    dx = screen_width - self.rect.left
                    self.direction_x *= -1
                if self.rect.right + dx < 0:
                    dx = - self.rect.right
                    self.direction_x *= -1
        if 140 < self.remaining <= 170:
            if self.timereset < 0:
                dx += self.direction_x * 4
                if self.rect.left + dx > screen_width:
                    dx = screen_width - self.rect.left
                    self.direction_x *= -1
                if self.rect.right + dx < 0:
                    dx = - self.rect.right
                    self.direction_x *= -1
        if self.remaining <= 140:
            if self.timereset < 0:
                dx += self.direction_x * 6
                if self.rect.left + dx > screen_width:
                    dx = screen_width - self.rect.left
                    self.direction_x *= -1
                if self.rect.right + dx < 0:
                    dx = - self.rect.right
                    self.direction_x *= -1

        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 1:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def auto_walk(self, enemy1):
        dy = 0
        if not enemy1.alive:
            self.timer -= 1
            self.timereset -= 1
            dy += 1.5
            if self.timer <= 0:
                self.timer = 0
                self.rect.y -= 0.5
        self.rect.y += dy

    def check_alive(self, Explosion, explosion_group):
        if self.remaining <= 0:
            self.remaining = 0
            self.alive = False
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 4)
            explosion_group.add(explosion)
