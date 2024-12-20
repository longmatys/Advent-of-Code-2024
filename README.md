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

Now it is obvious that variable a is only from range `[a_desired * 8, a_desired * 8 + 8]`
