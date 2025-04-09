import pygame
# gerekli olabilecek renklerin tanimi
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class PacMan(pygame.sprite.Sprite):
    # sprite sinifini miras aliyor ve pacman bir sprite oluyor. 
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pacmanright.png").convert()
        # resme dikdortgen alani tanimlar hareket ve carpisma kontrolu icin
        self.rect = self.image.get_rect()
        # toplanan coin sayisi
        self.coins = 0
        # pacmanin hizi
        self.speed = 2
        # konumu
        self.cell = [0,0]
        # gitmesi gereken hedef hucre 
        self.check_goal = [9, 15]
        # n no movement yani hareket yoku simgeler 
        self.dir = "n"

    def update(self):
        #bu metod surekli calisacak ve hareket yonune gore pozisyin degistirecek

        if self.dir == 'r':
            self.rect.x += self.speed
        elif self.dir == 'l':
            self.rect.x -= self.speed
        elif self.dir == 'u':
            self.rect.y -= self.speed
        elif self.dir == 'd':
            self.rect.y += self.speed


        # her hucre 32 piksel grid poziyonunu piksele cevirdik 
        if (self.check_goal[0] * 32 == self.rect.x) & (self.check_goal[1] * 32 == self.rect.y):
            # eger tam hedef hucreye geldiyse durdur
            self.dir = 'n'
            # bulundugu yer artik hedef hucresidir
            self.cell = self.check_goal
        

  

    def draw(self, screen):
        if self.dir == 'r': # sag 
            self.image = pygame.image.load("pacmanright.png").convert()
        elif self.dir == 'd': # asagi
            self.image = pygame.image.load("pacmandown.png").convert()
        elif self.dir == 'u': # yukari 
            self.image = pygame.image.load("pacmanup.png").convert()
        elif self.dir == 'l': # sol
            self.image = pygame.image.load("pacmanleft.png").convert()
        screen.blit(self.image, [self.rect.x, self.rect.y])
        
class GridCell():
    """cell bilgilerini tutan class"""
    def __init__(self):
        self.cell = [0,0]
        self.position = [0,0]
        self.walkable = False
        self.coin = False
        
class DummyPac:
    def __init__(self, cell):
        self.cell = cell

class SearchNode():
    def __init__(self, location = None, pred = None):
        self.cell = location
        '''A starda kullanilacak olan f ve g 
        g baslangicta buraya kadar olan makiyet 
        f toplam maliyeti tutacak
        pred ise dugumun nerden geldigini tutacak
        location ise konumunu tutacak'''
        self.f = 0 # f toplam maliyet
        #  Hedef düğüme olan tahmin edilen maliyet veya heuristic (kavram). Bu, algoritmanın hedefe doğru yönelmesini sağlayan, 
        # hedefe olan uzaklıkla ilgili tahmini bir değerdir. Örneğin, bir ızgara üzerinde Manhattan mesafesi hesaplanabilir.
        self.g = 0 # başlangıç düğümünden şu anki düğüme kadar olan toplam maliyeti ifade eder.
        #Genellikle, her adımda bir birim maliyet olarak kabul edilir, 
        self.pred = pred

class Ghost(pygame.sprite.Sprite):
    """ghost sprites """
    def __init__(self, color):
        super().__init__()
        self.speed = 2
        if color == "orange":
            self.image = pygame.transform.scale(pygame.image.load("orange.png").convert(), (32, 32))
            self.image.set_colorkey(WHITE)
        elif color == "green":
            self.image = pygame.transform.scale(pygame.image.load("blue.png").convert(), (32, 32))
            self.image.set_colorkey(WHITE)
        elif color == "pink":
            self.image = pygame.transform.scale(pygame.image.load("pink.png").convert(), (32, 32))
            self.image.set_colorkey(WHITE)
        elif color == "red":
            self.image = pygame.transform.scale(pygame.image.load("red.png").convert(), (32, 32))
            self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.cell = [0,0]
        self.check_goal = [9, 15]
        self.dir = "n"

    def update(self):
        if self.dir == 'r':
            self.rect.x += self.speed
        elif self.dir == 'l':
            self.rect.x -= self.speed
        elif self.dir == 'u':
            self.rect.y -= self.speed
        elif self.dir == 'd':
            self.rect.y += self.speed

        # goal olup olmadigini kontrol etmemiz gerek
        if (self.check_goal[0] * 32 == self.rect.x) & (self.check_goal[1] * 32 == self.rect.y):
            self.dir = 'n'
            self.cell = self.check_goal
    # blit : resmi ekrana yapistirir
    # draw : bu islemi her framede cagirarak pacmani gorunur yapar
    def draw(self, screen):
        screen.blit(self.image, [self.rect.x, self.rect.y])      