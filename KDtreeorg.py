import math
class node:
    def __init__(self, cords=None, val=None):
        self.left = None
        self.right = None
        self.val = val
        self.cordinates = cords


class KDTree:

    def __init__(self, k=1):
        self.k = k
        self.root = node()

    def createTree(self, data,val):
        for i in range(len(data)):
            self.insert(data[i],val[i])

    def insert(self, cords, val=None):
        if self.root.cordinates == None:
            self.root = node(cords, val)
            return
        else:
            curr_node = self.root
            curr_d = 0
            while curr_node:
                curr_d = curr_d % self.k
                next_node = curr_node.left if cords[curr_d] < curr_node.cordinates[curr_d] else curr_node.right
                # age next node peyda nashe yani be barg residim
                if not next_node:
                    break
                # age next node peyda she be search edame midim
                curr_node = next_node
                curr_d += 1
            # Insert the new point as a left or right child node of the correct leaf node
            if cords[curr_d] < curr_node.cordinates[curr_d]:
                curr_node.left = node(cords, val)
            else:
                curr_node.right = node(cords, val)

            return

    # Function to copy the values of one point to another
    def copyPoint(self, p1, p2):
        for i in range(self.k):
            p1.cordinates[i] = p2.cordinates[i]
        p1.val=p2.val


    # Function to find the node with the minimum value in a subtree
    def minValueNode(self, given):
        current_node = given
        # Go to the leftmost leaf node in the subtree
        while current_node.left:
            current_node = current_node.left
        return current_node

    def deleteNodeRec(self, root, cords, depth):
        # If the tree is empty or the node is not found, return None
        if not root:
            return None

        # Calculate the current dimension based on the depth
        current_depth = depth % self.k
        # If the point to be deleted is smaller than the current node's point in the current dimension, go to the left subtree
        if cords[current_depth] < root.cordinates[current_depth]:
            root.left = self.deleteNodeRec(root.left, cords, depth + 1)
        # If the point to be deleted is larger than the current node's point in the current dimension, go to the right subtree
        elif cords[current_depth] > root.cordinates[current_depth]:
            root.right = self.deleteNodeRec(root.right, cords, depth + 1)
        # If the point to be deleted is equal to the current node's point, delete the node

        else:
            # If the node has no left child, return its right child
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            else:
                temp = self.minValueNode(root.right)
                self.copyPoint(root, temp)
                root.right = self.deleteNodeRec(root.right, temp.cordinates, depth + 1)
        return root

    def deleteNode(self, root, cords):
        return self.deleteNodeRec(self.root, cords, 0)

    def pointExists(self, cords):
        curr_node = self.root
        curr_d = 0
        if curr_node.cordinates == cords:
            return True

        while curr_node:
            if curr_node.cordinates == cords:
                return True
            curr_d = curr_d % self.k
            next_node = curr_node.left if cords[curr_d] < curr_node.cordinates[curr_d] else curr_node.right
            # age next node peyda nashe yani be barg residim
            if not next_node:
                return False

            # age next node peyda she be search edame midim
            curr_node = next_node
            curr_d += 1

    # cords cords = dis
    def distance(self, point1, point2):
        summ = 0
        diff=[]

        for i in range(len(point1)):
            diff.append(point1[i] - point2[i])

        for i in diff:
            summ+=i**2

        return math.sqrt(summ)

    # cords node node = node
    def closer_distance(self, pivot, p1, p2):
        if p1  is None:
            return p2

        if p2 is None:
            return p1

        d1 = self.distance(pivot, p1.cordinates)
        d2 = self.distance(pivot, p2.cordinates)

        if d1 < d2:
            return p1
        else:
            return p2

    # node cords
    def closest_point(self, root, point, depth=0):
        if root is None:
            return None

        axis = depth % self.k

        next_branch = None
        opposite_branch = None

        if point[axis] < root.cordinates[axis]:
            next_branch = root.left
            opposite_branch = root.right
        else:
            next_branch = root.right
            opposite_branch = root.left

        best = self.closer_distance(point,
                                    self.closest_point(next_branch, point, depth + 1),
                                    root)

        if self.distance(point, best.cordinates) > (point[axis] - root.cordinates[axis])**2:
            best = self.closer_distance(point,
                                        self.closest_point(opposite_branch, point , depth + 1),
                                        best)

        return best

    #
    def findMNearest(self,root_second,point,second_tree,k):
        MNN = []
        for i in range(k):
            temp= node()
            temp.cordinates=second_tree.closest_point(root_second,point).cordinates
            temp.val = second_tree.closest_point(root_second, point).val
            MNN.append(temp)
            second_tree.deleteNode(root_second,
                                   second_tree.closest_point(root_second,point).cordinates)
        return MNN


    def searchRange_help(self,max,min,root,depth=0):
        depth=depth%self.k
        if root==None: return None

        if (root.cordinates[depth]<=max and root.cordinates[depth]>=min):
           return root
        if not root.left==None :
             return self.searchRange_help(max,min,root.left,depth+1)
        if not root.right == None:
            return self.searchRange_help( max, min, root.right, depth + 1)

    def searchRange(self,max,min,root):
        nodes=[]
        for i in range(len(max)):
            nodes.append(self.searchRange_help(max[i],min[i],root))
        nodes.remove(None)

        for i in range(len(nodes)):
            nodes[i]=nodes[i].cordinates

        # result = set(nodes)
        # for s in nodes[1:]:
        #     result.intersection_update(s)

        return nodes
