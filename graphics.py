import pygame as pg
import sys
import functions as f
pg.init()

    
#window
l = 640
h = 480
FPS_CLOCK = pg.time.Clock()
screen = pg.display.set_mode((l, h),pg.RESIZABLE)
pg.display.set_caption("Battleship")
screen.fill((255, 249, 143))

#title
f.written("Battleship", "broadway", 40, True, f.vert, (l/2, h/3),screen)
s = 20
#buttons
long = 5*s
larg = 2*s
pos = [(l/2 - long/2,h/2-larg/2+(larg+s)*i) for i in range(3)]
b1 = f.button(pos[0], long, larg, f.vertfonce,0, screen)
b2 = f.button(pos[1], long, larg, f.rougefonce,0,screen)
b3 = f.button(pos[2], long, larg, f.bleufonce,0,screen)
#text
f.written("Play !", "broadway", s, True, f.vert, (l/2, h/2), screen)
f.written("Quit", "broadway", s, True, f.rouge, (l/2,3*s+h/2), screen)
f.written("Help", "broadway", s, True, f.bleu, (l/2, h/2+6*s), screen)


menu = 1
while menu: #While user in menu window
    for event in pg.event.get():
        if event.type == pg.QUIT :
            sys.exit()
            pg.quit()
            menu = 0 
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pg.mouse.get_pos()
            bplay_ = b1.collidepoint(x,y)
            bquit_ = b2.collidepoint(x,y)
            bhelp_ = b3.collidepoint(x,y)
            if bplay_ or bquit_ or bhelp_: #Button play or quit or help
                menu = False 
            pg.display.update()
            FPS_CLOCK.tick(60)

if bplay_: #Button play
    f.button(pos[0], long, larg, f.vertclair, 3, screen) #highlight the button
    pg.time.delay(500)
    
    #PLACEMENT PHASE
    a = min(l,h)
    s = 40 #space to the borders of the window
    cell = (a-2*s)/10 #dimension of a cell
    coord = f.Grid(l,h,a,s,cell) #display grid + store coordinates of the grid (xmin, xmax, ymin, ymax)
    xcentercell = [coord[0]+ cell/2 + i*cell for i in range(10)] #x coordinates of center of cells
    ycentercell = [coord[2]+ cell/2 + i*cell for i in range(10)] #y coordinates of center of cells
    
    players = ["Player 1", "Player 2"]
    colors = [(185, 15, 11), (241, 191, 0)]
    for p in range(2):
        print(players[p]+" has to place its ships.")
        #ROTATION OF SHIPS (eventually arrow event) in the Command interface (to complicated to do it graphically)
        print("Clic on the desired cell corresponding to the ship's top-left corner.")
        pg.time.delay(1000)
        f.Grid(l,h,a,s,cell)
        
        cptclic = 0 #counts number of VALID clics in the grid
        listclicpos = [] #position of the clics
        while cptclic != 5 :  
            for event in pg.event.get():
                if event.type == pg.QUIT :
                    sys.exit()
                    pg.quit()
                    cptclic = 5
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: #right clic
                    x, y = pg.mouse.get_pos()
                    x,y,validclic = f.PosClicCenterCell(x,y,cell,coord, listclicpos, xcentercell, ycentercell)
                    if validclic:
                        cptclic += 1 #increase count of valid clics
                        dim = cell #dimension of boat
                        f.button((x-dim/2, y-dim/2), dim, dim, colors[p], 0, screen)
                        listclicpos.append((x,y))
                        #RELIER PYGAME PYTHON AVEC POSITION CLIC ET LISTE
            pg.display.update()
    
    #GAME PHASE
    '''
    while (unsunk ships both players) :
        for loop in range(2):
            cptclic = 0
            listclicpos = []
            while cptclic != 1 :  
                for event in pg.event.get():
                    if event.type == pg.QUIT :
                        sys.exit()
                        pg.quit()
                        cptclic = 1
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        x, y = pg.mouse.get_pos()
                        x,y,validclic = f.PosClicCenterCell(x,y,cell,coord, listclicpos, xcentercell, ycentercell)
                        if validclic:
                            cptclic += 1 #increase count of valid clics
                            dim = cell #dimension of boat
                            f.button((x-dim/2, y-dim/2), dim, dim, colors[p], 0, screen)
                            listclicpos.append((x,y))
                            #####RELIER PYGAME PYTHON AVEC POSITION CLIC ET LISTE
                pg.display.update()
                if (x,y) corresponds to position of a ship:
                    ...
                    if this ship is sunk:
                        ...
        
    '''
elif bquit_: #Button quit
    f.button(pos[1], long, larg, f.rougeclair, 3, screen)
elif bhelp_: #Button help
    f.button(pos[2], long, larg, f.bleuclair, 3, screen)
