from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn import metrics
import pandas as pd
import numpy as np

test = pd.read_csv("test.csv")
train = pd.read_csv("train.csv")

train_label = pd.DataFrame(train.Activity)
train = train.drop(['Activity','subject'], axis=1)

test_label = pd.DataFrame(test.Activity)
test = test.drop(['Activity','subject'], axis=1)

encoder = preprocessing.LabelEncoder()
encoder.fit(train_label)
train_label = encoder.transform(train_label)
encoder.fit(test_label)
test_label = encoder.transform(test_label)


def n_estimator(n, m):

    clf=RandomForestClassifier(n_estimators=n, max_depth=m)
    clf.fit(train,train_label)
    y_pred = clf.predict(test)
    return metrics.accuracy_score(test_label, y_pred)


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
        self.matrix[root_n][root_m] = 'Q'

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


def search_best_accuracy(n_values, m_values, root_n, root_m, baseline):
    best_so_far = { 'pair': (), 'value': 0.0, 'optimal': False }
    queue = MatrixQueue(n_values, m_values)
    if queue.invalid() or baseline > 1: return best_so_far
    while not queue.empty():
        queue.print()
        row, column = queue.deque()
        n, m = n_values[row], m_values[column]
        estimated = n_estimator(n, m)
        current = { 'pair': (n, m), 'value': estimated, 'optimal': False }
        if estimated >= baseline:
            current['optimal'] = True
            return current
        elif estimated >= best_so_far['value']:
            best_so_far = current
        queue.enque_children(row, column)
        print('current', (row, column), current)
    return best_so_far

n_values = [10, 20, 30, 40, 50, 60, 70, 80, 90]
m_values = [10, 20, 23, 30, 40, 50, 60]
root_n = int(len(n_values) / 2)
root_m = int(len(m_values) / 2)
optimal_parameters = search_best_accuracy(n_values, m_values, root_n, root_m, 0.93)

print('The best parameters with the accuracy result: ', optimal_parameters)


# from graphviz import Graph, Digraph
# bfs_graph = Digraph('bfs', filename='bfs.gv', format='png',
#             node_attr={'color': 'lightblue2'}, engine='dot')
# bfs_graph.attr('node', shape='circle')

# all_pos = []
# for i in n:
#     for j in m:
#         all_pos.append('n={} / m={}'.format(i,j))

# for i in all_pos:
#     for j in all_pos:
#         if j != all_pos[0]:
#             bfs_graph.edge('%s'%i,'%s'%j)
#         elif i != all_pos[0]:
#             bfs_graph.edge('%s'%j,'%s'%i)

# bfs_graph.render('bfs_graph.gv', view=True)
