import operator
from PIL import Image

class Point:
    def __init__(self, x=0, y=0):
        self._x = x;
        self._y = y;
        
    def __eq__(self, obj):
        return isinstance(Point.from_obj(obj), Point) and obj._x == self._x and obj._y == self._y
    
    x = property(operator.attrgetter('_x'))
    
    y = property(operator.attrgetter('_y'))
    
    @staticmethod
    def from_obj(obj):
        if isinstance(obj, Point):
            return obj
        if isinstance(obj, (tuple, list)) and len(obj) == 2:
            return Point(obj[0], obj[1])
        
    def __getitem__(self, key):
        if not isinstance(key, int) or key > 1:
            raise ValueError("key must be either 0 or 1")
        return self.x if key == 0 else self.y
    
    def __str__(self):
        return '(' + str(self._x) + ', ' + str(self._y) + ')'
    
    def __repr__(self):
        return '(' + str(self._x) + ', ' + str(self._y) + ')'
    
    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

# MazeGraph class
# implementa um grafo de pontos por lista de adjacência
class MazeGraph:
    
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end
        self._nodes = {} # dicionário de nós do grafo
        
    def add_node(self, point):
        if point != None:
            obj = Point.from_obj(point)
            if not isinstance(obj, Point):
                raise ValueError("argument should be of type Point")
            if not obj in self._nodes:
                self._nodes[obj] = []
            
    def remove_node(self, point):
        obj = Point.from_obj(point)
        if obj in self._nodes: # apenas se o nó existir
            for edge in self._nodes[obj]: # remove referências ao nó
                self._nodes[edge].remove(obj)
            del self._nodes[obj] # remove o nó em si
            
    def add_edge(self, a, b):
        obj_a = Point.from_obj(a)
        obj_b = Point.from_obj(b)
        
        if not all(point in self._nodes for point in [obj_a, obj_b]):
            raise ValueError("points a and b should be in graph already")
            
        # conecta os dois na lista de adjacência apenas se forem diferentes
        if (obj_a != obj_b):
            self._nodes[obj_a].append(obj_b)
            self._nodes[obj_b].append(obj_a)
        
    def remove_edge(self, a, b):
        obj_a = Point.from_obj(a)
        obj_b = Point.from_obj(b)
        
        if not all(point in self._nodes for point in [obj_a, obj_b]):
            raise ValueError("points a and b should be in graph already")
        # desconecta os dois na lista de adjacência
        self._nodes[obj_a].remove(obj_b)
        self._nodes[obj_b].remove(obj_a)
    
    def __getitem__(self, point):
        obj = Point.from_obj(point)
        if obj in self._nodes:
            return self._nodes[obj];
        return None
    
    def has_node(self, point):
        obj = Point.from_obj(point)
        return obj in self._nodes
    
    def has_edge(self, a, b):
        obj_a = Point.from_obj(a)
        obj_b = Point.from_obj(b)
        
        return obj_b in self._nodes[obj_a]
            
            
    def __str__(self):
        return str(self._nodes)
    
    # iterador
    def __iter__(self):
        return iter(self._nodes.items())
    
    @property
    def nodes(self):
        return list(self._nodes.keys());
    
    def to_img(self, im=None, node_color=(255, 0, 0), edge_color=(0, 255, 0)):
        w,h = 0, 0
        for node in self.nodes:
            if node.x >= w:
                w = node.x + 1
            if node.y >= h:
                h = node.y + 1
                
        if im == None:
            im = Image.new('RGB', (w, h))
        
        for node, edges in self:
            for n in edges:
                if node.x != n.x:
                    for i in range(node.x, n.x):
                        im.putpixel((i, node.y), edge_color)
                else:
                    for i in range(node.y, n.y):
                        im.putpixel((node.x, i), edge_color)
            im.putpixel((node.x, node.y), node_color)
        return im
        
        
    # Getters e setters
    
    start = property(operator.attrgetter('_start'))
    
    @start.setter
    def start(self, point):
        obj = Point.from_obj(point)
        self.add_node(obj)
        self._start = obj
    
    end = property(operator.attrgetter('_end'))
    
    @end.setter
    def end(self, point):
        obj = Point.from_obj(point)
        self.add_node(obj)
        self._end = obj