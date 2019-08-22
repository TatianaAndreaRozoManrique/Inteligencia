
import os
import util
import time
import sys
import pygame
import search
import numpy as np
import pyautogui


from matplotlib import colors
from graphviz import Graph, Digraph
from IPython.display import display
# from __future__ import print_function, division
if(len(sys.argv) <= 1):
    print ("Error: insert the command-line arguments passed to the script.")
    print ("       1. Depth-first search (FDS).")
    print ("       2. Breath-first Search (BFS).")
    print ("       3. Uniform cost search (UCS) .")
    sys.exit()

if sys.argv[1] == '1':
    source = 'Depth-first search'
elif sys.argv[1] == '2':
    source = 'Breath-first Search'
elif sys.argv[1] == '3':
    source = 'Uniform cost search'
else:
    print ("Error: insert a valid value.")
    print ("       1. Depth-first search (FDS).")
    print ("       2. Breath-first Search (BFS).")
    print ("       3. Uniform cost search (UCS).")
    sys.exit()

x_win = 100
y_win = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x_win,y_win)
width =630
height=630
Margen=1
Dic_Color = {}
Dic_Cuadros = {}
ancho = (width) /30 - Margen
largo = (height)/30 - Margen
pygame.init()
# pygame.display.set_caption("Press ESC to quit")
screen=pygame.display.set_mode((width,height), pygame.DOUBLEBUF)
background = pygame.Surface(screen.get_size()).convert()
background.fill((0,0,0))
screen.blit(background, (0,0))
pygame.display.flip()

class search_tree():
    def __init__(self):
        self.graph = Digraph(graph_attr = {'size':'900'})

    def addNode(self, name, label):
        self.graph.node(name, label)

    def addEdge(self, source, action, target):
        self.graph.edge(source, target, action)

    def getDot(self):
        return self.graph

class graph_problem(search.SearchProblem):
    def __init__(self, vertices, edges, Agente, Gold):
        self.G = {v:{} for v in vertices}
        for v1, v2, c in edges:
            (self.G[v1])[v2] = c
            #(self.G[v2])[v1] = c
        self.start = Agente
        self.goal = Gold

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return self.goal == state

    def getSuccessors(self, state):
        successors = [(suc, str(state) + '->' + str(suc),
                       (self.G[state])[suc]) for suc in self.G[state]]
        return successors

def graphDot(g_prob, color):
    #dot = Graph(graph_attr = {'size':'3.5'})
    dot = Digraph('hola')
    dot.attr(rankdir='LR', size='8,5')
    for node in g_prob.G:
        if not node in color:
            dot.node(node)
        else:
            dot.node(node, style = 'filled', color = color[node])
    for n1 in g_prob.G:
        for n2 in g_prob.G[n1]:
            dot.edge(n1, n2, label=str(g_prob.G[n1][n2]))
    return dot

def general_search(problem, frontier,Agente,Gold):
    visited = []
    Final = []
    Final2 = []
    state = problem.getStartState()
    frontier.push((state, [], Agente))
    tree = search_tree()
    tree.addNode(str(state)+"[]",str(state))
    while not frontier.isEmpty():
        u, actions, path_cost = frontier.pop()
        Dic_Cuadros[u]['Color'] = Dic_Color['blue']
        pygame.draw.rect(background, Dic_Cuadros[u]['Color'], (Dic_Cuadros[u]['x'],Dic_Cuadros[u]['y'],ancho,largo))
        screen.blit(background, (0, 0))
        pygame.display.flip()
        if problem.isGoalState(u):
            if sys.argv[1] == '3':
                print('Costo =', path_cost)
            return  actions, tree
        if not u in visited:
            visited.append(u)
            for v, action, cost in problem.getSuccessors(u):
                if v not in visited:
                    tree.addNode(str(v) + str(actions+[action]), str(v))
                    tree.addEdge(str(u) + str(actions), str(cost), str(v) + str(actions+[action]))
                    frontier.push((v, actions + [action], path_cost + cost))

    return [], tree

def uniformCostSearch(problem,Agente,Gold):
    def g_cost(item):
        return item[2]
    if sys.argv[1] == '1':
        return general_search(problem, util.Stack(),Agente,Gold)
    elif sys.argv[1] == '2':
        return general_search(problem, util.Queue(),Agente,Gold)
    elif sys.argv[1] == '3':
        return general_search(problem, util.PriorityQueueWithFunction(g_cost),Agente,Gold)

    #
    #






def run():
    pygame.display.set_caption('Agente')
    clock = pygame.time.Clock()
    FPS = 30
    playtime = 0.0
    Running = True
    Colors_M()
    Print_white()
    Paint_problem()
    milliseconds = clock.tick(FPS)
    playtime += milliseconds / 1000.0
    screenshot = pyautogui.screenshot(region=(x_win, y_win, 630, 658))
    screenshot.save("screenshot.png")
    text = "he agent arrived in: {0:.2f}".format(playtime)
    print(text, 'seconds with', source )

def Colors_M():
    Dic_Color['white'] = np.multiply(255,colors.hex2color(colors.cnames['white']))
    Dic_Color['black'] = np.multiply(255,colors.hex2color(colors.cnames['black']))
    Dic_Color['red'] = np.multiply(255,colors.hex2color(colors.cnames['red']))
    Dic_Color['green'] = np.multiply(255,colors.hex2color(colors.cnames['green']))
    Dic_Color['thistle'] = np.multiply(255,colors.hex2color(colors.cnames['thistle']))
    Dic_Color['blue'] = np.multiply(255,colors.hex2color(colors.cnames['blue']))

def Print_white():
    x = Margen
    y = Margen
    Num = 0
    for h in range(0,30):
        for v in range(0,30):
            Dic_Cuadros[Num] = {'Color':Dic_Color['white'],'x': x,'y': y}
            Num +=1
            y = y + largo + Margen
        y = Margen
        x = x + ancho + Margen

def Paint_problem():
    Posiciones=[]
    vec=[]
    vertices = []
    with open('hi.txt') as archivo:
        with_out = [ar.rstrip('\n') for ar in archivo]
        for ar in with_out:
          Posiciones.append(ar.split(','))
        for x in Posiciones:
            vec.append([int(i) for i in x])
    for w in range(len(vec)):
        color_ =""
        x_a = vec[w][0] *((width)/30) + Margen
        y_a = vec[w][1] *((height)/30) + Margen
        x = Margen
        y = Margen
        Num = 0
        for h in range(0,30):
            for v in range(0,30):
                if Dic_Cuadros[Num]['x'] == x_a and Dic_Cuadros[Num]['y'] == y_a:
                    if w == 0:
                        Agente = Num
                        color_ ='red'
                        vertices.append(Num)
                    elif w == 1:
                        Gold = Num
                        color_ ='green'
                        vertices.append(Num)
                    else:
                        color_ = 'black'
                    Dic_Cuadros[Num] = {'Color':Dic_Color[color_],'x': x_a,'y': y_a}
                Num +=1
                y = y + largo + Margen
            y = Margen
            x = x + ancho + Margen

    x = Margen
    y = Margen
    Num = 0
    for h in range(0,30):
        for v in range(0,30):
            pygame.draw.rect(background, Dic_Cuadros[Num]['Color'], (x,y,ancho,largo))
            if np.array_equiv(Dic_Cuadros[Num]['Color'],Dic_Color['white']):
                vertices.append(Num)
            Num +=1
            y = y + largo + Margen
        y = Margen
        x = x + ancho + Margen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    Orientacion = []
    Dere = []
    Izq = []
    for x in range(0,30):
        Dere.append(30*(x+1))
        Izq.append(30*(x+1)-1)
    for pos in vertices:
        N = pos-30
        S = pos+30
        O = pos-1
        E = pos+1
        if N>=0 and N in vertices:
            Orientacion.append((pos, N, 1))
        if S<=900 and S in vertices:
            Orientacion.append((pos, S, 1))
        if O>=0 and O in vertices and not(O in Izq):
            Orientacion.append((pos, O, 1))
        if E in vertices and not(E in Dere):
            Orientacion.append((pos, E, 1))
    problem = graph_problem(vertices, Orientacion,Agente,Gold)
    actions2, tree2 = uniformCostSearch(problem,Agente,Gold)
    Final = []
    Final2 = []
    for c in actions2:
        Final.append(c.split('->'))
    for x in Final:
        Final2.append([int(i) for i in x])
    for x in Final2:
        Dic_Cuadros[x[0]]['Color'] = Dic_Color['thistle']
    x = Margen
    y = Margen
    Num = 0
    for h in range(0,30):
        for v in range(0,30):
            pygame.draw.rect(background, Dic_Cuadros[Num]['Color'], (x,y,ancho,largo))
            Num +=1
            y = y + largo + Margen
        y = Margen
        x = x + ancho + Margen
    screen.blit(background, (0, 0))
    pygame.display.flip()



if __name__ == '__main__':
    run()
