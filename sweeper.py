# Minesweeper Project 
# Authored by Alex Wolfe on 6/18/2022


import pygame
import winsound
import random

def main():
    
    # Define Classes
    class Tile():
        def __init__(self,pos,color,tilesize,display):
            self.color = color
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
            pygame.draw.rect(display,self.color,self.square)

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

        def Flag(self,display,flags):
            if self.flagged:
                self.flagged = False
                pygame.draw.rect(display,self.color,self.square)
                flags+=1
            elif flags:
                self.flagged = True
                rect = flagmap[difficulty].get_rect()
                rect.center = self.center
                display.blit(flagmap[difficulty],rect)
                flags-=1
            return flags

        def QuickDig(self,display):
            adjacent = getAdjacent(self,tiles)
            for tile in adjacent:
                if not tile.flagged and tile.covered:
                    tile.Dig(display)


    # Define Functions
    def CreateWindow(windowsize):
        display = pygame.display.set_mode(windowsize)
        return display

    def CreateTiles(tilesize,boardarray,display):
        tiles = []
        for row in range(boardarray[1]):
            subtiles = []
            for col in range(boardarray[0]):
                if (row+col)%2:
                    tilecolor = (90,204,20)
                else:
                    tilecolor = (168,218,102)
                subtiles.append(Tile([row,col],tilecolor,tilesize,display))
            tiles.append(subtiles)
        return tiles

    def UpdateHeader(display):
        header = pygame.Rect(0,0,windowsize[0],headerheight)
        color = (76,153,0)
        pygame.draw.rect(display,color,header)
        rect = flag_header.get_rect()
        rect.center = (windowsize[0]/3,headerheight/2)
        display.blit(flag_header,rect)
        numflags = headerfont.render(str(flags),True,(0,0,0))
        flagrect = numflags.get_rect()
        flagrect.center = (rect.center[0]+55,rect.center[1])
        display.blit(numflags,flagrect)
        clockrect = clock_img.get_rect()
        clockrect.center = (2*windowsize[0]/3, headerheight/2)
        display.blit(clock_img,clockrect)
        timedis = headerfont.render(str(time),True,(0,0,0))
        timerect = timedis.get_rect()
        timerect.center = (clockrect.center[0]+55,clockrect.center[1])
        display.blit(timedis,timerect)
        
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

    def CheckforWin(tiles):
        for set in tiles:
            for tile in set:
                if tile.covered and not tile.mine:
                    return False
        return True

    def GameOver(display):
        print('kaboom')

    def GameWin(display):
        print('pog')

    def StartGame():
        difficulty = 'easy'
        fontmap = {'easy':48,'medium':38,'hard':30}
        minemap = {'easy':mine_easy,'medium':mine_med,'hard':mine_hard}
        flagmap = {'easy':flag_easy,'medium':flag_med,'hard':flag_hard}
        tilesizemap = {'easy':40,'medium':30,'hard':25} 
        numminesmap = {'easy':10,'medium':40,'hard':99}
        boardarraymap = {'easy':[10,8],'medium':[18,14],'hard':[24,20]}
        nummines = numminesmap[difficulty]
        tilesize = tilesizemap[difficulty]
        boardarray = boardarraymap[difficulty]
        windowsize = (boardarray[0]*tilesize, boardarray[1]*tilesize + headerheight)
        display = CreateWindow(windowsize)
        clock = pygame.time.Clock()
        tiles = CreateTiles(tilesize,boardarray,display)
        flags = nummines
        font = pygame.font.SysFont(None, fontmap[difficulty])
        subtime = 0
        time = 0
        return [tiles,display,clock,minemap,flagmap,flags,font,subtime,time,difficulty,windowsize,boardarray,tilesize,nummines,True]

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
    flag_header = pygame.image.load('flag_header.png')
    clock_img = pygame.image.load('clock.png')
    headerfont = pygame.font.SysFont(None,50)
    headerheight = 70
    [tiles,display,clock,minemap,flagmap,flags,font,subtime,time,difficulty,windowsize,boardarray,tilesize,nummines,first]= StartGame()
    UpdateHeader(display)
    # Main game loop
    while True:
        while first:
            # First while loop is for first click only, after which bombs are set and main game loop is entered
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    click = pygame.mouse.get_pos()
                    if mouse_presses[0]:
                        [row,col] = GetClickCoords(click[0],click[1],tilesize)
                        selected = tiles[row][col]
                        SetBombs(nummines,tiles,selected)
                        CalculateTileNumbers(tiles)
                        selected.Dig(display)
                        first = False
                    elif mouse_presses[1]:
                        pass
                    else:
                        [row,col] = GetClickCoords(click[0],click[1],tilesize)
                        selected = tiles[row][col]
                        SetBombs(nummines,tiles,selected)
                        CalculateTileNumbers(tiles)
                        selected.Dig(display)
                        first = False
            pygame.display.update()
            clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                click = pygame.mouse.get_pos()
                if mouse_presses[0]:
                    [row,col] = GetClickCoords(click[0],click[1],tilesize)
                    if not tiles[row][col].flagged:
                        if tiles[row][col].mine:
                            GameOver(display)
                        else:
                            tiles[row][col].Dig(display)
                elif mouse_presses[1]:
                    [row,col] = GetClickCoords(click[0],click[1],tilesize)
                    adjacenttiles = getAdjacent(tiles[row][col],tiles)
                    numadjflags = 0
                    if not tiles[row][col].covered:
                        for tile in adjacenttiles:
                            if tile.flagged:
                                numadjflags+=1
                        if numadjflags == tiles[row][col].adjacentmines:
                            tiles[row][col].QuickDig(display)
                else:
                    [row,col] = GetClickCoords(click[0],click[1],tilesize)
                    if tiles[row][col].covered:
                        flags = tiles[row][col].Flag(display,flags)
        UpdateHeader(display)
        if CheckforWin(tiles):
            GameWin(display)
        pygame.display.update()
        clock.tick(60)
        subtime+=1
        if subtime == 60:
            subtime = 0
            time+=1




if __name__ == '__main__':
    main()
