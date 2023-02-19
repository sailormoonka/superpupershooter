from pygame import *
from random import randint 

#фонова музика
mixer.init() 
mixer.music.load('space.ogg') 
mixer.music.play() 
fire_sound = mixer.Sound('fire.ogg') 

font.init() 
font1 = font.Font(None, 36) 
font2 = font.Font(None, 80) 
win = font2.render('YOU WON!', True, (255, 255, 255)) 
lose = font2.render('YOU LOSE!', True, (180, 0, 0))

#нам потрібні такі каринки: 
img_back = "galaxy.jpg" #фон гри
img_hero = "rocket.png" #герой 
img_enemy = "ufo.png" #ворог
img_bullet = "bullet.png" 

lost = 0 
score = 0

#клас-батько для інших спрайтів
class GameSprite(sprite.Sprite): 
    #конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed): 
        #викликаємо конструктор класу (Sprite): 
        sprite.Sprite.__init__(self) 
        #кожен спрайт повинен зберігати властивість image - зображення  
        self.image = transform.scale( 
            image.load(player_image), (size_x, size_y)) 
        self.speed = player_speed 
    
        #кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y 
    
    #метод, що малює героя на вікні
    def reset(self): 
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    #метод для керування спрайтом стрілками клавіатури
    def update(self): 
        keys = key.get_pressed() 
        if keys[K_LEFT] and self.rect.x > 5: 
            self.rect.x = self.speed 
        if keys [K_RIGHT] and self.rect.x < win_width - 80: 
            self.rect.x += self.speed 
            
    #метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self): 
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15) 
        bullets.add(bullet) 
        
#клас спрайта - кулі
class Bullet(GameSprite): 
    #рух ворога
    def update(self): 
        self.rect.y += self.speed 
        #зникає, якщо підійде до краю екрана 
        if self.rect.y < 0: 
            self.kill()

class Enemy (GameSprite): 
    def update(self): 
        self.rect.y += self.speed 
        global lost 
        if self.rect.y> win_height:
            self.rect.x = randint(80, win_width - 80) 
            self.rect.y = 0 
            lost = lost + 1 

#створюємо віконце 
win_width = 700 
win_height = 500 
display.set_caption("Shooter") 
window = display.set_mode((win_width, win_height)) 
background = transform.scale(image.load(img_back), (win_width, win_height)) 

#створюємо спрайти 
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10) 

monsters = sprite.Group()
for i in range (1, 6):
    monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1, 5)) 
    monsters.add(monster) 
    
bullets = sprite.Group() 

#зміна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False 

#основний цикл гри: 
run = True #прапорець скидається кнопкою закриття вікна 

while run: 
    #подія натискання на кнопку Закрити
    for e in event.get(): 
        if e.type == QUIT: 
            run = False
        elif e.type == KEYDOWN: 
            if e.key == K_SPACE: 
                fire_sound.play() 
                ship.fire()
    if not finish: 
        #оновлюємо фон 
        window.blit(background, (0, 0)) 
        
        text_score = font1.render("Paxyнoк: "+str(score), 1, (255,255,255))
        window.blit(text_score, (0, 0))
        
        text_lose = font1.render("Пропущено: "+str(lost), 1, (255,255,255)) 
        window.blit(text_lose, (0, 30)) 
        #рухи спрайтів 
        ship.update() 
        
        #оновлюємо їх у новому місці при кожній ітерації циклу
        ship.reset() 
        
        monsters.update() 
        bullets.update() 
        monsters.draw(window) 
        bullets.draw(window) 
        collides = sprite.groupcollide(monsters, bullets, True, True)

        for c in collides: 
            score = score + 1 
            monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1, 5)) 
            monsters.add(monster) 
        if sprite.spritecollide(ship, monsters, False) or lost >= 3: 
            finish = True 
            window.blit(lose, (200, 200)) 
        if score >= 10: 
            finish = True 
            window.blit(win, (200, 200)) 
        display.update() 
    #цикл спрацьовує кожні 0.05 секунд
    time.delay (50)








