import operator

# MazeGraph class
# implementa um grafo de pontos por lista de adjacência
class MazeGraph:
    @staticmethod
    def _ispoint(p):
        return (isinstance(p, (tuple, list)) and 
                isinstance(p[0], int) and isinstance(p[1], int))
    
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end
        self._nodes = [] # lista de nós do grafo
        
    def add_node(self, point)
        if not point in self._nodes
            self._nodes[point] = []
            
    def remove_node(self, point)
        if point in self._nodes: # apenas se o nó existir
            for edge in self._nodes[point]: # remove referências ao nó
                self._nodes[edge].remove(point)
            self._nodes.remove(point) # remove o nó em si
            
    def add_edge(self, a, b):
        if not all(point in self._nodes for point in [a, b]):
            raise ValueError("points a and b should be in graph already")
        # conecta os dois na lista de adjacência
        self._nodes[a].append(b);
        self._nodes[b].append(a);
        
    def remove_edge(self, a, b):
        if not all(point in self._nodes for point in [a, b]):
            raise ValueError("points a and b should be in graph already")
        # desconecta os dois na lista de adjacência
        self._nodes[a].remove(b);
        self._nodes[b].remove(a);
    
    def get_adjacent_edges(self, point)
        return self._nodes[point];
            
            
    # Getters e setters
    
    start = property(operator.attrgetter('_start'))
    
    @start.setter
    def start(self, point, connections=None):
        if point != None and not MazeGraph._ispoint(point)
            raise AttributeError("point should be (int, int)")
        self.add_node(point)
        self._start = point
    
    end = property(operator.attrgetter('_end'))
    
    @end.setter
    def end(self, point, connections=None):
        if point != None and not MazeGraph._ispoint(point)
            raise AttributeError("point should be (int, int)")
        self.add_node(point)
        self._end = point