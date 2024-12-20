# Advent of Code 2024

I am very pleased that this year there is another wagon of problems to solve

## Inspirations

I am not that good coder so i often inspire in better one's work

As i am curious about python there are some authors who published their python work:

- [Peter Cullen Burbery](https://github.com/PeterCullenBurbery/advent-of-code-002/tree/420dc67bf433fb11c1ada8f331d7f0b4587c3ef9/jupyter-notebook-python/2024)
- [BarrensZeppelin 2023 so far](https://github.com/BarrensZeppelin/adventofcode2023)
- [JonathanPaulson full 2024](https://github.com/jonathanpaulson/AdventOfCode/tree/master/2024)

## Interesting lessons learned

- [Day 16](day%2016.py)
  - how to work with priority queue [heapq](https://docs.python.org/3/library/heapq.html) in python - super useful for path finding problems
  - Instead of recursion i have used loop
- [Day 17](day%2017.py)
  - nice example of FSM (Finite state machine) - like real computer!
  - I have also tried brute force process, but `10^14` is way too much to try
  - Quite interesting was that there were 6 different solutions
  - Part 2 was quite challenging until i have created the program process
```python
b = a % 8
b = b ^ 1
c = math.floor(a / (2**b))
b = b ^ 5
b = b ^ c
out = b % 8
a = math.floor(a/2**3)
```
- [Day 18](day%2018.py)
  - Another maze movement
  - just another search of shortest path - so again i have tried priority queue solution
  - quite interesting I had to implement a duplicit entries protection otherwise it did not finish in timely manner
- [Day 19](day%2019.py)
  - very nice example of recursion, i tried stack based solution, but there are so many same queries that it does not end in time
  - after change to recursion solution a adapt to cache results it finished in seconds
- [Day 20](day%20.py)
  - yet another walking map problem
  - i have a real struggle with this one part 2 and i have taken inspiration from [HyperNeutrino](https://www.youtube.com/watch?v=tWhwcORztSY)
    - the idea is that important is **the starting point** and **the ending point** (not the path anymore) So we iterate through the distance (1-20) and 
    divide it to the x and y coordinate
    - i look at the difference of distance map, so no duplicates
    - surprisingly it is really fast!
  - As there is always a step of 1 priority q (heapq) is not needed and deque would be sufficient



Now it is obvious that variable a is only from range `[a_desired * 8, a_desired * 8 + 8]`
