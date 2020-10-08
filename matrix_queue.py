def get_children(x, y, n, m):

    children = []
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        cx, cy = (x + dx), (y + dy)
        if 0 <= cx and cx < n and 0 <= cy and cy < m:
            children.append((cx, cy))
    return children


def mprint(content):
    rows = len(content)
    cols = len(content[0])
    width       = len(str(max(rows,cols)-1))
    contentLine = "# | values |"

    dashes      = "-".join("-"*width for _ in range(cols))
    frameLine   = contentLine.replace("values",dashes)
    frameLine   = frameLine.replace("#"," "*width)
    frameLine   = frameLine.replace("| ","+-").replace(" |","-+")

    print(frameLine)
    for i,row in enumerate(reversed(content),1):
        values = " ".join(str(v) for v in row)
        line   = contentLine.replace("values",values)
        line   = line.replace("#",f"{rows-i:{width}d}")
        print(line)
    print(frameLine)

    numLine = contentLine.replace("|"," ")
    numLine = numLine.replace("#"," "*width)
    colNums = " ".join(f"{i:<{width}d}" for i in range(cols))
    numLine = numLine.replace("values",colNums)
    print(numLine)


def build_matrix(n, m, v):
    """
    >>> build_matrix(3, 3, '.')
    [[False, False, False], [False, False, False], [False, False, False]]
    """
    grid = []
    for i in range(0, n):
        grid.append([v for item in range(0, m)])
    return grid


class MatrixQueue:
    def __init__(self, n_values, m_values):
        self.rows, self.columns = len(n_values), len(m_values)
        root_row = int(self.rows / 2)
        root_column = int(self.columns / 2)
        self.queue = [(root_row, root_column)]
        self.matrix = build_matrix(self.rows, self.columns, '.')
        self.matrix[root_row][root_column] = 'Q'

    def enque(self, row, column):
        if self.matrix[row][column] == '.':
            self.matrix[row][column] = 'Q'
            self.queue.append((row, column))
            return True
        return False

    def enque_children(self, row, column):
        children = get_children(row, column, self.rows, self.columns)
        actually_inserted = []
        for cx, cy in children:
            if self.enque(cx, cy): actually_inserted.append((cx, cy))
        print('actually_inserted', actually_inserted)

    def deque(self):
        row, column = self.queue.pop(0)
        self.matrix[row][column] = 'V'
        return (row, column)

    def empty(self):
        return not (len(self.queue) > 0)

    def print(self):
        mprint(self.matrix)

    def invalid(self):
        return not (self.rows > 0 and self.columns > 0)
