import time
import pygame
import random

WIDTH = 10
HEIGHT = 20
# 테트리스는 10*20
# AND 연산의 결과값이 참이라면 충돌한 것임 test
# 충돌 시 블럭을 이동시키지 않고 설치 (OR연산)
# 블럭은 x=4번째 칸에서 생성
# 21번째 줄에 블럭이 설치되면 게임오버

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
BLUE  = [0, 0, 255]
GREEN = [0, 255, 0]
RED   = [255, 0, 0]
PURPLE = [255, 0, 255]
YELLOW = [255, 255, 0]
AQUA = [0, 255, 255]
BROWN = [150, 100, 50]

TICK = 17
SCREEN_SIZE = [800, 910]

STAGE_WIDTH = 425
BLOCK_SIZE = STAGE_WIDTH/10
STAGE_EDGE = 3

STAGE_X = 30
STAGE_Y = 30

class StageManager:
    def __init__(self):
        self.__stage = [0 for i in range (HEIGHT+4)]
        self.__wall = 1 << WIDTH
        self.__max = self.__wall-1
    
    def CollideCheck(self, block, y, temp):     # self, blocktype, cursorpos, return True = collided
        if y < 0: return True
        if y > 20: return False
        i = 0
        
        if type(block) is list:     
            for b in block:          
                if y < i: return True
                if b & self.__stage[y - i] != 0: return True
                if b >= self.__wall: return True
                i += 1
            return False
            
        else:
            if block & self.__stage[y] != 0: return True
            if block & self.__stage[y] != 0: return True  
            if block >= self.__wall: return True
        return False
    
    def PopCheck(self):
        for line in range (0, HEIGHT):
            if self.__stage[line] == self.__max: 
                return True
        return False
    
    def PopLine(self):
        blank = [] # y, chain
        for line in range (0, HEIGHT):
            if self.__stage[line] == self.__max: 
                self.__stage[line] = 0
                if (line !=  0) and (self.__stage[line-1] == 0):
                    blank[-1][1] += 1
                else: blank.append([line,1])

        i = blank[0][1]
        for info in blank:
            for s in range(info[0], HEIGHT-1-i):
                self.__stage[s] = self.__stage[s + i]
            
            i += blank[-1][1]    
              
        for s in range(HEIGHT - 1 - i + blank[-1][0], HEIGHT):
            self.__stage[s] = 0
                    
        return blank

    
    def PutBlock(self, block, y, temp):
        isGameOver = False
        
        
        i = 0
        if type(block) is not int:
            for b in block:          
                self.__stage[y-i] |= b
                i += 1
        
        else:
            self.__stage[y] |= block
        
        self.PrintStage()
        
        for i in range(HEIGHT, HEIGHT + 4):
            if self.__stage[i] != 0: isGameOver = True   
        return isGameOver
    
    def PrintStage(self):
        print("==============================================")
        for i in range(0,HEIGHT):
            line = str(bin(self.__stage[HEIGHT-i-1]))[2:]
            for i in range(WIDTH-len(line)):
                line = "0" + line
            print(line)
        print("==============================================")
            
STARTPOS = (4, 23)

class Cursor:
    def __init__(self):
    
        self.__BLOCK_TYPE = (  # BLOCK_TYPE[type][0 = numofvariations , 1 = variationlist, 2 = color][rotatenum]
        (2, ((1, 1, 1, 1) , (0b1111) ), RED ),    # Straight
        (1, (0b11, 0b11), GREEN ),    # Square
        (4, ((0b11, 1, 1), (1, 0b111), (0b10, 0b10, 0b11), (0b111, 0b100) ), BLUE ),    # L
        (4, ((0b11, 0b10, 0b10), (0b111, 1), (1, 1, 0b11), (0b100, 0b111) ), PURPLE ),    # Flipped L
        (4, ((0b10, 0b11, 0b10), (0b111, 0b10), (1, 0b11, 1), (0b10, 0b111) ), YELLOW ),  # T
        (2, ((1, 0b11, 0b10), (0b110, 0b11) ), AQUA ),  # N
        (2, ((0b10, 0b11, 1), (0b11, 0b110) ), BROWN )   # Flipped N
        )
    

        self.__pos = [0, 0]
        self.__type = 0  # str, squ, L, Lf, T, N, Nf (0~6)
        self.__rotate = 0

        self.__used = 0b0000000
        self.__check = 0b1111111
        self.__picked = False
        self.__rand = 0

    def SetType(self, num):
        self.__type = num
        
    def GetBlock(self):
        temB = []
        
        if self.__type == 0 and self.__rotate == 1:
            temB = self.__BLOCK_TYPE[0][1][1] << self.__pos[0]
            return temB, self.__pos[1], self.__BLOCK_TYPE[0][2]
        
        elif self.__type == 1:
            temB = [0, 0]
            i = 0
            for b in self.__BLOCK_TYPE[1][1]:
                temB[i] = b << self.__pos[0]
                i += 1
            return temB, self.__pos[1], self.__BLOCK_TYPE[1][2]
        
        else:
            temB = [0 for s in range (len(self.__BLOCK_TYPE[self.__type][1][self.__rotate]))]
            i = 0
            for b in self.__BLOCK_TYPE[self.__type][1][self.__rotate]:
                temB[i] = b << self.__pos[0]
                i += 1
            return temB, self.__pos[1], self.__BLOCK_TYPE[self.__type][2]

    def GetX(self):
        return self.__pos[0]
    
    def GetRotate(self):
        return self.__rotate
    
    def RotateBlock(self, dir):     # -1 = left, 1 = right
        if self.__type == 1: return

        self.__rotate += dir
        
        
        if(self.__rotate == -1): self.__rotate = self.__BLOCK_TYPE[self.__type][0] - 1
        elif self.__rotate == self.__BLOCK_TYPE[self.__type][0]: self.__rotate = 0

        
    def MoveBlock(self, dir):   # -1 = left, 0 = down, 1 = right, 2 = up
        if dir == 0: self.__pos[1] -= 1
        elif dir == -1: self.__pos[0] += 1
        elif dir == 1: self.__pos[0] -= 1
        else: self.__pos[1] += 1
    
    def NewBlock(self):
        
        if self.__used == self.__check: self.__used = 0
        while not self.__picked:
            self.__rand = random.randrange(0, 7)
            if 1<<self.__rand&self.__used == 0:
                self.__used |= 1<<self.__rand
                self.__picked = True

        self.__pos = [STARTPOS[0], STARTPOS[1]]
        self.__rotate = 0
        self.__type = self.__rand #random.randrange(0,7)
        self.__picked = False






class Canvas:
    def __init__(self):
        
        self.__canvas = [[BLACK for col in range(0,HEIGHT)] for row in range(0,WIDTH)]
        self.__screen = pygame.display.set_mode(SCREEN_SIZE)
        self.__screen.fill(BLACK)
        pygame.draw.rect(self.__screen, WHITE, [STAGE_X - STAGE_EDGE, STAGE_Y - STAGE_EDGE, STAGE_WIDTH + STAGE_EDGE*2, (STAGE_WIDTH + STAGE_EDGE) *2], STAGE_EDGE)

    def Rend(self, block, y, color):
        pygame.draw.rect(self.__screen, BLACK, [STAGE_X, STAGE_Y, STAGE_WIDTH, STAGE_WIDTH*2])
        tx = 0
        ty = STAGE_Y + BLOCK_SIZE * (HEIGHT-y-1)
        
        if type(block) is not int:
            for b in block:
                
                i = 0
                tx = STAGE_X + BLOCK_SIZE * (WIDTH-1)
                while b != 0:
                    if b&1 == 1 and y < 20:
                        pygame.draw.rect(self.__screen, color, [tx, ty, BLOCK_SIZE, BLOCK_SIZE])                   
                    b >>= 1
                    tx -= BLOCK_SIZE
                    i += 1
                ty += BLOCK_SIZE
                y -= 1
            
        else:
            tx = STAGE_X + BLOCK_SIZE * (WIDTH-1)
            while block != 0:
                if block&1 == 1 and y < 20:
                    pygame.draw.rect(self.__screen, color, [tx, ty, BLOCK_SIZE, BLOCK_SIZE])                   
                block >>= 1
                tx -= BLOCK_SIZE
                    
        for i in range(0, HEIGHT):
            for s in range(0, WIDTH):
                if self.__canvas[s][i] != BLACK:
                    pygame.draw.rect(self.__screen, self.__canvas[s][i], [STAGE_X + BLOCK_SIZE * (WIDTH-s-1), STAGE_Y + BLOCK_SIZE * (HEIGHT-i-1), BLOCK_SIZE, BLOCK_SIZE])

        pygame.draw.rect(self.__screen, WHITE, [STAGE_X - STAGE_EDGE, STAGE_Y - STAGE_EDGE, STAGE_WIDTH + STAGE_EDGE*2, (STAGE_WIDTH + STAGE_EDGE) *2], STAGE_EDGE)
        pygame.display.update()
        
    def AddBlock(self, block, ty, color):
        tx = 0
        

        
        if type(block) is not int:
            for b in block:
                tx = 0
                while b != 0:
                    if b&1 == 1:
                        
                        self.__canvas[tx][ty] = color                   
                    b >>= 1
                    tx += 1
                ty -= 1
        else:
            tx = 0
            while block != 0:
                if block&1 == 1:
                        
                    self.__canvas[tx][ty] = color                   
                block >>= 1
                tx += 1
    
    def FallSet(self, blank): 
        i = blank[0][1]
        for info in blank:
            for s in range(info[0], HEIGHT-1-i):
                for row in range(0,WIDTH):
                    self.__canvas[row][s] = self.__canvas[row][s + i]
                    
            
            i += blank[-1][1] 
            
        for i in range(HEIGHT - 1 - i, HEIGHT):
                for row in range(0,WIDTH):
                    self.__canvas[row][i] = BLACK

class GameManager:
    def __init__(self):

        pygame.init()
        
        self.__stm = StageManager()
        self.__csr = Cursor()
        self.__nva = Canvas()
        
        self.__dealy = 1000    #ms
        self.__fallMax = 5
        
        self.__clock = pygame.time.Clock()

        pygame.display.set_caption("TISISTTIS")
        
        
        
    def Start(self):
        done = False
        fallcount = 0
        
        self.__csr.NewBlock()
        
        while not done:
            
            self.__clock.tick(TICK)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.__csr.MoveBlock(-1)
                        if not self.__stm.CollideCheck(*self.__csr.GetBlock()):
                            pass
                            
                        else: 
                            self.__csr.MoveBlock(1)
                    
                    elif event.key == pygame.K_RIGHT:
                        self.__csr.MoveBlock(1)
                        if self.__csr.GetX() > -1 and (not self.__stm.CollideCheck(*self.__csr.GetBlock())):
                            pass
                            
                        else: 
                            self.__csr.MoveBlock(-1)
                            
                            
                    elif event.key == pygame.K_UP:
                        self.__csr.RotateBlock(1)
                        if not self.__stm.CollideCheck(*self.__csr.GetBlock()):
                            pass 
                        
                        else:
                            self.__csr.RotateBlock(-1)
                                                                  
                    
                    elif event.key == pygame.K_SPACE:
                        while not self.__stm.CollideCheck(*self.__csr.GetBlock()):
                            self.__csr.MoveBlock(0)
                        self.__csr.MoveBlock(2)
                        
                        if self.__stm.PutBlock(*self.__csr.GetBlock()):
                            print("GAMEOVER")
                            return 
                        self.__nva.AddBlock(*self.__csr.GetBlock())    
                        
                        self.__csr.NewBlock()

                        self.PopBlock()
                        fallcount = 0; 
                
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]: fallcount = self.__fallMax
                    
                        
                        
            
            if fallcount == self.__fallMax: 
                
                fallcount = 0
                self.__csr.MoveBlock(0)
                
                if not self.__stm.CollideCheck(*self.__csr.GetBlock()):
                    pass
                else:                     
                    self.__csr.MoveBlock(2)
                    
                    if self.__stm.PutBlock(*self.__csr.GetBlock()) == True:
                        print("GAMEOVER")
                        return  
                    self.__nva.AddBlock(*self.__csr.GetBlock())
                    
                    self.__csr.NewBlock()
                    
                    self.PopBlock()
                    
                    
            else: fallcount += 1
                  
            self.__nva.Rend(*self.__csr.GetBlock())   
                

    def PopBlock(self):
        if self.__stm.PopCheck() == True:
            self.__nva.FallSet(self.__stm.PopLine())
            #self.__stm.PrintStage()
            

        
gameManager = GameManager()        
gameManager.Start()
    
    
    
    