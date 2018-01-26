from maze import Maze

# Main
if __name__ == '__main__':
    import sys
    maze = Maze(sys.argv[1])
    im = maze.to_img(solved=True)
    im.save(sys.argv[2])