'''
Assignment 5
Nithin Krishna Gowda
Advanced Data Structures
Application of Ford Fulkerson Algorithm
The program can be executed in the terminal with the command:    

cat inSample1.txt | python3 assignment5.py
'''
# Steps needed to be implemented:
# Based on the input set of dimensions of boxes, building the bipartiate graph out of them
    # implementation of rotation of the boxes and checking if one box can fit inside another
    # converting the strings in each line into numbers and storing them in a list
    # Guardian code:
        # check if there are only three numbers
        # use isdigit() to check if all the numbers in each line are a list
        
# Once the Bipartiate graph has been generated, creating a adjacency matrix out of it. 
# The adjacency matrix needs to be a DAG
# After adjacency matrix, building a ford fulkerson algorithm out of it

'''
cat inSample1.txt | python3 asst5.py
creating a pipeline in linux
The output of inSample1.txt is fed as the input to the python file asst5.py
This input be read using the command sys.stdin.readlines() which is stored in data
'''
import sys
data =  sys.stdin.readlines()
#print("counted", len(data), "lines")
n_boxes =  int(data[0])
box_dim = []
for line in data:
    line = line.strip()
    #line = line.replace(" ", "") 
    #print(line.isdigit())
    # if not line.isdigit():
    #     print("each line should contain only integers", line)
    #     print("exiting the for loop and the program")
    #     break

    
    box_dim.append(line)


box_dim.pop(0)

print("The original box dimensions in the form of a list are",box_dim)

# stored the dimensions of all the boxes in a list
# Need to write a function to rearrange the dimensions of each box in ascending order

# function returns a list of numbers from a string separated by spaces
def numbers_from_spaces(dim_string):
    l_nums = []
    num = ''
    for i in dim_string:
        if i == ' ':
            l_nums.append(num)
            num = ''
        else:
            num += i
    l_nums.append(num)   
    return l_nums

#ans1 = numbers_from_spaces("11 13 6")
#print(ans1)

# Function to create a single string separated by spaces from a list
def list_to_string(one_box_dim: list):
    string_dim = ""
    for i in one_box_dim:
        string_dim += i
        string_dim += ' '
    string_dim = string_dim[0 : (len(string_dim)-1) ]
    return string_dim

#ans2 = list_to_string(["11", "13", "6"])
#print(ans2)
    

def rearrange(l_dim):
    for i in range( len(l_dim)):
        l_dim[i] = numbers_from_spaces(l_dim[i])
        l_dim[i] = [int(num_string) for num_string in l_dim[i]]
        l_dim[i].sort()
        l_dim[i] = [str(num) for num in l_dim[i]]
        l_dim[i] = list_to_string(l_dim[i])    
    return l_dim

#print(rearrange(box_dim))




# Need to create a adjacency matrix out of all the boxes in the list and their dimensions
# input is a list and output is an adjacency matrix(list of lists)
# compare each box with the rest of the boxes dimensions and see if each digit is less than the other

def adj_matrix(l_dim : list, n_boxes: int):
    #print("l_dim", l_dim)
    # This was super hard to figure it out. I should be really careful while creating 2D matrices in python
    matrix = [[0 for i in range(n_boxes)] for i in range(n_boxes)]
    #print(matrix)
    #check if one box is less than the other
    true_count = 0
    false_count = 0
    for i in range(0, n_boxes):
        for j in range(0, n_boxes):
            #print("indexes", i, j)
            b_main_list = numbers_from_spaces(l_dim[i])
            b_rest_list = numbers_from_spaces(l_dim[j])
            flag = False
            # extracting numbers from spaces
            for n,m in zip(b_main_list, b_rest_list):
                #print(n,m)
                if int(n) < int(m):
                    flag = True
                else:
                    flag = False
                    break
            #print("flag_status", flag)
            
            if flag:
                #print("The value of index at", i, j,"is", 1)
                #print('###')
                matrix[i][j] = 1
                #print(matrix)
                true_count +=1
            
            if not flag:
                #print('###')
                matrix[i][j] = 0
                false_count +=1
    
    #print("true count", true_count)
    #print("false count", false_count)
    #print(matrix)

    return matrix

s_dim = rearrange(box_dim)
print("The box dimensions sorted and arranged in the form of a list are", s_dim)
#print(box_dim)

f_matrix = adj_matrix(s_dim, n_boxes)
print("The adjacency matrix for the boxes are:")
for i in range(len(f_matrix)):
    print(f_matrix[i])


# the f_matrix represents the finished matrix 
# A 1 at index i, j represents that box[i] < box[j] or box[i] fits in box[j]

# Now need to implement Bipartite matching:
class bipartite_matching():
    def __init__(self, graph):
        self.graph = graph
        self.n_boxes = len(graph)
        #print(graph)
    
    # recursive DFS
    # returns true if box u can be put inside another box
    def _bpm(self, u, inside, matched_boxes):

        for v in range(self.n_boxes):
            # print(v, "box no" )
            # print(u, "u box no")
            # print(matched_boxes)
            # print(self.graph[0][1])
        
            # if box u fits inside box v and that has not been checked
            if self.graph[u][v] and matched_boxes[v] == False:
                matched_boxes[v] = True
                
            
                if inside[v] == -1 or self._bpm(inside[v], inside, matched_boxes):
                    inside[v] = u
                    return True
        return False


    def max_bpm(self):
        # an array to keep track if a box is inside another box
        #  the value of inside[i] is box inside i
        # eg: if inside[3] = 2, then box 2 fits inside box 3 

        inside = [-1] * self.n_boxes
        box_in_box = 0
        for i in range(self.n_boxes):

            # marking all boxes as not matched
            matched_boxes = [False] * self.n_boxes

            # if a box can fit in another box
            if self._bpm(i, inside, matched_boxes):
                box_in_box +=1
            
        return self.n_boxes - box_in_box

    

bpm_object = bipartite_matching(f_matrix)

print("The number of visbible boxes is", bpm_object.max_bpm())
