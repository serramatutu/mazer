from maze import Maze

# Main
if __name__ == '__main__':
    import sys
    maze = Maze(sys.argv[1])
    print(maze)
    print()
    print('Graph:')
    graph = maze.solve()
    for node, edges in graph:
        print(str(node) + ' -> ' + str(edges))
    
    graph.to_image().save(fp='graph.png')