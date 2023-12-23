import os
import random

import pygame
from pygame import mixer

mixer.init()
pygame.init()

clock = pygame.time.Clock()
FPS = 60
WIDTH = 1540
HEIGHT = 880

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME")

pygame.mixer.music.load('audio/John Wick (OST) - Shots Fired.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0, 5000)

shoot1_fx = pygame.mixer.Sound('audio/enemyshoot.wav')
shoot1_fx.set_volume(0.5)
shoot2_fx = pygame.mixer.Sound('audio/playershoot.mp3')
shoot2_fx.set_volume(0.2)

moving_left = False
moving_right = False
moving_up = False
moving_down = False
jump = False
shoot = False
slash = False
start_pos_y = 750
screen_scroll_x = 0
screen_scroll_y = 0
bulletimg = pygame.image.load('img/icons/bullet.png').convert_alpha()
health_box_image = pygame.transform.scale(pygame.image.load('img/icons/health_box.png').convert_alpha(), (40, 30))
ammo_box_image = pygame.transform.scale(pygame.image.load('img/icons/ammo_box.png').convert_alpha(), (50, 30))
item_boxes = {'Health': health_box_image,
              'Ammo': ammo_box_image}

Credit = False
Return_from_credit = False
start_game = False
run = True
bgr_x = 0
bgr_y = -500
death_timer = 50
wind_slash = pygame.transform.scale_by(pygame.image.load("img/Wind_Slash.png").convert_alpha(), 0.3)
img = pygame.transform.scale_by(pygame.image.load("img/Picture2.png"), 0.6)
bgr_width = img.get_width()
bgr = pygame.transform.scale_by(pygame.image.load("img/Picture2.png").convert(), 0.6)

platformimg = pygame.transform.scale_by(pygame.image.load("img/container.png"), 1)
crate1_1 = pygame.transform.scale(pygame.image.load("img/Crate1_1.png"), (120, 126))
crate1_2 = pygame.transform.scale(pygame.image.load("img/Crate1_2.png"), (120, 126))
crate1_3 = pygame.transform.scale(pygame.image.load("img/Crate1_3.png"), (120, 126))
crane = pygame.image.load("img/Sprite-0001.png")
spark = pygame.transform.scale_by(pygame.image.load("img/pngwing.com.png"), 0.05)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        if type == 'Container':
            self.image = platformimg
        if type == 'Crate1_1':
            self.image = crate1_1
        if type == 'Crate1_2':
            self.image = crate1_2
        if type == 'Crate1_3':
            self.image = crate1_3
        if type == "Crane":
            self.image = crane
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

    def update(self):
        self.rect.x += screen_scroll_x
        self.rect.y += screen_scroll_y
        screen.blit(self.image, self.rect)


platform_group = pygame.sprite.Group()
platform1 = Platform(1000, start_pos_y, 'Container')
platform_group.add(platform1)
platform_group.add(Platform(1000 + platform1.rect.width, start_pos_y, 'Container'))
platform_group.add(Platform(1000 + platform1.rect.width, start_pos_y - platform1.rect.height, 'Crate1_1'))
platform_group.add(Platform(1120 + platform1.rect.width, start_pos_y - platform1.rect.height, 'Crate1_3'))
platform_group.add(Platform(1120 + platform1.rect.width, start_pos_y - platform1.rect.height - 120, 'Crate1_2'))
platform_group.add(Platform(4000, start_pos_y, 'Container'))
platform_group.add(Platform(4485, start_pos_y, 'Container'))
platform_group.add(Platform(4485, start_pos_y - 124, 'Container'))
platform_group.add(Platform(4485 + 485 + 485, start_pos_y - 124, 'Container'))
platform_group.add(Platform(4485 + 485 + 485 + 485, start_pos_y - 124, 'Container'))
platform_group.add(Platform(4485 + 485 + 485, start_pos_y - 248, 'Container'))
platform_group.add(Platform(4485 + 485 + 485 + 485 + 485 + 300, start_pos_y, 'Container'))
platform_group.add(Platform(4485 + 485 + 485 + 485 + 485 + 300, start_pos_y - 124, 'Container'))
platform_group.add(Platform(4485 + 485 + 485 + 485 + 485 + 300, start_pos_y - 124 * 2, 'Container'))
platform_group.add(Platform(4485 + 485 + 485 + 485 + 485 + 300, start_pos_y - 124 * 3, 'Container'))
platform_group.add(Platform(4485 + 485 + 485 + 485 + 485 + 300, start_pos_y - 124 * 4, 'Container'))
platform_group.add(Platform(4485 + 485 + 485 + 485 + 485 + 300, start_pos_y - 124 * 5, 'Container'))
platform_group.add(Platform(4485 + 300, start_pos_y - 248, 'Crate1_2'))
platform_group.add(Platform(4485 + 485 + 485 + 485 + 485 + 300 - 120, start_pos_y, 'Crate1_3'))
platform_group.add(Platform(4485 + 485 + 485 + 205, start_pos_y - 1000, 'Crane'))
platform_group.add(Platform(4485 + 485 + 485 + 485 + 205, start_pos_y - 1000, 'Crane'))
platform_group.add(Platform(4485 + 485 + 485 + 485 + 205 + 485, start_pos_y - 1000, 'Crane'))
platform_group.add(Platform(4485 + 485 + 485 + 485 + 205 + 485 + 485, start_pos_y - 1000, 'Crane'))


class Player(pygame.sprite.Sprite):
    def __init__(self, char, x, y, scale, speed, ammo, shooting_speed):
        pygame.sprite.Sprite.__init__(self)
        self.shooting_speed = shooting_speed
        self.alive = True
        self.ammo = ammo
        self.max_ammo = 45
        self.stored_ammo = 45
        self.jump = False
        self.jumping = False
        self.shooting_cooldown = 3
        self.slashing_cooldown = 3
        self.y_vel = 0
        self.health = 100
        self.max_health = 100
        self.char = char
        self.animation_list = []
        self.action = 0
        self.index = 0
        self.dx = 0
        self.dy = 0
        self.update_time = pygame.time.get_ticks()
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.vision = pygame.Rect(0, 0, 250, 20)

        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            num_frames = len(os.listdir(f"img/{self.char}/{animation}"))
            temp_list = []
            for i in range(num_frames):
                img = pygame.image.load(f"img/{self.char}/{animation}/{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width()) * scale, int(img.get_height()) * scale))
                temp_list.append(img)
                self.width = img.get_width()
                self.height = img.get_height()
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        self.speed = speed
        self.dir = 1
        self.flip = False

    def move(self, moving_left, moving_right):
        screen_scroll_x = 0
        global screen_scroll_y
        self.dx = 0
        self.dy = 0
        self.check_foot = pygame.Rect(0, 0, 15, 55)
        self.check_foot.midtop = (self.rect.centerx, self.rect.centery)
        if moving_left:
            self.dx = -self.speed
            self.flip = True
            self.dir = -1
        if moving_right:
            self.dx = self.speed
            self.flip = False
            self.dir = 1

        if jump and not player.jumping:
            player.jumping = True
            player.y_vel = -15

        if moving_left == 0 or moving_right == 0 or jump == 0:
            self.dy += self.y_vel

        if not rope_collide:
            self.y_vel += 0.675
        if moving_up and rope_collide:
            player.dy -= self.speed
        if moving_down and rope_collide:
            player.dy += self.speed

        for enemy in enemy_group:
            if enemy.rect.bottom + enemy.dy > 750:
                enemy.dy = 0
                enemy.jumping = False

        if ground.rect.colliderect(player.rect) and ground.rect.y >= player.rect.y:
            if player.y_vel > 0:
                player.y_vel = 0
                player.rect.y = ground.rect.bottom - player.rect.height
                player.jumping = False
        if ground1.rect.colliderect(
                self.rect) and ground1.rect.y < self.rect.y + 70 and ground1.rect.bottom > self.rect.top + 15:
            if self.dx > 0:
                self.rect.x = ground1.rect.left - self.rect.width - 3

        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.char == 'player':
            if self.rect.right > WIDTH - 600 or self.rect.left < 250:
                self.rect.x -= self.dx
                screen_scroll_x = -self.dx
            if self.rect.top < 200 and moving_up:
                self.rect.y -= self.dy
                screen_scroll_y = 5
            elif self.rect.bottom > start_pos_y and not player.check_foot.colliderect(ground.rect):
                self.rect.y -= self.dy
                screen_scroll_y = -9
            else:
                screen_scroll_y = 0
        return screen_scroll_x

    def collide_block(self):
        for platform in platform_group:
            if platform.rect.colliderect(
                    self.rect) and platform.rect.y < self.rect.y + 70 and platform.rect.bottom > self.rect.top + 15:
                if self.dx > 0:
                    self.rect.x = platform.rect.left - self.rect.width
                if self.dx < 0:
                    self.rect.x = platform.rect.right
            if platform.rect.colliderect(self.rect):
                if self.y_vel >= 0 and platform.rect.y >= self.rect.y:
                    self.y_vel = 0
                    self.rect.y = platform.rect.top - self.rect.height
                    self.jumping = False
                elif self.dy < 0 and self.rect.top + 50 >= platform.rect.bottom:
                    self.dy = 0
                    self.y_vel = 0
                    self.rect.y = platform.rect.bottom

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def update_animation(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
            if self.index >= len(self.animation_list[self.action]):
                if self.action == 3:
                    self.kill()
                else:
                    self.index = 0

    def shoot(self, char_type):
        if self.shooting_cooldown == 0 and self.ammo > 0:
            self.shooting_cooldown = self.shooting_speed
            bullet = Bullet(self.rect.right, self.rect.centery, self.dir)
            spark = Spark((self.rect.centerx + 35 * self.dir), self.rect.centery,
                          self.dir)
            spark_group.add(spark)
            if char_type == player:
                bullet_group_player.add(bullet)
                shoot2_fx.play()
            if char_type == enemy:
                bullet_group_enemy.add(bullet)
                shoot1_fx.play()
            self.ammo -= 1

    def slash(self):
        if self.slashing_cooldown == 0:
            self.slashing_cooldown = 20
            slash = Slash(self.rect.centerx + ((0.2 * self.rect.size[0] + 20) * self.dir),
                          self.rect.centery,
                          self.dir)

            slash_group.add(slash)

    def AI(self):
        if self.alive and player.alive:
            if not self.idling and random.randint(1, 150) == 1:
                self.idling = True
                self.update_action(0)
                self.idling_counter = 50

            if self.vision.colliderect(player.rect):
                self.update_action(0)
                self.shoot(enemy)

            else:
                if not self.idling:
                    if self.dir == 1:
                        AI_moving_right = True
                    else:
                        AI_moving_right = False
                    AI_moving_left = not AI_moving_right
                    self.move(AI_moving_left, AI_moving_right)
                    self.move_counter += 1
                    self.update_action(1)
                    self.vision.center = (self.rect.centerx + 75 * self.dir, self.rect.centery)

                    if self.move_counter > 50:
                        self.dir *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter == 0:
                        self.idling = False
        self.rect.x += screen_scroll_x
        self.rect.y += screen_scroll_y

    def update(self):
        self.collide_block()
        self.update_animation()
        self.check_alive()
        if self.shooting_cooldown > 0:
            self.shooting_cooldown -= 1
        if self.slashing_cooldown > 0:
            self.slashing_cooldown -= 1
        for bullet in bullet_group_enemy:
            if bullet.rect.colliderect(player.rect):
                if player.alive:
                    player.health -= 5
                    bullet.kill()
        for bullet in bullet_group_player:
            for enemy in enemy_group:
                if bullet.rect.colliderect(enemy.rect):
                    if enemy.alive:
                        enemy.health -= 50
                        bullet.kill()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.index = 0
            self.update_time = pygame.time.get_ticks()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dir):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 85
        self.image = bulletimg
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dir = dir

    def update(self):
        self.rect.x += (self.dir * self.speed)
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

        for platform in platform_group:
            if pygame.sprite.spritecollide(platform, bullet_group_enemy, False):
                self.kill()
            if pygame.sprite.spritecollide(platform, bullet_group_player, False):
                self.kill()


class Spark(pygame.sprite.Sprite):
    def __init__(self, x, y, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = spark
        self.rect = self.image.get_rect()
        if player.jumping:
            self.rect.center = (x, y - 5)
        else:
            self.rect.center = (x, y)
        self.dir = dir
        self.flip = False
        self.display_time = 1

    def update(self):
        if player.dir == -1:
            self.flip = True
        else:
            self.flip = False
        if self.display_time > 0:
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
            self.display_time -= 1
        if self.display_time == 0:
            self.kill()


class Slash(pygame.sprite.Sprite):
    def __init__(self, x, y, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = wind_slash
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dir = dir
        self.flip = False
        self.display_time = 5

    def update(self):
        if player.dir == -1:
            self.flip = True
        else:
            self.flip = False
        if self.display_time > 0:
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
            self.display_time -= 1
        if self.display_time == 0:
            self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, slash_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

    def update(self):
        self.rect.x += screen_scroll_x
        self.rect.y += screen_scroll_y
        if player.rect.colliderect(self.rect):
            self.kill()
            if self.item_type == "Health":
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            if self.item_type == "Ammo":
                player.stored_ammo += 35
                if player.stored_ammo > player.max_ammo:
                    player.stored_ammo = player.max_ammo


Container1 = pygame.image.load("img/container.png")
Container1_1 = pygame.image.load("img/container.png")
Container1_1.set_alpha(80)
Container2 = pygame.transform.scale_by(Container1, 2)
Container2_1 = pygame.transform.scale_by(Container1, 2)
Container2_1.set_alpha(80)
Crane2 = pygame.image.load("img/Sprite-0002.png")
Crane3 = pygame.image.load("img/Sprite-0003.png")
Crane4 = pygame.image.load("img/Sprite-0003.png")
Crane4.set_alpha(80)

Crate_types = {"1": [Container1, Container1_1],
               "2": [Container2, Container2_1],
               "3": [Crane2, Crane2],
               "4": [Crane3, Crane4]}


class Crates(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = Crate_types[type][0]
        self.image1 = Crate_types[type][1]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        self.rect1 = self.image1.get_rect()
        self.rect1.bottomleft = (x, y)

    def update(self):
        self.rect.x += screen_scroll_x
        self.rect.y += screen_scroll_y
        if not pygame.sprite.spritecollide(player, crate_group, False):
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.image1, self.rect)


def draw_text(text, text_color, x, y, size):
    font = pygame.font.SysFont('DePixel', size)
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


class Button:
    def __init__(self, text, x, y, func, enabled):
        self.font = pygame.font.SysFont('DePixel', 30)
        self.x = x
        self.y = y
        self.func = func
        self.button_text = self.font.render(text, True, 'white')
        self.text_width = self.button_text.get_width()
        self.text_height = self.button_text.get_height()
        self.button_rect = pygame.rect.Rect((x, y), (200, 50))
        self.draw()
        self.enabled = enabled
        self.update()

    def draw(self):
        screen.blit(self.button_text, (self.x + (200 - self.text_width) // 2, self.y + 10))
        pygame.draw.rect(screen, 'white', self.button_rect, 3, 5)

    def update(self):
        global start_game, run, Credit, Return_from_credit
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        if self.button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, 'dark gray', self.button_rect, 0, 5)
            screen.blit(self.button_text, (self.x + (200 - self.text_width) // 2, self.y + 10))
            if self.enabled:
                if left_click:
                    if self.func == 'Start':
                        start_game = True
                    elif self.func == 'Exit':
                        run = False
                    elif self.func == 'Credit':
                        Credit = True
                    elif self.func == 'Return':
                        Return_from_credit = True


def main_menu():
    screen.blit(start_menu_img, (0, 0))
    Button('START', WIDTH // 2 + 300, HEIGHT // 2 - 50, 'Start', button1_enabled)
    Button('EXIT', WIDTH // 2 + 300, HEIGHT // 2 + 50, 'Exit', button2_enabled)
    Button('CREDIT', WIDTH // 2 + 300, HEIGHT // 2 + 150, 'Credit', button3_enabled)


def credit():
    screen.fill((0, 0, 25))
    draw_text("NGHIEM NHAT MINH", 'white', WIDTH // 2 - 500, HEIGHT // 2 - 200, 50)
    draw_text("PHAM TRUNG DUC", 'white', WIDTH // 2 - 500, HEIGHT // 2, 50)
    draw_text("HUYNH TUAN KHANH", 'white', WIDTH // 2 - 500, HEIGHT // 2 + 200, 50)
    Button('RETURN', WIDTH // 2 + 300, HEIGHT // 2 - 100, 'Return', True)
    Button('EXIT', WIDTH // 2 + 300, HEIGHT // 2, 'Exit', True)


slash_group = pygame.sprite.Group()
bullet_group_player = pygame.sprite.Group()
bullet_group_enemy = pygame.sprite.Group()
spark_group = pygame.sprite.Group()
crate_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

item_box1 = ItemBox('Health', 3500, start_pos_y)
item_box2 = ItemBox('Ammo', 3400, start_pos_y)
item_box_group.add(item_box1, item_box2)

crate_group.add(Crates(2800, start_pos_y, "2"))
crate_group.add(Crates(4485 + 485, start_pos_y, "1"))
crate_group.add(Crates(4485 + 485, start_pos_y - 124, "1"))
crate_group.add(Crates(4485 + 485, start_pos_y - 248, "1"))
crate_group.add(Crates(4485 + 485 + 485, start_pos_y, "1"))
crate_group.add(Crates(4485 + 485 + 485 + 485, start_pos_y, "1"))
crate_group.add(Crates(4485 + 485 + 485, start_pos_y - 124 * 3, "1"))
crate_group.add(Crates(4485 + 485 + 485 + 485, start_pos_y - 124 * 2, "1"))
crate_group.add(Crates(4485 + 485 + 485 + 485, start_pos_y - 124 * 3, "1"))
crate_group.add(Crates(4485 + 485 + 485 + 105, start_pos_y - 1000, "3"))
crate_group.add(Crates(4485 + 485 + 485 + 105 + 485 + 485, start_pos_y - 1000 - 100, "4"))

player = Player("player", WIDTH / 2 - 200, start_pos_y, 2.2, 5, 15, 15)
player_group.add(player)
enemy_group.add(Player("enemy", 3200, start_pos_y, 2.2, 2, 150, 25))
enemy_group.add(Player("enemy", 3400, start_pos_y, 2.2, 2, 150, 25))
enemy_group.add(Player("enemy", 1800, start_pos_y - 200, 2.2, 2, 150, 25))
enemy_group.add(Player("enemy", 1300, start_pos_y - 140, 2.2, 2, 150, 25))
enemy_group.add(Player("enemy", 4485 + 485 + 485, start_pos_y, 2.2, 2, 150, 25))
enemy_group.add(Player("enemy", 4485 + 485 + 485 + 355, start_pos_y, 2.2, 2, 150, 25))
enemy_group.add(Player("enemy", 4485 + 485 + 485 + 455, start_pos_y, 2.2, 2, 150, 25))
enemy_group.add(Player("enemy", 4485 + 485 + 485 + 400, start_pos_y, 2.2, 2, 150, 25))
enemy_group.add(Player("enemy", 4485 + 485 + 485, start_pos_y, 2.2, 2, 150, 25))
enemy_group.add(Player("enemy", 4485 + 485 + 485 + 485 + 10, start_pos_y - 124 * 2, 2.2, 2, 150, 25))
enemy_group.add(
    Player("enemy", 4485 + 485 + 485 + 105 + 485 + 485 + 50, start_pos_y - 1000 - 100 - 50 - 50, 2.2, 2, 150, 25))
enemy_group.add(
    Player("enemy", 4485 + 485 + 485 + 105 + 485 + 400, start_pos_y - 1000 - 100 - 50 - 50, 2.2, 2, 150, 25))
enemy_group.add(Player("enemy", 4485 + 485 + 485 + 105 + 485, start_pos_y - 1000 - 100 - 50 - 50, 2.2, 2, 150, 25))

dead = 0

start_menu_img = pygame.transform.scale(pygame.image.load("img/background.png"), (WIDTH, HEIGHT))
button1_enabled = True
button2_enabled = True
button3_enabled = True

font = pygame.font.SysFont('DePixel', 30)
message = '...'
snip = font.render('', True, 'White')
counter = 0
speed = 3
done = False


def Dialog(message):
    global counter, snip, speed, done, font
    pygame.draw.rect(screen, 'white', pygame.rect.Rect((15, 650), (1515, 150)), 0, 5)
    if counter < len(message) * speed:
        counter += 1
    elif counter >= len(message) * speed:
        done = True
    snip = font.render(message[0:counter // speed], True, 'black')
    screen.blit(snip, (60, 670))


note_img = pygame.image.load("img/note.png")
note1_img = pygame.image.load("img/note1.png")


class Document(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(note_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.image1 = pygame.transform.scale(note1_img, (50, 50))

    def update(self):
        global document
        self.rect.x += screen_scroll_x
        self.rect.y += screen_scroll_y
        if not pygame.sprite.spritecollide(player, note_group, False):
            screen.blit(self.image, self.rect)
            document = False
        else:
            screen.blit(self.image1, self.rect)
            document = True


Trigger = False
Empty = pygame.image.load("img/Empty.png")


class Triggers(pygame.sprite.Sprite):
    def __init__(self, x, y, enabled):
        pygame.sprite.Sprite.__init__(self)
        self.enabled = enabled
        self.image = pygame.transform.scale(Empty, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

    def update(self):
        global Trigger
        self.rect.x += screen_scroll_x
        self.rect.y += screen_scroll_y
        for trigger in trigger_group:
            if trigger.enabled:
                if player.rect.colliderect(trigger.rect):
                    trigger.enabled = False
                    Trigger = True


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Empty, size)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

    def update(self):
        self.rect.x += screen_scroll_x
        self.rect.y += screen_scroll_y


ground = Ground(0, start_pos_y, (bgr_width * 2, 10))
ground1 = Ground(4485 + 485 + 485 + 485 + 485 + 300 - 15, start_pos_y, (1, 3000))
ground_group = pygame.sprite.Group()
ground_group.add(ground, ground1)

Rope_img = pygame.image.load("img/Rope1.png")
rope_collide = False


class Rope(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Rope_img, (10, 720))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

    def update(self):
        global rope_collide
        self.rect.x += screen_scroll_x
        self.rect.y += screen_scroll_y
        screen.blit(self.image, self.rect)
        if player.rect.colliderect(self.rect):
            player.jumping = True
            player.y_vel = 0
            rope_collide = True
        else:
            rope_collide = False


Rope1 = Rope(5600, start_pos_y - 380)
rope_group = pygame.sprite.Group()
rope_group.add(Rope1)

Trigger1 = Triggers(550, start_pos_y, True)
Trigger2 = Triggers(900, start_pos_y, True)
Trigger3 = Triggers(750, start_pos_y, True)
trigger_group = pygame.sprite.Group()
trigger_group.add(Trigger1, Trigger2, Trigger3)

note_group = pygame.sprite.Group()
note1 = Document(4485 + 485 + 485 + 105 + 485 + 485 + 50, start_pos_y - 1000 - 100 - 50 - 50)
note_group.add(note1)
document = False
pause = 0

while run:

    clock.tick(FPS)
    if not start_game and dead == 0 and pause == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        main_menu()
        button1_enabled = True
        button2_enabled = True

        if Credit:
            Return_from_credit = False
            Credit = True
            credit()
            button1_enabled = False
            button2_enabled = False
        if Return_from_credit:
            button1_enabled = True
            button2_enabled = True
            main_menu()
            Credit = False
    elif not start_game and dead > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_text("GAME OVER", 'white', WIDTH // 2 - 200, HEIGHT // 2 - 200, 50)
        Button('EXIT', WIDTH // 2 - 100, HEIGHT // 2, 'Exit', True)

    elif start_game and pause == 0:
        screen.blit(bgr, (bgr_x, bgr_y - 180))
        bgr_x += screen_scroll_x * 0.5
        bgr_y += screen_scroll_y * 0.5
        platform_group.update()
        note_group.draw(screen)
        note_group.update()
        player.draw()
        slash_group.update()
        bullet_group_player.update()
        bullet_group_player.draw(screen)
        bullet_group_enemy.update()
        bullet_group_enemy.draw(screen)
        item_box_group.draw(screen)
        item_box_group.update()
        spark_group.update()
        rope_group.update()
        ground_group.update()
        draw_text(f"AMMO: {player.ammo}", 'light gray', 20, 765, 15)
        draw_text(f"STORED AMMO: {player.stored_ammo}/{player.max_ammo}", 'light gray', 20, 795, 15)
        draw_text(f"HEALTH: {player.health}/{player.max_health}", 'light gray', 20, 825, 15)
        if player.alive:
            if slash:
                player.slash()
            if shoot:
                player.shoot(player)
            if player.jumping:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1)
            else:
                player.update_action(0)
            screen_scroll_x = player.move(moving_left, moving_right)

        temp_ammo = 0
        player.update()

        trigger_group.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if document:
                    if event.key == pygame.K_e:
                        pause = 1
                if event.key == pygame.K_w:
                    moving_up = True
                if event.key == pygame.K_s:
                    moving_down = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_SPACE and player.alive:
                    jump = True
                if event.key == pygame.K_r and player.stored_ammo >= 15:
                    temp_ammo = 15 - player.ammo
                    player.stored_ammo -= temp_ammo
                    player.ammo = 15
                elif event.key == pygame.K_r and player.stored_ammo < 15 and player.stored_ammo + player.ammo >= 15:
                    temp_ammo = 15 - player.ammo
                    player.stored_ammo -= temp_ammo
                    player.ammo = 15
                elif event.key == pygame.K_r and player.stored_ammo < 15 and player.stored_ammo + player.ammo < 15:
                    player.ammo += player.stored_ammo
                    player.stored_ammo = 0
                if event.key == pygame.K_ESCAPE:
                    start_game = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    moving_up = False
                if event.key == pygame.K_s:
                    moving_down = False
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_SPACE:
                    jump = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                shoot = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                slash = True
            if event.type == pygame.MOUSEBUTTONUP:
                shoot = False
                slash = False
        for enemy in enemy_group:
            enemy.update()
            enemy.draw()
            enemy.AI()
        crate_group.update()
        if not player.alive:
            player.update_action(3)
            dead += 1
            death_timer -= 1
        if death_timer == 0:
            start_game = False
    if pause == 1 and document:
        start_game = False
        draw_text("CONGRATULATIONS", 'white', WIDTH // 2 - 300, HEIGHT // 2 - 200, 50)
        draw_text("YOU HAVE COMPLETED THE GAME", 'white', WIDTH // 2 - 500, HEIGHT // 2 - 100, 50)
        Button('EXIT', WIDTH // 2 - 100, HEIGHT // 2, 'Exit', True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    if moving_left and moving_right and jump:
        jump = False
    if Trigger:
        pause = 1
        start_game = False
        if player.rect.colliderect(Trigger1.rect):
            Dialog("Press A-D to move left and right. W-S to climb up and down.")
        elif player.rect.colliderect(Trigger2.rect):
            Dialog("Press SPACE to jump")
        elif player.rect.colliderect(Trigger3.rect):
            Dialog("Left click to shoot and right click to use dagger")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    pause = 0
                    start_game = True
                    Trigger = False
                    counter = 0
                    moving_left = False
                    moving_right = False
    pygame.display.update()
