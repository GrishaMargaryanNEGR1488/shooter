import random
from time import time as time_get
from pygame import*

font.init()
#Переменные, задающие размеры игровой сцены и спрайтов
SCREEN_SIZE = (920, 980)
SPRITE_SIZE = 70
WHITE = (255, 255, 255)

def show_label(text: str, x: int, y: int, font_size: int, font_name: str ='Arial', color: tuple = WHITE) -> None:
    '''
    Функция выводит надпись на игровуй сцену window.

    Аргументы:
    x, y - координаты выводимого текста
    text - выводимый текст
    font_name - имя шрифта, которым будет написан текст 
    color - цвет текста (RGB)
    font_size - размер шрифта
    '''
    font1 = font.SysFont(font_name, font_size)
    text = font1.render(text, True, color)
    window.blit(text, (x, y))


def show_text(text):
    font.init()
    font1 = font.SysFont('Arial', 40)
    text = font1.render(text, True, (255, 255, 255))
    window.blit(text, (250, 200))
    return True

class GameSprite(sprite.Sprite):
    '''
    Родительский класс для всех ишгровых объектов
    '''
    def __init__(self, player_image: str, player_x: int, player_y: int, player_speed: int) -> None:
        '''
        Аргументы:

        x, y - координаты выводимого текста
        image_name - имя файла-картинки, которая отображает жизнь
        speed - скорость движения спрайта
        '''
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self) -> None:
        '''Отрисосвывает сам спрайт на экране'''
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    '''Класс для игрока'''
    def update(self) -> None:
        '''
        Обарабатывает нажатие клавиш:

        a, d - left, right
        space - shoot
        '''
        key_presssed = key.get_pressed()        
        if key_presssed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed            
        if key_presssed[K_d]and self.rect.x < 700 - self.rect.width:
            self.rect.x += self.speed        
        if key_presssed[K_SPACE]:
            try:
                if time_get() - self.shoot_time > .3:
                    self.shoot()
            except:
                self.shoot()
    def shoot(self) -> None:
        '''Метод для выстрела'''
        for i in range(3):
            b2 = Bullet('bullet.png', self.rect.x + 27, self.rect.y, 7, 10, 30, direction=i)
            bullets.add(b2)
        self.shoot_time = time_get()

class Lives:
    '''
    Жизни для игрока
    ''' 
    def __init__(self, lives: int, x: int, y: int, image_name: str):
        '''
        x, y - координаты, от которой начинается отрисовка жизней
        image_name - имя файла-картинки, которая отображает жизнь
        lives - количество жизней
        '''
        self.lives = lives
        self.x = x
        self.y = y
        self.image= transform.scale(image.load('heart.png'), (30, 30))
    def draw(self):
        '''
        Отрисовывают жизни на экране
        '''
        window.blit(self.image, (self.x, self.y))
               

class Enemy(GameSprite):
    def __init__(self, player_image: str, player_x: int, player_y: int, player_speed: int) -> None:
        '''
        Аргументы:

        x, y - координаты выводимого текста
        image_name - имя файла-картинки, которая отображает жизнь
        speed - скорость движения спрайта
        '''
    def update(self):
        '''
        Движение врагов вниз.
        Если враг долетает до низа игровой сцены, то переставляем его наврех и увеличиваем счетчик пропущенный врагов.
        '''
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = random.randint(1, 635)
            missed.counter += 1


class Asteroid(GameSprite):
    '''Класс для астероидов'''
    def __init__(self, player_image, player_x, player_y, player_speed, size):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(self.image, (size, size)) 
    def update(self):
        '''Движение астероидов вниз'''
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = random.randint(1, 635)

        

class Counter:
    def __init__(self, text: str, x: int, y: int):
        self.counter = 0
        self.text = text
        self.position = (x, y)

    def show(self):
        font.init()
        font1 = font.SysFont('Arial', 20)
        text = font1.render(self.text + str(self.counter), True, (255,255,255))
        window.blit(text, self.position)

class Bullet(GameSprite):
    '''Класс для пуль'''
    def __init__(self, player_image, player_x, player_y, player_speed, w,h, direction):
        '''
        Аргументы:

        x, y - координаты выводимого текста
        image_name - имя файла-картинки, которая отображает жизнь
        speed - скорость движения спрайта
        directiuon - направление
            0 - вертикально вверх
            1 - вверх и влево
            2 - вверх и вправо
        '''
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (w, h))
        self.direction = direction
    def update(self):
        if  self.direction == 1:
            self.rect.x -= 1
        if  self.direction == 2:
            self.rect.x += 1
            
        self.rect.y -= self.speed

lives = Lives(3, 650, 20)
        

missed = Counter('Список пропущенных врагов: ', 10,10)
killed = Counter('Список убитых врагов: ', 10,35)

bullets = sprite.Group()
asteroids = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monsters.add(Enemy('ufo.png', random.randint(1, 635), 0, random.randint(1, 3)))
for i in range(2):
    asteroids.add(Asteroid('asteroid.png', random.randint(1, 635), 0, random.randint(1, 3), random.randint(30, 50)))
player = Player('rocket.png', 300,435, 5)
window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
game = True
finish = False
clock = time.Clock()

while game:
    clock.tick(60)
    if finish == False:
        #Перерисовка всех объектов в игре
        window.blit(background, (0, 0))
        asteroids.update()
        asteroids.draw(window)
        player.update()
        player.reset()
        missed.show()
        killed.show()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        lives.draw()
        bullets.draw(window)
        sprites_list = sprite.groupcollide(monsters, bullets, False, True)
        for b in sprites_list:
            b.rect.y = 0
            b.rect.x = random.randint(1, 635)
            killed.counter += 1
        if killed.counter >= 10:
            show_text('You win!')
            finish = True
            
        if missed.counter >= 3 or sprite.spritecollideany(player, monsters) or sprite.spritecollideany(player, asteroids):
            show_text('You lose!')
            finish = True
        
        if lives.lives <= 0:
            show_text('YOU LOOOSEE')
            finish = True
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            for s in sprite.spritecollide(player, monsters, False) + sprite.spritecollide(player, asteroids, False):
                s.rect.y = 0
                s.rect.x = random.randint(1, 635)
                lives.lives -= 1

        display.update()    

    
    
    for e in event.get():
        if e.type == QUIT:
            game = False
