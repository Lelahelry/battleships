# -*- coding: utf-8 -*-
"""
Created on Tue May 24 14:57:26 2022

@author: Orane
"""
import pygame as pg

pg.init()

vert = (63,128,70)
vertclair = (64, 255, 64)
vertfonce = (119, 221, 119)
rouge = (185, 15, 11)
rougeclair = (255, 64, 64)
rougefonce = (221, 119, 119)
bleu = (0, 68, 125)
bleuclair = (64, 64, 255)
bleufonce = (119, 119, 221)
jaune = (241, 191, 0)
jaunepale = (246, 255, 41)
r_orange = (255, 85, 64)
noir = (0, 0, 0)


def written(text,font,size,bold, color, pos,screen): #create written text
    myfont = pg.font.SysFont(font, size)
    TextSurf = myfont.render(text, bold, color)
    TextRect = TextSurf.get_rect()
    TextRect.center = pos
    screen.blit(TextSurf, TextRect)#"collage" des textes sur l'écran
    pg.display.flip()

def button(pos, long, larg, color,borderad,screen):
    rect_object = pg.Rect(pos[0], pos[1], long, larg)
    pg.draw.rect(screen, color, rect_object, borderad)
    pg.display.flip()
    return(rect_object)

def Grid(l,h,a,s,cell):
    '''Create a square grid of length a, cell dimention cell, and with s space between the borders and the grid'''
    #window
    screen = pg.display.set_mode((l, h))
    pg.display.set_caption("Battleship")
    screen.fill(bleuclair)
    pg.display.flip()
        
    ###GRID
    #to center the position of the square grid for any window size
    if h<l:
        ecartx = abs(l-h)/2
        ecarty = 0
    else:
        ecartx = 0
        ecarty = abs(l-h)/2
    #cells
    for i in range(11):
        pg.draw.line(screen, (0,0,0), (s+ecartx, i*cell+s+ecarty), (a-s+ecartx, i*cell+s+ecarty))
        pg.draw.line(screen, (0,0,0), (i*cell+s+ecartx, s+ecarty), (i*cell+s+ecartx, a-s+ecarty))
        pg.display.flip()
    #writing and typography
    t = 15
    font = pg.font.SysFont("comicsansms", t)
    alph = ["A","B","C","D","E","F","G","H","I","J"]
    for i in range(10):
        t1 = font.render(str(i+1), True, (0, 0, 0))
        screen.blit(t1, (ecartx, ecarty+s+(i+1/2)*cell-t/2))
        t2 = font.render(alph[i], True, (0, 0, 0))
        screen.blit(t2, (ecartx+s+cell*(i+1/2), ecarty))
        pg.display.flip()
    return (s+ecartx, a-s+ecartx, s+ecarty, a-s+ecarty) #coordinates of the grid

'''
def Placmt(l, h, color, player, font, size,screen):
    long = l
    larg = 200
    borderad = 0
    pos = ((l-long)/2, (h-larg)/2)
    button(pos, long, larg, color, borderad, screen)
    written(player,font,size,True, noir,(l/2,h/2), screen)
    written("Place your boats as you wish",font,size-30,False, noir,(l/2,h/2+40), screen)
    pg.display.flip()'''

def PosClicCenterCell(x,y,cell, coord, listclicpos, xcentercell, ycentercell):
    validclic = False
    if (coord[0] <= x and x <= coord[1]) and (coord[2] <= y and y <= coord[3]): #in the grid
        i=0
        j=0
        while abs(x-xcentercell[i]) > cell/2:
            i += 1
        while abs(y-ycentercell[j]) > cell/2:
            j += 1
            
        if (abs(x-xcentercell[i]) == cell/2) or (abs(y-ycentercell[j]) > cell/2):
            print("Don't clic on a line !!")
        elif (xcentercell[i],ycentercell[j]) in listclicpos:
            print("You already clicked here !!")
        else:
            x = xcentercell[i]
            y = ycentercell[j]
            validclic = True
    else: #not in grid
        print("Clic in the grid !!")
        
    return x,y, validclic