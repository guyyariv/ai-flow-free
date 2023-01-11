# AI Flow Free

Description:  
Our project focuses on solving the popular game
“Free Flow”.
If you are not familiar with this game you are welcome to try it
out here.
Our aim was to use AI techniques to quickly and automatically
determine the best plays to make in order to win the game.
We concentrate our solution on two key strategies: first, employing
search algorithms to solve the board, and second,
reinforcement learning.
Our program is fully accessible


## Running Instructions

1. Clone this repo
2. Activate virtual env
3. Install requirements
```angular2html
pip install -r requirements.txt
```
4. Run main.py
Optional parameters:  
--a -> Choose algorithm.   
options:  
q - Q Learning
bfs - BFS  
dfs - DFS  
ucs - UCS  
man - A star Manhattan  
maze - A star Maze
(default=q)  
--s -> Board size (default=5)  
--l -> Level (default=easy)   

For example:
```angular2html
python main.py --a='maze' --l='hard'
```
