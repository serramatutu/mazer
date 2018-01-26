from PIL import Image
from mazegraph import MazeGraph, Point
import math

# Maze class
class Maze:
    def __init__(self, path):        
        im = Image.open(path)
        pixels = im.getdata()
        
        self.data = [[] for i in range(0, im.width)] # inicializa a matriz
        
        for i in range(0, len(pixels)):
            if pixels[i] > 127: # pixel branco
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
    
    def to_graph(self):
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
        
        self._single_neighbours = [] # variável privada é otimização para não recontar
        for y in range(1, self.height - 1): # descontando as bordas verticais
            open_row = None
            for x in range(1, self.width - 1): # descontando as bordas horizontais
                if self.data[x][y]: # se é branco
                    neighbours = self._count_white_neighbours(x, y)
                    point = Point(x, y)
                    open_col = open_cols.get(x, None)
                    
                    if neighbours != 2 or self.data[x-1][y] != self.data[x+1][y]:
                        graph.add_node(point)
                        open_cols[x] = point
                        if open_col == None:
                            open_col = point
                        if open_row == None:
                            open_row = point
                            
                    if neighbours <= 1:
                        self._single_neighbours.append(point) # marcado para morrer, pois é sem saída
                    
                    # checa por coluna aberta e fecha se necessário, conectando
                    if open_col != None and (neighbours > 2 or not self.data[x][y+1]): # se é ponto de conexão ou o abaixo é fechado
                        graph.add_edge(open_col, point) # conecta a coluna aberta ao ponto
                        if not self.data[x][y+1]: # fecha apenas se o abaixo for fechado
                            open_cols.pop(x, None)
                        
                    # checa por linha aberta e conecta quando necessário
                    if open_row != None and (neighbours > 2 or not self.data[x+1][y]): # se é ponto de conexão ou o esquerdo é fechado
                        graph.add_edge(open_row, point) # conecta a linha aberta ao ponto
                        open_row = point if (self.data[x+1][y]) else None # linha segue aberta apenas se for conexão
        
        #conecta a entrada ao logo abaixo
        y = 0
        for i in range(0, self.height): # vai para baixo até achar o mais embaixo
            if graph[graph.start.x, i] != None:
                y = i
                break
        graph.add_edge(graph.start, (graph.start.x, y))
        
        #conecta a saída ao logo acima
        graph.add_edge(graph.end, open_cols[graph.end.x])
        
        return graph
    
    
    def solve(self):
        graph = self.to_graph()
        
        # deve retirar do grafo todos os caminhos sem saída
        for point in self._single_neighbours: # criada em to_graph
            current = point
            while current != None and len(graph[current]) <= 1:
                deleted = current
                edges = graph[deleted]
                graph.remove_node(deleted)
                current = edges[0] if len(edges) > 0 else None
        
                
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
    
    def to_img(self, solved=False, 
               path_color=(255, 255, 255), 
               wall_color=(0, 0, 0),
               solution_color=(255, 0, 0)):
        im = Image.new('RGB', (self.width, self.height))
        
        # desenha o labirinto primeiro
        for x in range(0, self.width):
            for y in range(0, self.height):
                im.putpixel((x, y), path_color if self.data[x][y] else wall_color)
                
        if not solved:
            return im
        
        solution = self.solve()
        solution.to_img(im=im, node_color=solution_color, edge_color=solution_color)
        
        return im
    
    
    def _count_white_neighbours(self, x, y): # bleh
        n = 0
        if (self.data[x - 1][y]): n+=1
        if (self.data[x + 1][y]): n+=1
        if (self.data[x][y - 1]): n+=1
        if (self.data[x][y + 1]): n+=1
        return n