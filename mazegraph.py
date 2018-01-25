import operator

# _MazeGraphNode class
class _MazeGraphNode:
    @staticmethod
    def _ispoint(p):
        return (isinstance(p, (tuple, list)) and 
                isinstance(p[0], int) and isinstance(p[1], int))
    
    def __init__(self, point, connections=None):
        self.point = point;
        
        if connections != None:
            if not isinstance(connections, list):
                raise AttributeError("connections must be list of points")
            for p in connections:
                if not _MazeGraphNode._ispoint(p):
                    raise AttributeError("connections must be list of points")
            self._connections = connections
        else:
            self._connections = [];
        
    point = property(operator.attrgetter('_point'))
    
    @point.setter
    def point(self, point):
        if not _MazeGraphNode._ispoint(point):
            raise AttributeError("point must be (int, int)")
        self._point = point;
    
    def add_connection(self, point):
        if point == None or not _MazeGraphNode._ispoint(point):
            raise AttributeError("point must be (int, int)")
        self._connections.append(point)
        
    def remove_connection(self, point):
        if point in self._connections:
            self._connections.remove(point)
            
    @property
    def connection_count(self):
        return len(self._connections)

# MazeGraph class
class MazeGraph:
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end
        
    # Getters e setters
    
    @property
    def start(self):
        return self._start.point
    
    @start.setter
    def start(self, point, connections=None):
        self._start = _MazeGraphNode(point, connections)
    
    @property
    def end(self):
        return self._end.point
    
    @end.setter
    def end(self, point, connections=None):
        self._end = _MazeGraphNode(point, connections)