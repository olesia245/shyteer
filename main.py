import time

from pygame import *
from random import *
wids = 500
heght = 700
window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700,500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
clock = time.Clock()
FPS = 60

game = True

class GameSprite(sprite.Sprite):
    def __init__(self,player, player_x, player_y, speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 700-85:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
    def file(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 20)
        bullets.add(bullet)

lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= wids:
            self.rect.y = 0
            self.rect.x = randint(10,500)
            lost += 1

bullets = sprite.Group()

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        global lost
        if self.rect.y <= 0:
            self.kill()

player = Player('rocket.png', 0, 400, 5 ,70, 100)
enemy = Enemy('ufo.png', 450, 0, 2, 80, 70)
enemy1 = Enemy('ufo.png', 300, 10, 1, 80, 70)
enemy2 = Enemy('ufo.png', 200, 50, 1, 80, 70)
enemy3 = Enemy('ufo.png', 100, 100, 1, 80, 70)
enemy4 = Enemy('ufo.png', 50, 150, 1, 80, 70)
monsters = sprite.Group()
monsters.add(enemy)
monsters.add(enemy1)
monsters.add(enemy2)
monsters.add(enemy3)
monsters.add(enemy4)

font.init()
font1 = font.Font(None,36)
font2 = font.Font(None,100)

finish = True

kills = 0

text_lose1 = font2.render('YOU LOSE', 5, (255, 255, 255))
text_lose2 = font2.render('YOU WIN', 1, (255, 255, 255))

while game:

    if finish:
        window.blit(background, (0, 0))

        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (0, 0))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            enemy = Enemy('ufo.png', randint(30, 650), 0, 2, 80, 70)
            monsters.add(enemy)
            kills += 1

        text_kills = font1.render("Убито: " + str(kills), 1, (255, 255, 255))
        window.blit(text_kills, (0, 30))

        bullets.update()
        bullets.draw(window)
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)

        if kills == 10:
            finish = False
            window.blit(background, (0, 0))
            window.blit(text_lose2, (200, 250))

        if lost >= 3:
            finish = False

            window.blit(text_lose1, (200, 250))

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                player.file()

    display.update()
    clock.tick(FPS)