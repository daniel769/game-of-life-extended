## Game of Life - using bit map 2d convolution

### Preface

I've chosen to share my implementation of [*Conway's Game of life*](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) since it is using a uniquely elegant of solution using image processing vectorized approach.

The idea is that any rule based application can be imposed as a combination of vectorized bitwise operators. This way we can avoid both "branch-style" and "element wise" computation schemes.

The main ideas are as followed:

- Any computation in Cell's world is fully vectorized
- 2D Convolution is used to generate neighbors counting "mask" for the Cell
- Each rule is a vectorized bitwise operator
- Rules set inhibits a composite logical operations between the rules

How a single iteration is applied:

```python
import scipy.signal
import numpy as np
def apply(live):
    cnt_kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    cnt = scipy.signal.convolve2d(live, cnt_kernel,
                                          mode='same', boundary='fill', fillvalue=0)

    l_under_pop = lambda live, cnt: ~(cnt < 2) & live
    l_surv      = lambda live, cnt: np.isin (cnt, [2,3]) & live
    l_overpop   = lambda live, cnt: ~(cnt > 3) & live
    l_repro     = lambda live, cnt: (cnt == 3) & ~live
    
    r1, r2, r3, r4 = l_under_pop(live, cnt), l_survival(live, cnt), l_overpop(live, cnt), l_repro(live, cnt)
    return (r1 & r2 & r3 ) | r4

```



### Rules of the Game (Original)

The original universe of the Game of Life is a two-dimensional orthogonal grid of square
cells, each of which is in one of two possible states, alive or dead. Every cell interacts
with its eight neighbors, which are the cells that are horizontally, vertically, or
diagonally adjacent.
At each step in time, the following transitions occur:

1. Any live cell with fewer than two live neighbors dies (under population).
2. Any live cell with two or three live neighbors lives on to the next generation.
3. Any live cell with more than three live neighbors dies (overpopulation).
4. Any dead cell with exactly three live neighbors becomes a live cell (reproduction).

The grid is initiated with a seed - an initial state of alive and dead cells, and continues
on to its next generation automatically. This process repeats itself indefinitely, or until a
predefined number of generations pass.


### Extended Rules - Infection

For fun, few more rules are added to simulate infection. After a predefined number of generations has reached, a virus is spread around the universe
infecting cells.
From now on the rules change, the new rules are:

1. Any dead cell with a single live neighbor lives on to the next generation.
2. Any live cell with no horizontal or vertical live neighbors dies.

### Input

The program accepts the following arguments:

| Argument  | Type | Description               |
|:----------: |:------:|:---------------------------:|
| width     | int  | The width of the world   |
|height | int | The height of the world |
|infect-after | int | The number of generations after which the infection stage will start |
|max-generations | int | The maximum number of generations that can be created. Including all phases of the game |
|seed [] | int | The initial state of the world |


#### Example

Way to pass the parameters is:

`program [width] [height] [ infect-after] [ max-generations] [seed]`

`$ your-program 2 3 3 6 "1 0 0 1 1 1"`

### Output
Each generation produces a flat output of the current state to stdout. The values
are separated by whitespace and followed by a newline character at the end.
The format for the output is:

 `<row 1> <row 2> <row 3> ... <row n>\n`

#### Example

With the current state being

```
0 0 0 
1 0 0 
1 0 1
```

the first 2 lines output to stdout will be

```
0 0 0 1 0 0 1 0 1
0 0 0 0 1 0 0 1 0
```
