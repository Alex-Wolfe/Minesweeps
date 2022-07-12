# Minesweeper Project 
# Authored by Alex Wolfe on 6/18/2022
# Contains several features like in game difficulty changing, quick digging and more

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

        # Method which processes a tile being dug. Only allows tiles that are still covered to be dug
        #   Only plays the dig sound once for each click. If a tile has no adjacent bombs, dig all adjacent tiles as well
        #   Returns True if a bomb was dug, signaling a loss
        def Dig(self,display,token):
            if not self.covered:
                return False
            if token:
                num = random.randint(0,2)
                if volume:
                    winsound.PlaySound(digmap[num],winsound.SND_ASYNC)
                token = 0
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
                            tile.Dig(display,0)
            else:
                rect = minemap[difficulty].get_rect()
                rect.center = self.center
                display.blit(minemap[difficulty],rect)
                return True
            return False

        # Method for flagging tiles. Flagged tiles can't be dug. If tile is already flagged, remove the flag.
        #   The number of flags that can be placed is the number of bombs on the board
        def Flag(self,display,flags):
            if self.flagged:
                if volume:
                    winsound.PlaySound('pop.wav',winsound.SND_ASYNC)
                self.flagged = False
                pygame.draw.rect(display,self.color,self.square)
                flags+=1
            elif flags:
                if volume:
                    winsound.PlaySound('flag.wav',winsound.SND_ASYNC)
                self.flagged = True
                rect = flagmap[difficulty].get_rect()
                rect.center = self.center
                display.blit(flagmap[difficulty],rect)
                flags-=1
            return flags

        # Method for middle clicking tiles, where is the tile has the same amount of adjacent flagged tiles as it does adjacent mines,
        # middle clicking will dig all the remaining adjacent tiles. This is a quicker way to dig when you have 'cleared' a tile by 
        # completely flagging it
        def QuickDig(self,display):
            adjacent = getAdjacent(self,tiles)
            for tile in adjacent:
                if not tile.flagged and tile.covered:
                    lost = tile.Dig(display,1)
                    if lost:
                        return True
            return False


    # Define Functions

    # Creates the game window and returns the object
    def CreateWindow(windowsize):
        display = pygame.display.set_mode(windowsize)
        return display

    # Creates the 2-D array of tiles. Alternates the color of tiles in a checkerboard pattern. 
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

    # Every tick through the loop, this function is called to update the game header which
    #  includes the time, number of flags, difficulty, and images
    def UpdateHeader(display,difficulty):
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
        speakerrect = speaker_img.get_rect()
        speakerrect.center = (windowsize[0]-30, headerheight/2)
        display.blit(speaker_img,speakerrect)
        timedis = headerfont.render(str(time),True,(0,0,0))
        timerect = timedis.get_rect()
        timerect.center = (clockrect.center[0]+55,clockrect.center[1])
        display.blit(timedis,timerect)
        dif = diffont.render(difficulty,True,(0,0,0))
        difrect = dif.get_rect()
        difrect.left = 25
        difrect.top = 25
        display.blit(dif,difrect)
        return difrect, speakerrect
        
    # Takes in x and y coordinates of a mouse click and returns the row and col of the tile that was clicked on the 2-D board
    def GetClickCoords(x,y,tilesize):
        col = x//tilesize
        row = (y-headerheight)//tilesize
        return [int(row),int(col)]
    
    # Takes a 2-D array of tiles and randomly fills the board with the number of the mines that the current
    # difficulty calls for.
    # This method is called after the first click is made, so the board is filled with mines so that the first clicked tile
    # is not a mine and all the adjacent tiles to the first clicked tile are not mines
    def SetBombs(numbombs,tiles,selected):
        adjacents = getAdjacent(selected,tiles)
        while numbombs:
            col = random.randint(0,boardarray[0]-1)
            row = random.randint(0,boardarray[1]-1)
            if tiles[row][col].mine or tiles[row][col] == selected or tiles[row][col] in adjacents:
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

    # This function is called just after the mines are set on the board. This function calculates the number to be displayed
    # on each tile, which represents the number of adjacent bombs to that tile
    def CalculateTileNumbers(tiles):
        for k in range(len(tiles)):
            for j in range(len(tiles[k])):
                if not tiles[k][j].mine:
                    continue
                adjacent = getAdjacent(tiles[k][j],tiles)
                for tile in adjacent:
                    tile.adjacentmines+=1

    # This function checks to see if the game has been won, called every tick through the game loop. Returns True is game is won
    def CheckforWin(tiles):
        for set in tiles:
            for tile in set:
                if tile.covered and not tile.mine:
                    return False
        return True

    # This function is called when a mine has been dug and the game is lost. Creates screen which shows record time and prompts
    # player to play again
    def GameOver(display):
        if volume:
            winsound.PlaySound('kaboom.wav',winsound.SND_ASYNC)
        for set in tiles:
            for tile in set:
                if tile.mine:
                    tile.Dig(display,0)
        bg = pygame.Rect(windowsize[0]/5,windowsize[1]/5,3*windowsize[0]/5,3*windowsize[1]/5)
        color = (76,153,0)
        pygame.draw.rect(display,color,bg)
        clockrect = clock_img.get_rect()
        clockrect.center = (bg.topleft[0]+50,bg.topleft[1]+30)
        display.blit(clock_img,clockrect)
        trophyrect = trophy.get_rect()
        trophyrect.center = (bg.topright[0]-50,bg.topright[1]+30)
        display.blit(trophy,trophyrect)
        time = headerfont.render('--',True,(0,0,0))
        timerect = time.get_rect()
        timerect.center = (clockrect.center[0],clockrect.center[1]+50)
        display.blit(time,timerect)
        line = ReadRecord()
        record = headerfont.render(line,True,(0,0,0))
        recordrect = record.get_rect()
        recordrect.center = (trophyrect.center[0],trophyrect.center[1]+50)
        display.blit(record,recordrect)
        restartrect = restart.get_rect()
        restartrect.center = (bg.center[0],bg.center[1]+windowsize[1]/6)
        display.blit(restart,restartrect)
        pygame.display.update()
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    click = pygame.mouse.get_pos()
                    if mouse_presses[0]:
                        if click[0]<restartrect.right and click[0]>restartrect.left and click[1]<restartrect.bottom and click[1]>restartrect.top:
                            wait = False
                    elif mouse_presses[1]:
                        pass
                    else:
                        pass

    # This function is called when the game has been won. Shows time acheived compared to record time. If record time has been beat, it 
    # updates the record file to reflect that change. Prompts user to play again
    def GameWin(display,time):
        bg = pygame.Rect(windowsize[0]/5,windowsize[1]/5,3*windowsize[0]/5,3*windowsize[1]/5)
        color = (76,153,0)
        pygame.draw.rect(display,color,bg)
        clockrect = clock_img.get_rect()
        clockrect.center = (bg.topleft[0]+50,bg.topleft[1]+30)
        display.blit(clock_img,clockrect)
        trophyrect = trophy.get_rect()
        trophyrect.center = (bg.topright[0]-50,bg.topright[1]+30)
        display.blit(trophy,trophyrect)
        timedis = headerfont.render(str(time),True,(0,0,0))
        timerect = timedis.get_rect()
        timerect.center = (clockrect.center[0],clockrect.center[1]+50)
        display.blit(timedis,timerect)
        line = ReadRecord()
        if time < int(line):
            WriteRecord(time)
            if volume:
                winsound.PlaySound('newrecord.wav',winsound.SND_ASYNC)
        else:
            if volume:
                winsound.PlaySound('win.wav',winsound.SND_ASYNC)
        line = ReadRecord()
        record = headerfont.render(line,True,(0,0,0))
        recordrect = record.get_rect()
        recordrect.center = (trophyrect.center[0],trophyrect.center[1]+50)
        display.blit(record,recordrect)
        restartrect = restart.get_rect()
        restartrect.center = (bg.center[0],bg.center[1]+windowsize[1]/6)
        display.blit(restart,restartrect)
        pygame.display.update()
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    click = pygame.mouse.get_pos()
                    if mouse_presses[0]:
                        if click[0]<restartrect.right and click[0]>restartrect.left and click[1]<restartrect.bottom and click[1]>restartrect.top:
                            wait = False
                    elif mouse_presses[1]:
                        pass
                    else:
                        pass
    
    # Reads the data from the record file, and returns the record time for the current difficulty only
    def ReadRecord():
        recordfile = open('record.txt')
        lines = recordfile.readlines()
        line = lines[recordline]
        line = line.replace('\n','')
        recordfile.close()
        return line

    # This function called if record time was beaten. Updates the record file with the new time
    def WriteRecord(time):
        recordfile = open('record.txt','r+')
        data = recordfile.readlines()
        data[recordline] = str(time) + '\n'
        recordfile.truncate(0)
        recordfile.seek(0)
        recordfile.writelines(data)
        recordfile.close()
    
    # This function called when the program first starts, resets the records
    def InitializeRecord():
        recordfile = open('record.txt','w')
        data = ['999\n','999\n','999']
        recordfile.seek(0)
        recordfile.writelines(data)
        recordfile.close()

    # This function used to reset game in case of loss, win, or difficulty change
    def StartGame(difficulty):
        fontmap = {'easy':48,'med':38,'hard':30,'extreme':30}
        minemap = {'easy':mine_easy,'med':mine_med,'hard':mine_hard,'extreme':mine_hard}
        flagmap = {'easy':flag_easy,'med':flag_med,'hard':flag_hard,'extreme':flag_hard}
        tilesizemap = {'easy':40,'med':30,'hard':25,'extreme':25} 
        numminesmap = {'easy':10,'med':40,'hard':99,'extreme':266}
        boardarraymap = {'easy':[10,8],'med':[18,14],'hard':[24,20],'extreme':[60,28]}
        recordmap = {'easy':0,'med':1,'hard':2,'extreme':3}
        recordline = recordmap[difficulty]
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
        return [tiles,display,clock,minemap,flagmap,flags,font,subtime,time,difficulty,windowsize,boardarray,tilesize,nummines,recordline,True]



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
    speaker_on = pygame.image.load('speaker.png')
    speaker_off = pygame.image.load('speaker_off.png')
    speaker_img = speaker_on
    trophy = pygame.image.load('trophy.png')
    restart = pygame.image.load('try_again.png')
    headerfont = pygame.font.SysFont(None,50)
    diffont = pygame.font.SysFont(None,30)
    headerheight = 70
    digmap = {0:'dig_low.wav',1:'dig_mid.wav',2:'dig_hi.wav'}
    difficultymap = {0:'easy',1:'med',2:'hard',3:'extreme'}
    difpointer = 0
    difficulty = difficultymap[difpointer]
    [tiles,display,clock,minemap,flagmap,flags,font,subtime,time,difficulty,windowsize,boardarray,tilesize,nummines,recordline,first] = StartGame(difficulty)
    difrect,speakerrect = UpdateHeader(display,difficulty)
    volume = True
    # InitializeRecord()

    # Main game loop
    while True:
        UpdateHeader(display,difficulty)
        while first:
            UpdateHeader(display,difficulty)
            # First while loop is for first click only, after which bombs are set and main game loop is entered
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    click = pygame.mouse.get_pos()
                    if difrect.collidepoint(click):
                        difpointer = (difpointer + 1) % 4
                        [tiles,display,clock,minemap,flagmap,flags,font,subtime,time,difficulty,windowsize,boardarray,tilesize,nummines,recordline,first] = StartGame(difficultymap[difpointer])
                        difrect = UpdateHeader(display,difficulty)
                    if speakerrect.collidepoint(click):
                        if volume:
                            volume = False
                            speaker_img = speaker_off
                        else:
                            volume = True
                            speaker_img = speaker_on
                    if mouse_presses[0]:
                        [row,col] = GetClickCoords(click[0],click[1],tilesize)
                        if row >= 0:
                            selected = tiles[row][col]
                            SetBombs(nummines,tiles,selected)
                            CalculateTileNumbers(tiles)
                            selected.Dig(display,1)
                            first = False
                    elif mouse_presses[1]:
                        pass
                    else:
                        [row,col] = GetClickCoords(click[0],click[1],tilesize)
                        if row >= 0:
                            selected = tiles[row][col]
                            SetBombs(nummines,tiles,selected)
                            CalculateTileNumbers(tiles)
                            selected.Dig(display,1)
                            first = False
            pygame.display.update()
            clock.tick(60)
        # Game loop for after first click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                click = pygame.mouse.get_pos()
                # Check for difficulty change
                if difrect.collidepoint(click):
                    difpointer = (difpointer + 1) % 4
                    [tiles,display,clock,minemap,flagmap,flags,font,subtime,time,difficulty,windowsize,boardarray,tilesize,nummines,recordline,first] = StartGame(difficultymap[difpointer])
                    difrect = UpdateHeader(display,difficulty)
                if speakerrect.collidepoint(click):
                    if volume:
                        volume = False
                        speaker_img = speaker_off
                    else:
                        volume = True
                        speaker_img = speaker_on
                if mouse_presses[0]:
                    # Handle left click
                    [row,col] = GetClickCoords(click[0],click[1],tilesize)
                    if row >= 0:
                        if not tiles[row][col].flagged:
                            lost = tiles[row][col].Dig(display,1)
                            if lost:
                                GameOver(display)
                                [tiles,display,clock,minemap,flagmap,flags,font,subtime,time,difficulty,windowsize,boardarray,tilesize,nummines,recordline,first] = StartGame(difficulty)
                elif mouse_presses[1]:
                    # Handle middle click
                    [row,col] = GetClickCoords(click[0],click[1],tilesize)
                    if row >= 0:
                        adjacenttiles = getAdjacent(tiles[row][col],tiles)
                        numadjflags = 0
                        if not tiles[row][col].covered:
                            for tile in adjacenttiles:
                                if tile.flagged:
                                    numadjflags+=1
                            if numadjflags == tiles[row][col].adjacentmines:
                                lost = tiles[row][col].QuickDig(display)
                                if lost:
                                    GameOver(display)
                                    [tiles,display,clock,minemap,flagmap,flags,font,subtime,time,difficulty,windowsize,boardarray,tilesize,nummines,recordline,first] = StartGame(difficulty)
                else:
                    # Handle right click
                    [row,col] = GetClickCoords(click[0],click[1],tilesize)
                    if row >= 0:
                        if tiles[row][col].covered:
                            flags = tiles[row][col].Flag(display,flags)
        # Check for game win
        if CheckforWin(tiles):
            GameWin(display,time)
            [tiles,display,clock,minemap,flagmap,flags,font,subtime,time,difficulty,windowsize,boardarray,tilesize,nummines,recordline,first] = StartGame(difficulty)
        pygame.display.update()
        # In game timer update
        clock.tick(60)
        subtime+=1
        if subtime == 60:
            subtime = 0
            time+=1



if __name__ == '__main__':
    main()