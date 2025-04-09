from classes import *
from PIL import Image
from pprint import pprint
from collections import deque

import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

            
                
def checkCollissions(pacman, INKY, BLINKY, CLYDE , PINKY):
    if pacman.cell == INKY.cell:
        return -1
    if pacman.cell == BLINKY.cell:
        return -1
    if pacman.cell == CLYDE.cell:
        return -1
    if pacman.cell == PINKY.cell:
        return -1


def aStarGhost(ghost, pac, cells):
    # f = g + h


    inf = float("inf")
    # yurunemeyen hucrelerin maliyeti sonsuz 
    visited = []
    # ziyaret edilenler

    unvisited = [] # daha ziyaret edilmeyenler
    unvisited.append(SearchNode(ghost.cell))
    #baslangıc noktası notvisitide eklenir 
    goalNode = SearchNode(pac.cell)

    while len(unvisited) > 0:
        # en düşük g + h = f değerine sahip olanı seçeceğiz
        distance = 0
        index = 0
        expandingNode = unvisited[0]
        for i in range(len(unvisited)):
            if expandingNode.f > unvisited[i].f:
                expandingNode = unvisited[i]
                index = i

        visited.append(unvisited.pop(index))

        if expandingNode.cell == goalNode.cell:
            goalNode = expandingNode
            break
            
        expandingNodeX = expandingNode.cell[0]
        expandingNodeY = expandingNode.cell[1]

        # yeni düğümler oluşturuyoruz. 
        left = SearchNode([expandingNodeX - 1,expandingNodeY], expandingNode)
        right = SearchNode([expandingNodeX + 1,expandingNodeY], expandingNode)
        up = SearchNode([expandingNodeX,expandingNodeY - 1], expandingNode)
        down = SearchNode([expandingNodeX,expandingNodeY + 1], expandingNode)

        rightbool = True
        leftbool = True
        upbool = True
        downbool = True
        for i in visited:
            #eğer bu komsular zaten visitedse tekrar işlenemez
            if i.cell == left.cell:
                leftbool = False
            if i.cell == right.cell:
                rightbool = False
            if i.cell == up.cell:
                upbool = False
            if i.cell == down.cell:
                downbool = False

        if rightbool:
            if cells[right.cell[0]][right.cell[1]].walkable == False:
                right.g = inf
                right.f = inf
            else:
                right.g = right.pred.g + 1
                distance = abs(goalNode.cell[0] - right.cell[0]) + abs(goalNode.cell[1] - right.cell[1])
                right.f = right.g + distance
            unvisited.append(right)
        if leftbool:
            if cells[left.cell[0]][left.cell[1]].walkable == False:
                left.g = inf
                left.f = inf
                #eger yurunemıyorsa sonsuz olarak ayarlanır
            else:
                #g maliyetine bir eklenir h ise manhattan mesafesi olarka hesaplanır 
                left.g = left.pred.g + 1
                distance = abs(goalNode.cell[0] - left.cell[0]) + abs(goalNode.cell[1] - left.cell[1])
                left.f = left.g + distance
            unvisited.append(left)
        if upbool:
            if cells[up.cell[0]][up.cell[1]].walkable == False:
                up.g = inf
                up.f = inf
            else:
                up.g = up.pred.g + 1
                distance = abs(goalNode.cell[0] - up.cell[0]) + abs(goalNode.cell[1] - up.cell[1])
                up.f = up.g + distance
            unvisited.append(up)
        if downbool:
            if cells[down.cell[0]][down.cell[1]].walkable == False:
                down.g = inf
                down.f = inf
            else:
                down.g = down.pred.g + 1
                distance = abs(goalNode.cell[0] - down.cell[0]) + abs(goalNode.cell[1] - down.cell[1])
                down.f = down.g + distance
            unvisited.append(down)
    # hayaletin pacmane doğru atması gereken ilk adım step hesaplanır
    
    node1 = goalNode
    step = goalNode

    while node1.cell != ghost.cell:
        step = node1
        node1 = node1.pred


    return step.cell, len(visited), len(visited) + len(visited)


def BFS(ghost, pac, cells):
    inf = float("inf")
    visited = []
    unvisited = []
    unvisited.append(SearchNode(ghost.cell))
    
    # Pacman'ın mevcut konumu
    pac_cell = pac.cell
    
    # Pacman'ın 2 adım ilerisindeki hücreyi kontrol et
    pac_x, pac_y = pac_cell[0], pac_cell[1]
    
    # İki adım ilerisini kontrol et (yukarı, aşağı, sağa, sola)
    target_cell = pac_cell  # Default hedef Pacman'ın kendisi
    
    # Dört yönü kontrol et: Up, Down, Left, Right
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # iki adım ileri gitme
    for dx, dy in directions:
        new_x = pac_x + dx
        new_y = pac_y + dy
        
        if 0 <= new_x < len(cells) and 0 <= new_y < len(cells[0]):  # Geçerli koordinat
            if cells[new_x][new_y].walkable:  # Eğer geçilebiliyorsa
                target_cell = [new_x, new_y]  # Hedefi iki adım ileriye ayarla
                break  # İlk geçilebilir hücreyi bulduğumuzda döngüyü bitir
    
    goalNode = SearchNode(target_cell)  # Hedef olarak belirlenen hücreyi kullan

    while len(unvisited) > 0:
        distance = 0
        index = 0
        expandingNode = unvisited[0]
        for i in range(len(unvisited)):
            if expandingNode.f > unvisited[i].f:
                expandingNode = unvisited[i]
                index = i

        visited.append(unvisited.pop(index))
        if expandingNode.cell == goalNode.cell:
            goalNode = expandingNode
            break
        #hedefe ulaşma durumu 
        expandingNodeX = expandingNode.cell[0]
        expandingNodeY = expandingNode.cell[1]

        left = SearchNode([expandingNodeX - 1,expandingNodeY], expandingNode)
        right = SearchNode([expandingNodeX + 1,expandingNodeY], expandingNode) 
        up = SearchNode([expandingNodeX,expandingNodeY - 1], expandingNode)
        down = SearchNode([expandingNodeX,expandingNodeY + 1], expandingNode)

        rightbool = True
        leftbool = True
        upbool = True
        downbool = True
                
        for i in visited:
            if i.cell == left.cell:
                leftbool = False
            if i.cell == right.cell:
                rightbool = False
            if i.cell == up.cell:
                upbool = False
            if i.cell == down.cell:
                downbool = False

        # Right hücresini kontrol et
        if rightbool:
            if 0 <= right.cell[0] < len(cells) and 0 <= right.cell[1] < len(cells[0]):  # Geçerli hücre
                if cells[right.cell[0]][right.cell[1]].walkable == False:
                    right.g = inf
                    right.f = inf
                else:
                    right.g = right.pred.g + 1
                    right.f = right.g
                unvisited.append(right)

        # Left hücresini kontrol et
        #f = g
        if leftbool:
            if 0 <= left.cell[0] < len(cells) and 0 <= left.cell[1] < len(cells[0]):  # Geçerli hücre
                if cells[left.cell[0]][left.cell[1]].walkable == False:
                    left.g = inf
                    left.f = inf
                else:
                    left.g = left.pred.g + 1
                    left.f = left.g
                unvisited.append(left)

        # Up hücresini kontrol et
        if upbool:
            if 0 <= up.cell[0] < len(cells) and 0 <= up.cell[1] < len(cells[0]):  # Geçerli hücre
                if cells[up.cell[0]][up.cell[1]].walkable == False:
                    up.g = inf
                    up.f = inf
                else:
                    up.g = up.pred.g + 1
                    up.f = up.g
                unvisited.append(up)

        # Down hücresini kontrol et
        if downbool:
            if 0 <= down.cell[0] < len(cells) and 0 <= down.cell[1] < len(cells[0]):  # Geçerli hücre
                if cells[down.cell[0]][down.cell[1]].walkable == False:
                    down.g = inf
                    down.f = inf
                else:
                    down.g = down.pred.g + 1
                    down.f = down.g
                unvisited.append(down)

    node1 = goalNode
    step = goalNode

    while node1.cell != ghost.cell:
        step = node1
        node1 = node1.pred

    return step.cell, len(visited), len(visited) + len(unvisited)

import random


def subGoalAStar(ghost, pac, cells):
    inf = float("inf")
    visited = []
    unvisited = []
    unvisited.append(SearchNode(ghost.cell))
    pac_cell = pac.cell
    pac_x, pac_y = pac_cell[0], pac_cell[1]
    target_cell = pac_cell  # Default hedef Pacman'ın kendisi
    
    # Dört yönü kontrol et: Up, Down, Left, Right
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # iki adım geriye gitme
    for dx, dy in directions:
        new_x = pac_x + dx
        new_y = pac_y + dy
        
        if 0 <= new_x < len(cells) and 0 <= new_y < len(cells[0]):  # Geçerli koordinat
            if cells[new_x][new_y].walkable:  # Eğer geçilebiliyorsa
                target_cell = [new_x, new_y]  # Hedefi iki adım geriye ayarla
                break  # İlk geçilebilir hücreyi bulduğumuzda döngüyü bitir
    
    goalNode = SearchNode(target_cell)  # Hedef olarak belirlenen hücreyi kullan
    #gercek hedef ama biz buraya gitmek zorunda değiliz 


    #en fazla 39 adım ilerleyeğiz hedefe ulaşırsak daha erken duracağız
    #39 adım içinde hedefe ulaşmazsak o ana kadarki en ilerideki node en son expand edilen node ara hedefimiz olur 

    num = 0
    while len(unvisited) > 0:
        num = num + 1
        distance = 0
        index = 0
        expandingNode = unvisited[0]
        for i in range(len(unvisited)):
            if expandingNode.f > unvisited[i].f:
                expandingNode = unvisited[i]
                index = i

        visited.append(unvisited.pop(index))

        if expandingNode.cell == goalNode.cell:
            #hedef hücreyi bulduğumuzu işaret eder
            goalNode = expandingNode
            break
        elif num == 39:
            goalNode = expandingNode
            break           
        expandingNodeX = expandingNode.cell[0]
        expandingNodeY = expandingNode.cell[1]

        
        left = SearchNode([expandingNodeX - 1,expandingNodeY], expandingNode)
        right = SearchNode([expandingNodeX + 1,expandingNodeY], expandingNode)
        up = SearchNode([expandingNodeX,expandingNodeY - 1], expandingNode)
        down = SearchNode([expandingNodeX,expandingNodeY + 1], expandingNode)

        rightbool = True
        leftbool = True
        upbool = True
        downbool = True
        for i in visited:
            if i.cell == left.cell:
                leftbool = False
            if i.cell == right.cell:
                rightbool = False
            if i.cell == up.cell:
                upbool = False
            if i.cell == down.cell:
                downbool = False

        # komşu hücreleri oluştur ve yürünebilir olmasına göre update et 
        #yürünemezse infinitive yap yürünebilirse f ve g değerlerini ata 
        if rightbool:
            if cells[right.cell[0]][right.cell[1]].walkable == False:
                right.g = inf
                right.f = inf
            else:
                right.g = right.pred.g + 1
                distance = abs(goalNode.cell[0] - right.cell[0]) + abs(goalNode.cell[1] - right.cell[1])
                right.f = right.g + distance
            unvisited.append(right)
        if leftbool:
            if cells[left.cell[0]][left.cell[1]].walkable == False:
                left.g = inf
                left.f = inf
            else:
                left.g = left.pred.g + 1
                distance = abs(goalNode.cell[0] - left.cell[0]) + abs(goalNode.cell[1] - left.cell[1])
                left.f = left.g + distance
            unvisited.append(left)
        if upbool:
            if cells[up.cell[0]][up.cell[1]].walkable == False:
                up.g = inf
                up.f = inf
            else:
                up.g = up.pred.g + 1
                distance = abs(goalNode.cell[0] - up.cell[0]) + abs(goalNode.cell[1] - up.cell[1])
                up.f = up.g + distance
            unvisited.append(up)
        if downbool:
            if cells[down.cell[0]][down.cell[1]].walkable == False:
                down.g = inf
                down.f = inf
            else:
                down.g = down.pred.g + 1
                distance = abs(goalNode.cell[0] - down.cell[0]) + abs(goalNode.cell[1] - down.cell[1])
                down.f = down.g + distance
            unvisited.append(down)

#son olarak goal nodedan geriye doğru giderek ghost.cell e ulaşana kadar predleri takip ederiz ve bir sonraki 
#adımda gidilecek hücreyi node2.cell i döndürürüz. 
    
    node1 = goalNode
    node2 = goalNode

    while node1.cell != ghost.cell:
        node2 = node1
        node1 = node1.pred


    return node2.cell, len(visited), len(visited) + len(unvisited)



# daha hızlı karar verebilir 
# daha az hesaplama yapar 
# anlık değişimlere uyum yeteneği arta 
# yüksek kompleks olan durumlarda basitleştirme sağlar 

import random

def DFS(ghost, pac, cells):
    visited = []
    unvisited = []
    unvisited.append(SearchNode(ghost.cell))
    goalNode = SearchNode(pac.cell)

    while len(unvisited) > 0:
        expandingNode = unvisited.pop()  # Stack'ten son ekleneni al (DFS)
        
        # Hücre bazlı ziyaret kontrolü
        if any(node.cell == expandingNode.cell for node in visited):
            continue
        
        visited.append(expandingNode)
        
        if expandingNode.cell == goalNode.cell:
            goalNode = expandingNode
            break

        x, y = expandingNode.cell[0], expandingNode.cell[1]
    
        neighbors = [
                ('down', SearchNode([x, y+1], expandingNode)),
                ('up', SearchNode([x, y-1], expandingNode)),
                ('right', SearchNode([x+1, y], expandingNode)),
                ('left', SearchNode([x-1, y], expandingNode))
        ]
        random.shuffle(neighbors)  # Pinky için rastgelelik

        for direction, neighbor in neighbors:
            nx, ny = neighbor.cell[0], neighbor.cell[1]
            # Geçerli hücre mi?
            if 0 <= nx < 19 and 0 <= ny < 19:
                # Daha önce ziyaret edildi mi veya stack'te var mı?
                if (cells[nx][ny].walkable and 
                    not any(n.cell == neighbor.cell for n in visited) and 
                    not any(n.cell == neighbor.cell for n in unvisited)):
                    unvisited.append(neighbor)

  
    # Yolu geri izle
    node = goalNode
    while node.pred and node.pred.cell != ghost.cell:
        node = node.pred

    return node.cell, len(visited), len(visited)+len(unvisited)




def BFSWithoutHeuristic(ghost, pac, cells):
    visited = []
    unvisited = deque()  # FIFO için optimize veri yapısı
    unvisited.append(SearchNode(ghost.cell))
    goalNode = SearchNode(pac.cell)

    while unvisited:
        current_node = unvisited.popleft()  # O(1) zaman karmaşıklığı
        
        # Hedef kontrolü doğru yerde
        if current_node.cell == goalNode.cell:
            goalNode = current_node
            break

        visited.append(current_node)
        x, y = current_node.cell[0], current_node.cell[1]
        
        # Komşuları oluştur
        neighbors = [
            SearchNode([x-1, y], current_node),  # left
            SearchNode([x+1, y], current_node),  # right
            SearchNode([x, y-1], current_node),  # up
            SearchNode([x, y+1], current_node)   # down
        ]

        for neighbor in neighbors:
            nx, ny = neighbor.cell[0], neighbor.cell[1]
            
            # Geçerlik kontrolü
            if (0 <= nx < 19 and 0 <= ny < 19 and 
                cells[nx][ny].walkable and 
                not any(n.cell == neighbor.cell for n in visited) and 
                not any(n.cell == neighbor.cell for n in unvisited)):
                
                neighbor.g = current_node.g + 1  # Mesafe güncelleme
                unvisited.append(neighbor)
                #g, başlangıç düğümünden o düğüme kadar olan gerçek mesafeyi temsil eder.
                #Yolun uzunluğunu ölçmek için kullanılır.
                #Bu yüzden her komşu düğüm için g değeri = parent’ın g değeri + 1 olur.


    # Yolu geri izle
    path_node = goalNode
    while path_node.pred and path_node.pred.cell != ghost.cell:
        path_node = path_node.pred

    return path_node.cell, len(visited), len(visited)+len(unvisited)



def init_grid(file):
    bc = Image.open(file)
    pix = bc.load()
    bc.close()

    cols = 19
    rows = 19
    cells = [[GridCell() for j in range(cols)] for i in range(rows)]
    for x in range(19):
        for y in range(19):
            cells[x][y].cell = [x, y]
            cells[x][y].position = [x * 32, y * 32]
            if pix[x * 32, y * 32] == BLACK:
                cells[x][y].walkable = True
                cells[x][y].coin = True
                # walkable olan yerlere coinler yerlestirdik
    cells[8][9].coin = False
    cells[9][9].coin = False
    cells[10][9].coin = False
    cells[9][8].coin = False
    cells[0][7].coin = False
    cells[1][7].coin = False
    cells[2][7].coin = False
    cells[0][11].coin = False
    cells[1][11].coin = False
    cells[2][11].coin = False
    cells[16][7].coin = False
    cells[17][7].coin = False
    cells[18][7].coin = False
    cells[16][11].coin = False
    cells[17][11].coin = False
    cells[18][11].coin = False
    #bunlar coin olmamasi gereken yerler 
    return cells
