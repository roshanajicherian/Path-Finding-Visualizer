import pygame
import sys
import os
import tkinter as tk
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
pygame.init()
win = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Pathfinding Visualizer')


class player(object):
    def __init__(self, rect_x, rect_y):
        self.x = rect_x
        self.y = rect_y
        self.g = 0
        self.h = 0
        self.f = 0
        self.neigbour = []
        self.block = False
        self.closed = False
        self.previous = None
        self.value = 1

    def draw(self, color, thick):
        if self.closed == False:
            pygame.draw.rect(
                win, color, (self.x*wid, self.y*ht, wid, ht), thick)
            pygame.display.update()

    def FindNeighbour(self, grid):

        i = self.x
        j = self.y
        if i < col-1 and grid[i+1][j].block == False:
            self.neigbour.append(grid[i+1][j])
        if i > 0 and grid[i-1][j].block == False:
            self.neigbour.append(grid[i-1][j])
        if j < row-1 and grid[i][j+1].block == False:
            self.neigbour.append(grid[i][j+1])
        if j > 0 and grid[i][j-1].block == False:
            self.neigbour.append(grid[i][j-1])


row = 25
col = 25
wid = 800/row
ht = 800/col
pink = (255, 8, 127)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
openSet = []
closedSet = []
grid = [[0 for i in range(col)] for j in range(row)]
start = grid[1][1]
end = grid[2][2]
for i in range(row):
    for j in range(col):
        grid[i][j] = player(i, j)

for i in range(row):
    for j in range(col):
        grid[i][j].draw(white, 2)


def OnSubmit():
    global start
    global end
    st = d1.get().split(',')
    ed = e1.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    winin.quit()
    winin.destroy()


winin = tk.Tk()
winin.title('Input')
Label(winin, text='Start').grid(row=0)
Label(winin, text='End').grid(row=1)
d1 = Entry(winin)
e1 = Entry(winin)
d1.grid(row=0, column=1)
e1.grid(row=1, column=1)
step = IntVar()
w = ttk.Checkbutton(winin, text='Show Steps', onvalue=1,
                    offvalue=0, variable=step)
w.grid(row=4)
button = tk.Button(winin, text='Test', width=20, bd=4,
                   justify=CENTER, command=OnSubmit)
button.grid(row=5, column=1)
winin.mainloop()
openSet.append(start)
start.draw(pink, 0)
end.draw(pink, 0)
# function to convert the mouse press to an obstruction by altering obs value


def mousepress(loc):
    x_mouse = loc[0]
    y_mouse = loc[1]
    x_mouse_eq = x_mouse//(800//row)
    y_mouse_eq = y_mouse//(800//col)
    state = grid[x_mouse_eq][y_mouse_eq]
    if state != start and state != end:
        if state.block == False:
            state.block = True
            state.draw(white, 0)


loop = True
while loop:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:

                loc = pygame.mouse.get_pos()
                mousepress(loc)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
                break

for i in range(col):
    for j in range(row):
        grid[i][j].FindNeighbour(grid)


def heu(s, e):
    dis = abs(math.sqrt(((s.x-e.x)**2)+((s.y-e.y)**2)))
    return dis


def main():
    start.draw(pink, 0)
    end.draw(pink, 0)
    if len(openSet) > 0:
        low = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[low].f:
                low = i
        current = openSet[low]
        if(current == end):
            print('Done')
            start.draw(pink, 0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.draw(blue, 0)
                current = current.previous
            end.draw((255, 8, 127), 0)
            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', ('Shortest Distance : ' + str(
                temp) + '\n Would you like to re run the program?'))
            if result == True:
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()
        openSet.pop(low)
        closedSet.append(current)
        nei_ls = current.neigbour
        for i in range(len(nei_ls)):
            nei = nei_ls[i]
            if nei not in closedSet:
                tempG = current.g+1
                if nei in openSet:
                    if nei.g > tempG:
                        nei.g = tempG
                else:
                    nei.g = tempG
                    openSet.append(nei)
            nei.h = heu(nei, end)
            nei.f = nei.g+nei.h
            if nei.previous == None:
                nei.previous = current
    if step.get():
        for i in range(len(openSet)):
            openSet[i].draw(green, 0)
        for i in range(len(closedSet)):
            if closedSet[i] != start:
                closedSet[i].draw(red, 0)
    # current.closed = True


while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    main()
