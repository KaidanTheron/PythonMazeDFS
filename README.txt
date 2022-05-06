- If you want to edit properties of maze generation you can change "widthMaze" property on line 35. 
- If you want to change generation/search speed you can change ppf: pause per frame on line 36.

Make sure to have Pygame installed on your device before you run the program, otherwise it won't work.

Run this baby in the terminal using "python maze.py" and watch it go. Btw, there are some cases with the generation algorithm where it reaches
its max recursion depth, and this tends to happen with "widthMaze" > 75. The recursion can also get to max depth on the
search with "widthMaze" > 50, but don't worry about it.

Once you run the script it will generate the maze. After the maze is generated you can press the enter key on your keyboard 
and it will solve the maze.