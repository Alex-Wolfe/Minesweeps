# Minesweeper Project 
# Authored by Alex Wolfe on 6/18/2022


import pygame
import winsound
import random

def main():
    
    # Define Classes
    class Tile():
        def __init__(self,pos,color,tilesize,display):
            self.covered = True
            self.mine = False
            self.adjacentmines = 0
            self.row = pos[0]
            self.col = pos[1]
            self.p1 = (pos[1]*tilesize, pos[0]*tilesize + headerheight)
            self.p2 = (self.p1[0] + tilesize, self.p1[1] + tilesize)
            self.center = ((self.p1[0]+self.p2[0])/2,(self.p1[1]+self.p2[1])/2)
            self.square = pygame.Rect(self.p1[0],self.p1[1],tilesize,tilesize)
            pygame.draw.rect(display,color,self.square)

        def Dig(self,display):
            self.covered = False
            if (self.row + self.col) % 2:
                color = (150,150,150)
                pygame.draw.rect(display,color,self.square)  
            else:
                color = (200,200,200)
                pygame.draw.rect(display,color,self.square)        
            if not self.mine:
                if self.adjacentmines:
                    number = font.render(str(self.adjacentmines),True,(0,0,0))
                    rect = number.get_rect()
                    rect.center = self.center
                    display.blit(number,rect)
            
            else:
                minesym = font.render('b',True,(0,0,0))
                rect = minesym.get_rect()
                rect.center = self.center
                display.blit(minesym,rect)


    # Define Functions
    def CreateWindow(windowsize,background):
        display = pygame.display.set_mode(windowsize)
        display.fill(background)
        return display

    def CreateTiles(tilesize,boardarray,display):
        tiles = []
        for row in range(boardarray[1]):
            subtiles = []
            for col in range(boardarray[0]):
                if (row+col)%2:
                    tilecolor = (255,0,0)
                else:
                    tilecolor = (0,255,0)
                subtiles.append(Tile([row,col],tilecolor,tilesize,display))
            tiles.append(subtiles)
        return tiles
        
    def DrawHeader(display):
        p1 = (0,0)
        header = pygame.Rect(p1[0],p1[1],windowsize[0],headerheight)
        color = (255,255,0)
        pygame.draw.rect(display,color,header)
    
    def SetBombs(numbombs,tiles):
        while numbombs:
            col = random.randint(0,boardarray[0]-1)
            row = random.randint(0,boardarray[1]-1)
            if tiles[row][col].mine:
                continue
            tiles[row][col].mine = True
            numbombs-=1

    def GetClickCoords(x,y,tilesize):
        col = x//tilesize
        row = (y-headerheight)//tilesize
        return [int(row),int(col)]

    def CalculateTileNumbers(tiles):
        for k in range(len(tiles)):
            for j in range(len(tiles[k])):
                if not tiles[k][j].mine:
                    continue
                if k < boardarray[1]-1:
                    tiles[k+1][j].adjacentmines+=1
                    if j < boardarray[0]-1:
                        tiles[k+1][j+1].adjacentmines+=1
                        tiles[k][j+1].adjacentmines+=1
                    if j > 0:
                        tiles[k+1][j-1].adjacentmines+=1
                        tiles[k][j-1].adjacentmines+=1
                if k > 0:
                    tiles[k-1][j].adjacentmines+=1
                    if j < boardarray[0]-1:
                        tiles[k-1][j+1].adjacentmines+=1
                    if j > 0:
                        tiles[k-1][j-1].adjacentmines+=1



    # Main game setup
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    font = pygame.font.SysFont(None, 48)
    headerheight = 100
    difficulty = 'easy'
    tilesizemap = {'easy':40,'medium':30,'hard':25}
    numbombsmap = {'easy':10,'medium':40,'hard':99}
    numbombs = numbombsmap[difficulty]
    tilesize = tilesizemap[difficulty]
    boardarraymap = {'easy':[10,8],'medium':[18,14],'hard':[24,20]}
    boardarray = boardarraymap[difficulty]
    windowsize = (boardarray[0]*tilesize, boardarray[1]*tilesize + headerheight)
    background = (50,50,225)    #lightblue
    display = CreateWindow(windowsize,background)
    clock = pygame.time.Clock()
    tiles = CreateTiles(tilesize,boardarray,display)
    DrawHeader(display)
    SetBombs(numbombs,tiles)
    CalculateTileNumbers(tiles)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                click = pygame.mouse.get_pos()
                if mouse_presses[0]:
                    [row,col] = GetClickCoords(click[0],click[1],tilesize)
                    tiles[row][col].Dig(display)
                elif mouse_presses[1]:
                    pass
                else:
                    [row,col] = GetClickCoords(click[0],click[1],tilesize)
                    tiles[row][col].Dig(display)


        pygame.display.update()
        clock.tick(60)
        
    




if __name__ == '__main__':
    main()
