import pygame
from searchAlgos import *
from classes import *
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

score = 0

pygame.init()
size = (608, 608)
font = pygame.font.SysFont('Arial', 25, False, True) 
screen = pygame.display.set_mode(size)
pygame.display.set_caption("WELCOME TO PACMAN GAME")
cells = init_grid("gridbackground.png")
coin = pygame.image.load("nomdot.png").convert()
coin.set_colorkey(BLACK)
background = pygame.image.load("gridbackground.png").convert()


pacman = PacMan()
pacman.rect.x = 9 * 32
pacman.rect.y = 15 * 32

PINKY = Ghost("pink")
PINKY.rect.x = 17 * 32
PINKY.rect.y = 17 * 32
PINKY.cell = [17,17]

BLINKY = Ghost("red")
BLINKY.rect.x = 1 * 32
BLINKY.rect.y = 17 * 32
BLINKY.cell = [1,17]

INKY = Ghost("green")
INKY.rect.x = 1 * 32
INKY.rect.y = 1 * 32
INKY.cell = [1,1]

CLYDE = Ghost("orange")
CLYDE.rect.x = 17 * 32
CLYDE.rect.y = 1 * 32
CLYDE.cell = [17,1]

framecount = 0
done = False
clock = pygame.time.Clock()
start = time.time()
buttonState = 'n'


# -------- MAIN GAME Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = time.time()
            print("SCORE: " + str(score))
            done = True  
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                end = time.time()
                print("oyun bitti")
                print("SCORE " + str(score))
                done =  True

    # Oyun döngüsü içinde
    keys = pygame.key.get_pressed()
    row, col = pacman.cell
    if keys[pygame.K_LEFT]:
        if (pacman.dir != 'u' and pacman.dir != 'd') and row > 0 and cells[row - 1][col].walkable:
            pacman.check_goal = [row - 1, col]
            pacman.dir = 'l'

            # SAĞ
    if keys[pygame.K_RIGHT]:
        if (pacman.dir != 'u' and pacman.dir != 'd') and row < len(cells) - 1 and cells[row + 1][col].walkable:
            pacman.check_goal = [row + 1, col]
            pacman.dir = 'r'

            # YUKARI
    if keys[pygame.K_UP]:
        if (pacman.dir != 'l' and pacman.dir != 'r') and col > 0 and cells[row][col - 1].walkable:
            pacman.check_goal = [row, col - 1]
            pacman.dir = 'u'

            # AŞAĞI
    if keys[pygame.K_DOWN]:
        if (pacman.dir != 'l' and pacman.dir != 'r') and col < len(cells[0]) - 1 and cells[row][col + 1].walkable:
            pacman.check_goal = [row, col + 1]
            pacman.dir = 'd'

    pacman.update()

    if cells[pacman.cell[0]][pacman.cell[1]].coin == True:
        cells[pacman.cell[0]][pacman.cell[1]].coin = False
        score += 1
    score_text = "Score: " + str(score)
    text = font.render(score_text, True, WHITE)
    if score == 164:
        end = time.time()
        print("TUM COINLERI TOPLADINN!!!")
        print("TIME :  " + str(end - start) + " seconds")
        pygame.quit()
    numExpanded = 0
    totalNodes = 0
    if framecount == 0:
        def is_valid(loc, cells):
            x, y = loc
            return 0 <= x < len(cells) and 0 <= y < len(cells[0]) and cells[x][y].walkable
        dir_to_offset = {'r': (1, 0), 'l': (-1, 0), 'u': (0, -1), 'd': (0, 1)}
        px, py = pacman.cell
        dx, dy = dir_to_offset.get(pacman.dir, (0, 0))  # fallback for 'n'

        # Pac-Man'in önündeki hücreyi bul
        front = [px + 3*dx, py + 3*dy ]
        pac = [px,py]

        # Pac-Man'in arkasındaki hücreyi bul
        back = [px - 3*dx, py - 3*dy]

        # Sağ ve sol hücreleri hesapla
        right = [px + dy, py - dx ]
        left = [px - dy, py + dx]

        # INKY - Pac-Man'in önü

        compTimeStart = time.time()
        INKY.check_goal, numExpanded, totalNodes = BFSWithoutHeuristic(INKY, pacman, cells)
        compTimeEnd = time.time()
        print("BFSWithoutHeuristic")
        print("Nodes Expanded:", numExpanded)
        print("Total Nodes:", totalNodes)
        print("Time:", compTimeEnd - compTimeStart)
        print()
        
        # INKY - Pac-Man'in önü
        compTimeStart = time.time()
        PINKY.check_goal, numExpanded, totalNodes = subGoalAStar(PINKY, pacman, cells)
        compTimeEnd = time.time()
        print("subGoalAStar")
        print("Nodes Expanded:", numExpanded)
        print("Total Nodes:", totalNodes)
        print("Time:", compTimeEnd - compTimeStart)
        print()

        # BLINKY - sağ taraf
        compTimeStart = time.time()
                
        BLINKY.check_goal, numExpanded, totalNodes = aStarGhost(BLINKY, pacman, cells)
        compTimeEnd = time.time()
        print("aStarGhost")
        print("Nodes Expanded:", numExpanded)
        print("Total Nodes:", totalNodes)
        print("Time:", compTimeEnd - compTimeStart)
        print()

        # CLYDE - sol taraf
        compTimeStart = time.time()
        CLYDE.check_goal, numExpanded, totalNodes = BFS(CLYDE, pacman, cells)
        compTimeEnd = time.time()
        print("BFS")
        print("Nodes Expanded:", numExpanded)
        print("Total Nodes:", totalNodes)
        print("Time:", compTimeEnd - compTimeStart)
        print()
        
        end = time.time()
        

    if INKY.check_goal[0] < INKY.cell[0]:
        INKY.dir = "l"
    elif INKY.check_goal[0] > INKY.cell[0]:
        INKY.dir = "r"
    elif INKY.check_goal[1] < INKY.cell[1]:
        INKY.dir = "u"
    elif INKY.check_goal[1] > INKY.cell[1]:
        INKY.dir = "d"
    INKY.update()

    
    if BLINKY.check_goal[0] < BLINKY.cell[0]:
        BLINKY.dir = "l"
    elif BLINKY.check_goal[0] > BLINKY.cell[0]:
        BLINKY.dir = "r"
    elif BLINKY.check_goal[1] < BLINKY.cell[1]:
        BLINKY.dir = "u"
    elif BLINKY.check_goal[1] > BLINKY.cell[1]:
        BLINKY.dir = "d"
    BLINKY.update()

    if CLYDE.check_goal[0] < CLYDE.cell[0]:
        CLYDE.dir = "l"
    elif CLYDE.check_goal[0] > CLYDE.cell[0]:
        CLYDE.dir = "r"
    elif CLYDE.check_goal[1] < CLYDE.cell[1]:
        CLYDE.dir = "u"
    elif CLYDE.check_goal[1] > CLYDE.cell[1]:
        CLYDE.dir = "d"
    CLYDE.update()

    if PINKY.check_goal[0] < PINKY.cell[0]:
        PINKY.dir = "l"
    elif PINKY.check_goal[0] > PINKY.cell[0]:
        PINKY.dir = "r"
    elif PINKY.check_goal[1] < PINKY.cell[1]:
        PINKY.dir = "u"
    elif PINKY.check_goal[1] > PINKY.cell[1]:
        PINKY.dir = "d"
    PINKY.update()
     
   

    if checkCollissions(pacman, INKY, BLINKY, CLYDE , PINKY) == -1:
        end = time.time()
        print("Öldün")
        print("score ", score)
        pygame.quit()

    screen.blit(background, [0,0])
    screen.blit(text, [267, 10 * 32])
    
    for i in range(19):
        for j in range(19):
            if cells[i][j].coin:
                screen.blit(coin, [i * 32, j * 32])
    pacman.draw(screen)
    INKY.draw(screen)
    BLINKY.draw(screen)
    CLYDE.draw(screen)
    PINKY.draw(screen)
    

    pygame.display.flip()

    framecount = (framecount + 1) % 16
    if framecount == 0:
        INKY.update()
        BLINKY.update()
        CLYDE.update()
        PINKY.update()

    clock.tick(64)
pygame.quit()