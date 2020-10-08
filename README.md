# CSC74010 Artificial Intelligence Homework

## Requirements

- python 3
- pip

Run:

```sh
pip install -r requirements.txt
```

## The Code

Run:

```sh
python bfs.py
```

Output:

```python
  +---------------+
8 | . . . . . . . |
7 | . . . . . . . |
6 | . . . . . . . |
5 | . . . . . . . |
4 | . . . Q . . . |
3 | . . . . . . . |
2 | . . . . . . . |
1 | . . . . . . . |
0 | . . . . . . . |
  +---------------+
    0 1 2 3 4 5 6  
actually_inserted [(4, 2), (4, 4), (3, 3), (5, 3)]
current (4, 3) {'pair': (50, 30), 'value': 0.9246691550729556, 'optimal': False}

.
.
.

  +---------------+
8 | . . . . . . . |
7 | . . . Q . . . |
6 | . Q Q V Q . . |
5 | Q V V V V Q . |
4 | V V V V V V Q |
3 | Q V V V V Q . |
2 | . Q V V Q . . |
1 | . . Q Q . . . |
0 | . . . . . . . |
  +---------------+
    0 1 2 3 4 5 6  
The best parameters with the accuracy result:  {'pair': (70, 23), 'value': 0.9314557176789956, 'optimal': True}
```
