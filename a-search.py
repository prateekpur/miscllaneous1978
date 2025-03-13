from pyamaze import maze
from queue import PriorityQueue
import matplotlib.pyplot as plt

def h(cell1, cell2):
    x1,y1 = cell1
    x2,y2 = cell2
    return abs(x1-x2) + abs(y1-y2)

def astar(m):
    start=(m.rows,m.cols)
    g_score={cell:float('inf') for cell in m.grid}
    g_score[start] = 0
    f_score={cell:float('inf') for cell in m.grid}
    f_score[start] = g_score[start] + h(start, (1,1))

    open=PriorityQueue()
    open.put((h(start, (1,1)), h(start, (1,1)), start))

    while not open.empty():
        currCell = open.get()[2]
        if currCell == (1,1):
            break
        for d in 'ESNW' :
            if m.maze_map[currCell][d] == True :
                if d=='E':
                    childCell = (currCell[0], currCell[0]+1)
                if d=='W':
                    childCell = (currCell[0], currCell[0]-1)
                if d=='N':
                    childCell = (currCell[0]-1, currCell[0])
                if d=='S':
                    childCell = (currCell[0]+1, currCell[0])

                temp_g_score=g_score[currCell]+1
                temp_f_score=temp_g_score+h(childCell, (1,1))
                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score, h(childCell, (1,1)), childCell))


m=maze()
m.CreateMaze()
astar(m)

m.run()