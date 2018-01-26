from PIL import Image
from mazegraph import MazeGraph, Point
import math

# Maze class
class Maze:
    def __init__(self, path):        
        im = Image.open(path)
        pixels = im.getdata()
        
        self.data = [[] for i in range(0, im.width)] # inicializa a matriz
        
        for i, pixel in enumerate(pixels):
            if pixel == (255, 255, 255): # pixel branco
                self.data[i % im.width].append(True); # tem caminho
            else:
                self.data[i % im.width].append(False); # não tem caminho
    
    def __str__(self):
        string = 'Maze:\n'
        for y in range(0, len(self.data)):
            for x in range(0, len(self.data[0])):
                string += ' ' if self.data[x][y] else '#'
            string += '\n'
        return string;
    
    @property
    def width(self):
        return len(self.data[0])
    
    @property
    def height(self):
        return len(self.data)
    
    def solve(self):
        graph = MazeGraph()
        
        open_cols = {} # colunas ainda não fechadas
        # encontrar entrada
        for i in range(0, self.width):
            if self.data[i][0]:
                point = Point(i, 0)
                graph.start = point
                open_cols[i] = point
                break
                
        # encontrar saida
        for i in range(0, self.width):
            if self.data[i][self.height - 1]:
                graph.end = (i, self.height - 1)
                break
        
        single_neighbours = []
        for y in range(1, self.height - 1): # descontando as bordas verticais
            open_row = None
            for x in range(1, self.width - 1): # descontando as bordas horizontais
                if self.data[x][y]: # se é branco
                    neighbours = self._count_white_neighbours(x, y)
                    point = Point(x, y)
                    
                    if neighbours != 2 or self.data[x-1][y] != self.data[x+1][y]:
                        graph.add_node(point)
                        open_cols[x] = point
                        if open_row == None:
                            open_row = point
                            
                    if neighbours <= 1:
                        single_neighbours.append(point) # marcado para morrer, pois é sem saída
                    
                    # checa por coluna aberta e fecha se necessário, conectando
                    if not self.data[x][y+1] and x in open_cols: # se abaixo é fechado
                        print ('a')
                        graph.add_edge(open_cols.pop(x), point) # conecta a coluna aberta ao ponto
                        
                    # checa por linha aberta e fecha se necessário, conectando
                    if open_row != None and not self.data[x+1][y]: # se o esquerdo é fechado
                        graph.add_edge(open_row, point) # conecta a linha aberta ponto
                        open_row = None # não há mais linha aberta
        
        #conecta a entrada ao logo abaixo
        start = graph.start
        graph.add_edge(start, (start.x, start.y + 1))
        
        #conecta a saída ao logo acima
        end = graph.end
        graph.add_edge(end, open_cols[end.x])
        
#        # deve retirar do grafo todos os caminhos sem saída
#        for point in single_neighbours:
#            current = point
#            while current != None and len(graph[current]) <= 1:
#                deleted = current
#                edges = graph[deleted]
#                graph.remove_node(deleted)
#                current = edges[0] if len(edges) > 0 else None
                
        # limpa o grafo, retirando nós inúteis
#        current = graph[graph.start][0] # primeiro depois do começo
#        last = graph.start
#        while current != end:
#            edges = graph[current]
#            print (str(current) + ' : ' + str(edges))
#            if self.data[current.x - 1][current.y] == self.data[current.x + 1][current.y]: # se não for canto
#                graph.remove_node(current)
#                graph.add_edge(edges[0], edges[1])
#            temp = current
#            current = edges[0 if edges[0] != last else 1]
#            last = temp
            
        
        return graph
    
    def _count_white_neighbours(self, x, y): # bleh
        n = 0
        if (self.data[x - 1][y]): n+=1
        if (self.data[x + 1][y]): n+=1
        if (self.data[x][y - 1]): n+=1
        if (self.data[x][y + 1]): n+=1
        return n