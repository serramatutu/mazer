# mazer
Simple and quick project for solving mazes in Python 3. This is my first contact with Python so don't mind my code :D

---
The solver implements the following algorithm:
1. Read once through the image, transforming it into a graph
2. From all "lonely" nodes (neighbours=1), reduce the graph until a connection to another path is found
3. Simplify the graph removing nodes in the middle of a line
4. Return the graph. It will be the solution to the maze

The graph can then be used to export another image, with the solution to the maze

I intend on making a maze generator out of this as well.
