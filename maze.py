from PIL import Image
from mazegraph import MazeGraph, Point
from mazematrix import ListMazeMatrix, ImageMazeMatrix
import math

# Maze class
class Maze:
    def __init__(self, arg):
        if isinstance(arg, str) or isinstance(arg, Image.Image):
            self.data = ImageMazeMatrix(arg)
        elif isinstance(arg, list):
            self.data = ListMazeMatrix(arg)
        else:
            raise ValueError("invalid maze initialization")
    
    def __str__(self):
        string = 'Maze:\n'
        for y in range(0, len(self.data)):
            for x in range(0, len(self.data[0])):
                string += ' ' if self.data[x][y] else '#'
            string += '\n'
        return string
    
    def __getitem__(self, key):
        return data[key]
    
    @property
    def width(self):
        return self.data.width
    
    @property
    def height(self):
        return self.data.height
    
    def to_graph(self):
        graph = MazeGraph()
        
        open_cols = {} # colunas ainda não fechadas
        
        def _assign_graph_border(point): # atribui um ponto a um dos finais do grafo
            if point.y == 0:
                open_cols[point.x] = point # só é coluna aberta se estiver no topo
            if graph.start == None:
                graph.start = point
                return False
            else:
                graph.end = point
                return True
            
        # encontrar entrada/saída nas fileiras de horizontais
        for i in range(1, self.width - 1):
            if self.data[i][0]:
                if _assign_graph_border(Point(i, 0)):
                    break
            if self.data[i][self.height - 1]:
                if _assign_graph_border(Point(i, self.height - 1)):
                    break
                
        # encontrar entrada/saída nas fileiras de verticais
        if graph.end == None:
            for i in range(1, self.height - 1):
                if self.data[0][i]:
                    if _assign_graph_border(Point(0, i)):
                        break
                if self.data[self.width - 1][i]:
                    if _assign_graph_border(Point(self.width - 1, i)):
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
        
        def _find_close_node(start, end, x=None, y=None):
            ix, iy = 0, 0 
            for i in range(start, end):
                ix = i if x == None else x
                iy = i if y == None else y
                if graph[ix, iy] != None:
                    return Point(ix, iy)
        
        def _connect_border(node):
            if node.x == 0:
                graph.add_edge(node, _find_close_node(1, self.width - 2, y=node.y))
            elif node.x == self.width - 1:
                graph.add_edge(node, _find_close_node(self.width - 2, 1, y=node.y))
            elif node.y == 0:
                graph.add_edge(node, _find_close_node(1, self.height - 2, x=node.x))
            else:
                graph.add_edge(node, open_cols[node.x]) # caso seja embaixo é só procurar a coluna aberta
        
        # conecta as pontas ao grafo
        _connect_border(graph.start)
        _connect_border(graph.end)
        
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
#        while current != graph.end:
#            edges = graph[current]
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
        solution.to_img(im=im, node_color=solution_color, edge_color=solution_color, start_at_zero=True)
        
        return im
    
    
    def _count_white_neighbours(self, x, y): # bleh
        n = 0
        if (self.data[x - 1][y]): n+=1
        if (self.data[x + 1][y]): n+=1
        if (self.data[x][y - 1]): n+=1
        if (self.data[x][y + 1]): n+=1
        return n