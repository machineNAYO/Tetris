import time
import pygame

WIDTH = 10
HEIGHT = 20
# 테트리스는 10*20d
# AND 연산의 결과값이 참이라면 충돌한 것임
# 충돌 시 블럭을 이동시키지 않고 설치 (OR연산)
# 블럭은 x=4번째 칸에서 생성
# 21번째 줄에 블럭이 설치되면 게임오버


class StageManager:
    def __init__(self):
        self.__stage = [0 for i in range (HEIGHT+4)]
        self.__wall = 1 << WIDTH+1
        self.__max = self.__wall-1
    
    def CollideCheck(self, block, pos):     # self, blocktype, cursorpos, return True = collided
        i = 0
        for b in block:
            b << pos[0]
            if b & self.__stage[pos[1] - i] != 0: return True
            if b >= self.__wall: return True
        return False
    
    def PopLine(self):
        for line in range (0, HEIGHT):
            if self.__stage[line] == self.__max: self.__stage[line] = 0
            
        for line in range (0, HEIGHT):
            if self.__stage[line] == 0:
                for sline in range(line, HEIGHT):
                    if self.__stage[sline] != 0:
                        self.__stage[line] = self.__stage[sline]
                        break
        
            
            

class Cursor:
    __BLOCK_TYPE = (  # BLOCK_TYPE[type][0, 1][numofvariations, rotate]
    (2, ((1, 1, 1, 1) , (0b1111) ) ),    # Straight
    (1, (0b11, 0b11) ),    # Square
    (4, ((0b11, 1, 1), (1, 0b111), (0b10, 0b10, 0b11), (0b111, 0b100) ) ),    # L
    (4, ((0b11, 0b10, 0b10), (0b111, 1), (1, 1, 0b11), (0b100, 0b111) ) ),    # Flipped L
    (4, ((0b10, 0b11, 0b10), (0b111, 0b10), (1, 0b11, 1), (0b10, 0b111) ) ),  # T
    (2, ((0b11, 0b10, 1), (0b110, 0b11) ) ),  # N
    (2, ((0b10, 0b11, 1), (0b11, 0b110) ) )   # Flipped N
    )
    
    __pos = [0, 0]  #[x, y]
    __type = 0  # str, squ, L, Lf, T, N, Nf (0~6)
    __rotate = 0

    def GetCursorPos(self):
        return self.__pos
    
    def SetType(self, num):
        self.__type = num
        
    def GetBlock(self):
        return self.__BLOCK_TYPE[self.__type][self.__rotate]
    
    def RotateBlock(self, dir):     # -1 = left, 1 = right
        if self.__type == 1: return
        
        self.__rotate += dir
        if(self.__rotate == -1): self.__rotate = self.__BLOCK_TYPE[self.__type][0]
        elif self.__rotate == self.__BLOCK_TYPE[self.__type][0]: self.__rotate = 0
        
    def MoveBlock(self, dir):   # -1 = left, 0 = down, 1 = right
        if dir == 0: self.__pos[1] -= 1
        elif dir == -1: self.__pos[0] -= 1
        else: self.__pos[0] += 1
        




BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
BLUE  = [0, 0, 255]
GREEN = [0, 255, 0]
RED   = [255, 0, 0]

TICK = 30
SCREEN_SIZE = [800, 910]

STAGE_WIDTH = 425
BLOCK_SIZE = STAGE_WIDTH/10
STAGE_EDGE = 3

STAGE_X = 30
STAGE_Y = 30

class Canvas:
    def __init__(self):
        
        self.__blockcanvas = [[BLACK for row in range(0,WIDTH)] for col in range(0,HEIGHT)]
        self.__screen = pygame.display.set_mode(SCREEN_SIZE)
        self.__screen.fill(BLACK)
        pygame.draw.rect(self.__screen, WHITE, [STAGE_X - STAGE_EDGE, STAGE_Y - STAGE_EDGE, STAGE_WIDTH + STAGE_EDGE*2, (STAGE_WIDTH + STAGE_EDGE) *2], STAGE_EDGE)


class GameManager:
    def __init__(self):

        pygame.init()
        
        self.__stm = StageManager()
        self.__csr = Cursor()
        self.__tcsr = Cursor()
        self.__nva = Canvas()
        
        self.__dealy = 5
   
        
        self.__clock = pygame.time.Clock()

        pygame.display.set_caption("TISISTTIS")
        
        
        
    def Start(self):
        done = False

        while not done:
            
            self.__clock.tick(TICK)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                print(event)      
   
            pygame.display.update()
            
            
        
        
        
gameManager = GameManager()        
gameManager.Start()
    
    
    
    