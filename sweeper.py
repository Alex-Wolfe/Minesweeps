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
            self.flagged = False
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
                    adjacent = getAdjacent(self,tiles)
                    for tile in adjacent:
                        if tile.covered:
                            tile.Dig(display)
            else:
                rect = minemap[difficulty].get_rect()
                rect.center = self.center
                display.blit(minemap[difficulty],rect)

        def Flag(self,display):
            if self.flagged:
                self.flagged = False
            else:
                self.flagged = True
            rect = flagmap[difficulty].get_rect()
            rect.center = self.center
            display.blit(flagmap[difficulty],rect)

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
        
    def GetClickCoords(x,y,tilesize):
        col = x//tilesize
        row = (y-headerheight)//tilesize
        return [int(row),int(col)]
    
    def SetBombs(numbombs,tiles,selected):
        while numbombs:
            col = random.randint(0,boardarray[0]-1)
            row = random.randint(0,boardarray[1]-1)
            if tiles[row][col].mine or tiles[row][col] == selected or tiles[row][col] in getAdjacent(selected,tiles):
                continue
            tiles[row][col].mine = True
            numbombs-=1

    # Returns list of tiles that are adjacent to the selected tile
    def getAdjacent(selected,tiles):
        row = selected.row
        col = selected.col
        adjacent = []
        if row < boardarray[1]-1:
            adjacent.append(tiles[row+1][col])
            if col < boardarray[0]-1:
                adjacent.append(tiles[row+1][col+1])
            if col:
                adjacent.append(tiles[row+1][col-1])
        if row:
            adjacent.append(tiles[row-1][col])
            if col < boardarray[0]-1:
                adjacent.append(tiles[row-1][col+1])
            if col:
                adjacent.append(tiles[row-1][col-1])
        if col < boardarray[0]-1:
            adjacent.append(tiles[row][col+1])
        if col:
            adjacent.append(tiles[row][col-1])
        return adjacent

    def CalculateTileNumbers(tiles):
        for k in range(len(tiles)):
            for j in range(len(tiles[k])):
                if not tiles[k][j].mine:
                    continue
                adjacent = getAdjacent(tiles[k][j],tiles)
                for tile in adjacent:
                    tile.adjacentmines+=1


    # Main game setup
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    mine_easy = pygame.image.load('mine_easy.png')
    mine_med = pygame.image.load('mine_medium.png')
    mine_hard = pygame.image.load('mine_hard.png')
    flag_easy = pygame.image.load('flag_easy.png')
    flag_med = pygame.image.load('flag_med.png')
    flag_hard = pygame.image.load('flag_hard.png')
    headerheight = 100
    difficulty = 'easy'
    fontmap = {'easy':48,'medium':38,'hard':30}
    minemap = {'easy':mine_easy,'medium':mine_med,'hard':mine_hard}
    flagmap = {'easy':flag_easy,'medium':flag_med,'hard':flag_hard}
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
    font = pygame.font.SysFont(None, fontmap[difficulty])

    # First while loop is for first click only, after which bombs are set and main game loop is entered
    breakflag = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                click = pygame.mouse.get_pos()
                if mouse_presses[0]:
                    [row,col] = GetClickCoords(click[0],click[1],tilesize)
                    selected = tiles[row][col]
                    SetBombs(numbombs,tiles,selected)
                    CalculateTileNumbers(tiles)
                    selected.Dig(display)
                    breakflag = True
                    break
                elif mouse_presses[1]:
                    pass
                else:
                    [row,col] = GetClickCoords(click[0],click[1],tilesize)
                    selected = tiles[row][col]
                    SetBombs(numbombs,tiles,selected)
                    CalculateTileNumbers(tiles)
                    selected.Dig(display)
                    breakflag = True
                    break
        if breakflag:
            break
        pygame.display.update()
        clock.tick(60)
        
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                click = pygame.mouse.get_pos()
                if mouse_presses[0]:
                    [row,col] = GetClickCoords(click[0],click[1],tilesize)
                    if not tiles[row][col].flagged:
                        tiles[row][col].Dig(display)
                elif mouse_presses[1]:
                    pass
                else:
                    [row,col] = GetClickCoords(click[0],click[1],tilesize)
                    if tiles[row][col].covered:
                        tiles[row][col].Flag(display)
        pygame.display.update()
        clock.tick(60)
        
    


if __name__ == '__main__':
    main()
