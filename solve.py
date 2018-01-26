from maze import Maze
from PIL import Image

# Main
if __name__ == '__main__':
    import sys     
    
    maze = Maze(sys.argv[1])
    print('conversion done.')
    im = maze.to_img(solved=True)
    im.save(sys.argv[2])