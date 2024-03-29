# Visualizing and Debugging Advent of Code (AoC) Day 12 and 17 

This repo demonstrates some ideas for using pictures/visualizations for helping
understanding what's going on in two of the problems from
[AoC 2022](https://adventofcode.com/2022).

Exploring the idea of using visualizations to
help debugging and understanding what's going on under the hood.

The
[original post](https://seeinglogic.com/posts/seeing-advent-of-code/)
goes into more detail on the thought process and iterations.

## Day 12: a hill-climbing problem

Shows how having a nice visualization up your sleeve can help you see your own
mistakes.

Show what's reachable from the current algorithm (for troubleshooting):

![Reachability graphic](./images/day12/d3_wrong_with_letters.png)

Show the solution once you get it right:

![Shortest_path](./images/day12/d3_right_with_letters.png)

## Day 17: Tetris simulator

Can we just use a good picture to see repeating intervals? Yes!

![Graphing x-position and height by blocktype](./images/day17/10k.png)

This knowledge allows us to quickly calculate states arbitrarily
far in the future (which is what is required for this problem).
