from PIL import Image
from mazegraph import MazeGraph

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
                string += '0' if cell else '1'
            string += '\n'
        return string;
    
    def solve(self):
        solution = MazeGraph()