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
    
    
class ImageMazeMatrixCol:
    def __init__(self, threshold, data, stride, col_index):
        self._threshold = threshold
        self._col_index = col_index
        self._stride = stride
        self._data = data
        
    def __getitem__(self, index):
        return self._data[index * self._stride + self._col_index] > self._threshold
    
    def __len__(self):
        return self._stride
    
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
        return ImageMazeMatrixCol(self.threshold, self._data, self._width, line)
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
        