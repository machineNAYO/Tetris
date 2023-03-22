WIDTH = 10
HEIGHT = 20
# 테트리스는 10*20
# AND 연산의 결과값이 참이라면 충돌한 것임
# 충돌 시 블럭을 이동시키지 않고 설치 (OR연산)
# 블럭은 x=4번째 칸에서 생성
# 21번째 줄에 블럭이 설치되면 게임오버


class StageManager:
    def __init__(self):
        self.__stage = [0 for i in range (HEIGHT+4)]
        self.__max = 1 << WIDTH+1
    
    def CollideCheck(self, block, pos):     # self, blocktype, cursorpos, True = collided
        i = 0
        for b in block:
            b << pos[0]
            if b & self.__stage[pos[1] - i] != 0: return True
            if b >= self.__max: return True
        return False
    
    
        
            
            

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
        pass
        


class GameManager:
    def __init__(self):
        self.__sm = StageManager()
        self.__cs = Cursor()
        self.__tcs = Cursor()
    
    