from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn import metrics
import pandas as pd
import numpy as np
from matrix_queue import MatrixQueue

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


def bfs_accuracy(n_values, m_values, baseline):
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

# n_values=[30,40,50]
# m_values = [10,20,30]

# n_values = [100,40,50,60]
# m_values = [20,30,23,12]

optimal_parameters = bfs_accuracy(n_values, m_values, 0.93)

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
