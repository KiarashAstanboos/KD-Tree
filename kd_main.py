import csv
from KNNClassifier import *
from Table import *
with open('test.txt', 'r') as f:
    table_data = [line.strip() for line in f]

for i in range(len(table_data)):
    table_data[i]=table_data[i].split(', ')

table_data_cords =[[int(int(j)) for j in i] for i in table_data[1:]] #tabdile list az string be int

table_tree=Table(table_data_cords,table_data[0])
print(table_tree.Search([30,3100,14],[25,3050,8]))


with open('train.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
data = [[int(int(j)) for j in i] for i in data] #tabdile list az string be int

with open('train_labels.csv', newline='') as f:
    reader = csv.reader(f)
    data_label= list(reader)
data_label = [[int(int(j)) for j in i] for i in data_label] #tabdile list az string be int


with open('test.csv', newline='') as f:
    reader = csv.reader(f)
    test_points = list(reader)
test_points = [[int(int(j)) for j in i] for i in  test_points] #tabdile list az string be int


with open('test_labels.csv', newline='') as f:
    reader = csv.reader(f)
    test_labels = list(reader)
test_labels = [[int(int(j)) for j in i] for i in test_labels] #tabdile list az string be int

tree=KNN(data,data_label,5)
# print(tree.classify(test_points[3])[1])
predicted=tree.classifyAll(test_points)
print(predicted)
print(tree.accuracy(predicted,test_labels))




