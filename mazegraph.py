import operator

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
        
    def __str__(self):
        return '(' + self._x + ', ' + self._y + ')'
    
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
            self._nodes.remove(obj) # remove o nó em si
            
    def add_edge(self, a, b):
        obj_a = Point.from_obj(a)
        obj_b = Point.from_obj(b)
        
        if not all(point in self._nodes for point in [obj_a, obj_b]):
            raise ValueError("points a and b should be in graph already")
        # conecta os dois na lista de adjacência
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
    
    def get_adjacent_edges(self, point):
        return self._nodes[Point.from_obj(point)];
            
            
    def __str__(self):
        string = str()
        for point, edges in self._nodes:
            string += point + ': ' + edges + '\n'
        return string
        
    # Getters e setters
    
    start = property(operator.attrgetter('_start'))
    
    @start.setter
    def start(self, point):
        self.add_node(point)
        self._start = point
    
    end = property(operator.attrgetter('_end'))
    
    @end.setter
    def end(self, point):
        self.add_node(point)
        self._end = point