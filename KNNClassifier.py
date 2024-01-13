from KDtreeorg import *
class KNN:
    def __init__(self,data,label,k):
        self.data=data
        self.tree= KDTree(len(data[0]))
        self.tree.createTree(data,label)
        self.k=k

    def classify(self,point):
        temp_tree=self.tree
        neighbors_list=temp_tree.findMNearest(temp_tree.root,point,temp_tree,self.k)

        #label noqte ha vared in mishe
        labels=[]
        for i in neighbors_list:
            labels.append(i.val)

        #tedad label az 0 ta 9 moshakhas mishe [x][0]=tedad [x][1]=shomare label
        counted_labels=[]
        for i in range(10):
            counted_labels.append([labels.count([i]), i])

        sorted_labes=sorted(counted_labels,reverse=True)
        return (sorted_labes[0])

    def classifyAll(self,points):
        labels=[]
        for i in (points):
            labels.append(self.classify(i)[1])
        return labels

    def accuracy(self,predicted,true):
        count=0
        for i in range(len(predicted)):
            if(predicted[i]==true[i][0]): count+=1

        percent=(count/len(predicted)) * 100
        return percent






