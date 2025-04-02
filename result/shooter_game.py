#Создай собственный Шутер!
from random import randint
from pygame import *
mixer.init()
font.init()
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))    
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
        self.width = width
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.speed
    def fire(self):
        keys_pressed = key.get_pressed()        
        if keys_pressed[K_SPACE] and self.inmb <= 0 and self.win == 1:
            mega_arrow = Bullet('bullet.png', self.rect.x + self.width/2 - 20, self.rect.y, 7, 40, 120)
            MEGA_arrows.add(mega_arrow)
            self.inmb = 120
            kick.play()
        if keys_pressed[K_SPACE] and self.inmb <= 0:
            arrow = Bullet('bullet.png', self.rect.x + self.width/2 - 10, self.rect.y, 7, 20, 60)
            arrows.add(arrow)
            self.inmb = 120
            kick.play()
        self.inmb -= 1


class Enemy(GameSprite):
    def respawn(self):
        self.rect.x = randint(0 , win_width - 100)
        self.rect.y = randint(-win_height - 200, -win_height)
        self.speed = randint(1, 3)
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.respawn()
            varior.lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

win_height = 750
win_width = 700
window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load('forest.jpg'), (win_width, win_height))
varior = Player('archer.png', 350, 650, 3, 100, 100)
arrows = sprite.Group()
MEGA_arrows = sprite.Group()
varior.lost = -10
varior.win = 0
varior.inmb = 0

font_lose = font.SysFont('Arial', 36)
font_win = font.SysFont('Arial', 36)
font_finish = font.SysFont('Arial', 100)

monsters = sprite.Group()
'''a = 0
b = -10
c = 2'''
for i in range(10):
    bad = Enemy('ufo.png', 0, 800, 2, 100, 100)
    monsters.add(bad)
    '''a += randint(10, 200)
    b -= randint(10, 200)
    b += randint(10, 100)
    c = randint(1, 3)'''

text_fin_win = font_finish.render('YOU WIN', 1, (0, 255, 0))
text_fin_lose = font_finish.render('YOU LOSE', 1, (255, 0, 0 ))
game = True

mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.5)
kick = mixer.Sound('fire.ogg')
clock = time.Clock()

finish = False

while game:
    if not finish:
        varior.update()
        varior.fire()
        monsters.update()
        arrows.update()
        MEGA_arrows.update()

        boom = sprite.groupcollide(monsters, arrows, False, True)
        for i in boom:
            i.respawn()
            varior.win += 1
        
        mega_boom = sprite.groupcollide(monsters, MEGA_arrows, False, False)
        for i in mega_boom:
            i.respawn()
            varior.win += 1

        sprites = sprite.spritecollide(varior, monsters, False)

        text_lose = font_lose.render('Упустил ' + str(varior.lost), 1, (255, 255, 255))
        text_win = font_win.render('Сбил ' + str(varior.win), 1, (255, 255, 255))
    
    
    window.blit(background,(0, 0))
    varior.reset()
    monsters.draw(window)
    arrows.draw(window)
    MEGA_arrows.draw(window)
    window.blit(text_lose, (0, 0))
    window.blit(text_win, (0, 60))

    if varior.win == 15:
        finish = True
        window.blit(text_fin_win, (200, 375))


    if varior.lost == 10:
        finish = True
        window.blit(text_fin_lose, (200, 375))

    if sprites:
        finish = True
        window.blit(text_fin_lose, (200, 375))


    for e in event.get():
       if e.type == QUIT:
          game = False
    clock.tick(60)
    display.update()
