from abc import ABC, abstractmethod, abstractproperty
from PIL import Image


class IMazeMatrix(ABC):
    @abstractmethod
    def __getitem__(self, line):
        pass
    
    @abstractproperty
    def width(self):
        pass
    
    @abstractproperty
    def height(self):
        pass
    
    
    
class ListMazeMatrix(IMazeMatrix):
    def __init__(self, l):
        if not isinstance(l, list) and not all(isinstance(x, list) for x in l):
            raise ValueError("l must be list")
        self._data = l
        
    def __getitem__(self, line):
        return self._data[line]
    
    @property
    def width(self):
        return len(self._data[0])
    
    @property
    def height(self):
        return len(self._data)
    
    
    
class ImageMazeMatrix(IMazeMatrix):
    def __init__(self, img, threshold = (127, 127, 127)):
        if not isinstance(img, Image.Image):
            if not isinstance(img, str):
                raise ValueError("img must be string or Image")
            img = Image.open(img)
            
        self.threshold = threshold
        self._width = img.width
        self._height = img.height
        self._data = img.convert('RGB').getdata()
        
        
    def __getitem__(self, line):
        l = list()
        for i in range(0, self.width):
            l.append(self._data[i * self.width + line] > self.threshold)
            
        return l
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
        