from PIL import Image
from mazegraph import MazeGraph, Point

# Maze class
class Maze:
    def __init__(self, path):        
        im = Image.open(path)
        pixels = im.getdata()
        
        self.data = [[] for i in range(0, im.width)] # inicializa a matriz
        
        for i, pixel in enumerate(pixels):
            if pixel == (255, 255, 255): # pixel branco
                self.data[i // im.width].append(True); # tem caminho
            else:
                self.data[i // im.width].append(False); # não tem caminho
    
    def __str__(self): # tipo um tostring
        string = str()
        for row in self.data:
            for cell in row:
                string += ' ' if cell else 'x'
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
        
        # encontrar entrada
        for i in range(0, self.width):
            if self.data[i][0]:
                solution.start = (i, 0)
                break
                
        # encontrar saida
        for i in range(0, self.width):
            if self.data[i][self.height - 1]:
                solution.end = (i, 0)
                break
        
        for x in range(1, self.width - 1): # desconta as bordas horizontais
            for y in range(1, self.height - 1): # desconta as bordas verticais
                if self.data[x][y]: # se é branco
                    if self._count_neighbours(x, y) != 2:
                        graph.add_node((i, 0))
                
                
        return graph
    
    def _count_neighbours(self, x, y): # bleh
        n = 0
        if (self.data[x - 1][y]): n+=1
        if (self.data[x + 1][y]): n+=1
        if (self.data[x][y - 1]): n+=1
        if (self.data[x][y + 1]): n+=1
        return n