from random import randint
import numpy

'''
start with the maze completely solid (all 1's).
mark one block as empty (0) for the maze starting point
loop through the entire grid of blocks:
  if empty: 
    check neighbours (5x5)
    if neighbour solid (1) and not touching empty (0):  
      if roll dice [0..1] > .5:
        mark empty (0)
keep looping until done
mark edge block empty (0) for exit point
'''

MAZE_W = 12
MAZE_H = 12
MAZE = [[int(1) for x in range(MAZE_W)]for y in range(MAZE_H)]
MAZE[0][randint(0, MAZE_W-1)] = 0

def touchingEmpty(X,Y):
    if MAZE[Y][X-1] == 1:
        if randint(0, 100) >= 50:
                MAZE[Y][X-1] = 0
    if MAZE[Y][X+1] == 1:
        if randint(0, 100) >= 50:
                MAZE[Y][X+1] = 0
    if MAZE[Y-1][X] == 1:
        if randint(0, 100) >= 50:
                MAZE[Y-1][X] = 0
    if MAZE[Y+1][X] == 1:
        if randint(0, 100) >= 50:
                MAZE[Y+1][X] = 0

for j in range(0,MAZE_H-1):
    for w in range(0,MAZE_W-1):
        if MAZE[j][w] == 0: 
            #if j-1 >= 0: touchingEmpty(w,j-1)
            #if j+1 < MAZE_W-1: touchingEmpty(w,j+1)
            #if w-1 >= 0: touchingEmpty(w-1,j)
            #if w+1 < MAZE_H-1: touchingEmpty(w+1,j)
            touchingEmpty(w,j)

maze = numpy.asarray(MAZE)
numpy.savetxt("foo.txt", maze, fmt="%d",delimiter=",")


from random import shuffle, randrange
 
def make_maze(w = 12, h = 6):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["1,"] * w for _ in range(h)] + [[]]
    hor = [["1,"] * w for _ in range(h + 1)]
 
    def walk(x, y):
        vis[y][x] = 1
 
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "0,"
            if yy == y: ver[y][max(x, xx)] = "0,"
            walk(xx, yy)
 
    walk(randrange(w), randrange(h))
 
    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    return s
 
if __name__ == '__main__':
    print(make_maze())