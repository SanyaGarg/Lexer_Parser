import copy
import random

class game:

    def __init__(self):
        self.matrix = []
        self.commands = ['L','R','U','D']
        self.operations = ['ADD','SUBTRACT','MULTIPLY','DIVIDE']
        self.history = []
        self.sum = 0
        self.tiles = {}
        #self.prev = [self.matrix,0]

    def generate_grid(self,n):
        matrix = self.matrix
        tiles = self.tiles

        for i in range(0,n):
            matrix.append([0]*n)
        
        for i in range(0,n):
            for j in range(0,n):
                tiles[(i,j)] = []
        
        self.generate_number()
        self.generate_number()
        new_matrix = copy.deepcopy(matrix)
        x = self.sum
        self.history.append((new_matrix,x))
        
    def assignment(self,val,x,y):
        matrix = self.matrix
        matrix[x][y] = val
        self.print_matrix(matrix)
        return True

    def naming(self,var,x,y):
        tiles = self.tiles
        tiles[(x,y)].append(var)
        print(tiles[(x,y)])
        return True

    def get_val(self,x,y):
        matrix = self.matrix
        return matrix[x][y]

    def switch_naming(self,i,j):
        m = self.matrix
        tiles = self.tiles
        m[i][j] = 0
        if(len(tiles[(i,j)])>0):
            tiles[(i,j)].pop()       

    def generate_number(self):
        pick = [2,4]
        matrix = self.matrix
        n = len(matrix)
        a = random.randint(0,n-1)
        b = random.randint(0,n-1)

        while matrix[a][b]!= 0:
            a = random.randint(0,n-1)
            b = random.randint(0,n-1)
        
        matrix[a][b] = random.choice(pick)
        self.sum += matrix[a][b]
        return True
    
    def print_matrix(self,matrix):
        n = len(matrix)
        for i in range(0,n):
            print(matrix[i])                

    def mov(self,op,direction):
        if direction == 'LEFT':
            self.left(op)
        elif direction == 'RIGHT':
            self.right(op)
        elif direction == 'UP':
            self.Up(op)
        elif direction == 'DOWN':
            self.Down(op)

    def operator(self,matrix,i,j,op,var):
        tiles = self.tiles

        if op == 'ADD':
            self.add(matrix,i,j,var)
        elif op == 'SUBTRACT':
            self.subtract(matrix,i,j)
            if(len(tiles[(i,j)])>0):
                tiles[(i,j)].pop()
        elif op == 'MULTIPLY':
            self.multiply(matrix,i,j,var)
        elif op == 'DIVIDE':
            self.divide(matrix,i,j,var)   

    def add(self,matrix,i,j,var):
        matrix[i][j]*= 2
        tiles = self.tiles
        for name in var:
            tiles[(i,j)].append(name)       

    def subtract(self,matrix,i,j):
        matrix[i][j] = 0

    def divide(self,matrix,i,j,var):
        matrix[i][j] = 1
        tiles = self.tiles
        for name in var:
            tiles[(i,j)].append(name)

    def multiply(self,matrix,i,j,var):
        matrix[i][j]*= matrix[i][j]
        tiles = self.tiles
        for name in var:
            tiles[(i,j)].append(name)

    def left(self,op): 
        m = self.matrix
        tiles = self.tiles
        n = len(m)

        for i in range(0,n):
            count = 0
            for j in range(0,n):
                if (m[i][j]!=0):
                    m[i][count],m[i][j] = m[i][j],m[i][count]
                    var = copy.deepcopy(tiles[(i,j)])
                    for name in var:
                        tiles[(i,count)].append(name)
                    if(len(tiles[(i,j)])>0):
                        tiles[(i,j)].pop()
                    count+=1

        for i in range(0,n):
            for j in range(0,n-1):
                if m[i][j]!=0 and m[i][j]==m[i][j+1]:
                    floor = copy.deepcopy(tiles[(i,j+1)])
                    self.operator(m,i,j,op,floor)    
                    self.switch_naming(i,j+1)

        for i in range(0,n):
            count = 0
            for j in range(0,n):
                if (m[i][j]!=0):
                    m[i][count],m[i][j] = m[i][j],m[i][count]
                    var = copy.deepcopy(tiles[(i,j)])
                    for name in var:
                        tiles[(i,count)].append(name)
                    if(len(tiles[(i,j)])>0):
                        tiles[(i,j)].pop()
                    count+=1  
 
        self.generate_number()
        new_matrix = []
        new_matrix = copy.deepcopy(self.matrix)  
        x = copy.deepcopy(self.sum)

        self.history.append((new_matrix,x)) 
        self.print_matrix(new_matrix)
        #self.prev = [new_matrix,x]
        return True 

    def right(self,op): 
        m = self.matrix
        tiles = self.tiles
        n = len(m)

        for i in range(0,n):
            count = 0
            for j in range(0,n):
                if (m[i][n-1-j]!=0):
                    m[i][n-1-j],m[i][n-1-count] = m[i][n-1-count],m[i][n-1-j]
                    var = copy.deepcopy(tiles[(i,n-1-j)])
                    for name in var:
                        tiles[(i,n-1-count)].append(name)
                    if(len(tiles[(i,n-1-j)])>0):
                        tiles[(i,n-1-j)].pop()
                    count+=1

        for i in range(0,n):
            for j in range(3,-1,-1):
                if m[i][j]!=0 and m[i][j]==m[i][j-1]:
                    floor = copy.deepcopy(tiles[(i,j-1)])
                    self.operator(m,i,j,op,floor)     #check
                    self.switch_naming(i,j-1)

        for i in range(0,n):
            count = 0
            for j in range(0,n):
                if (m[i][n-1-j]!=0):
                    m[i][n-1-j],m[i][n-1-count] = m[i][n-1-count],m[i][n-1-j]
                    var = copy.deepcopy(tiles[(i,n-1-j)])
                    for name in var:
                        tiles[(i,n-1-count)].append(name)
                    if(len(tiles[(i,n-1-j)])>0):
                        tiles[(i,n-1-j)].pop()
                    count+=1 

        self.generate_number()
        new_matrix = []
        new_matrix = copy.deepcopy(self.matrix) 
        x = copy.deepcopy(self.sum)

        self.history.append((new_matrix,x))  
        self.print_matrix(new_matrix)
        return True       

    def Up(self,op):
        m = self.matrix
        tiles = self.tiles
        n = len(m)
        for i in range(0,n):
            count = 0
            for j in range(0,n):
                if m[j][i]!=0:
                    m[j][i],m[count][i] = m[count][i],m[j][i]
                    var = copy.deepcopy(tiles[(j,i)])
                    for name in var:
                        tiles[(count,i)].append(name)
                    if(len(tiles[(j,i)])>0):
                        tiles[(j,i)].pop()
                    count +=1

        for i in range(0,n):
            for j in range(0,n-1):
                if m[j][i]!=0 and m[j][i] == m[j+1][i]:
                    floor = copy.deepcopy(tiles[(j+1,i)])
                    self.operator(m,j,i,op,floor)     #check   
                    self.switch_naming(j+1,i)

        for i in range(0,n):
            count = 0
            for j in range(0,n): 
                if m[j][i]!=0:
                    m[j][i],m[count][i] = m[count][i],m[j][i]               
                    var = copy.deepcopy(tiles[(j,i)])
                    for name in var:
                        tiles[(count,i)].append(name)
                    if(len(tiles[(j,i)])>0):
                        tiles[(j,i)].pop()
                    count+=1

        self.generate_number()
        new_matrix = []
        new_matrix = copy.deepcopy(self.matrix)  
        x = copy.deepcopy(self.sum)

        self.history.append((new_matrix,x))  
        self.print_matrix(new_matrix)
        return True

    def Down(self,op):
        m = self.matrix
        tiles = self.tiles

        n = len(m)
        for i in range(0,n):
            count = 0
            for j in range(0,n):
                if (m[n-1-j][i]!=0):
                    m[n-1-j][i],m[n-1-count][i] = m[n-1-count][i],m[n-1-j][i] 
                    var = copy.deepcopy(tiles[(n-1-j,i)])
                    for name in var:
                        tiles[(n-1-count,i)].append(name)
                    if(len(tiles[(n-1-j,i)])>0):
                        tiles[(n-1-j,i)].pop()
                    count+=1 

        for i in range(0,n):
            count = 0
            for j in range(n-1,-1,-1):
                if m[j][i]!=0 and m[j][i] == m[j-1][i]:
                    floor = copy.deepcopy(tiles[(j-1,i)])
                    self.operator(m,j,i,op,floor)     #check  
                    self.switch_naming(j-1,i)

        for i in range(0,n):
            count = 0
            for j in range(0,n):
                if (m[n-1-j][i]!=0):
                    m[n-1-j][i],m[n-1-count][i] = m[n-1-count][i],m[n-1-j][i] 
                    var = copy.deepcopy(tiles[(n-1-j,i)])
                    for name in var:
                        tiles[(n-1-count,i)].append(name)
                    if(len(tiles[(n-1-j,i)])>0):
                        tiles[(n-1-j,i)].pop()
                    count+=1 
        
        self.generate_number()
        new_matrix = []
        new_matrix = copy.deepcopy(self.matrix)  
        x = copy.deepcopy(self.sum)

        self.history.append((new_matrix,x)) 
        self.print_matrix(new_matrix)
        return True

    def getMatrix(self):
        return self.matrix

    def simulate(self,n):
        while(self.sum!=n):
            move = random.choice(self.commands)
            op = random.choice(self.operations)

            if move == 'U':
                print("Move Up:")
                self.Up(op)
                print("Sum:")
                print(self.sum) 
            elif move == 'D':
                print("Move Down:")
                self.Down(op)
                print("Sum:")
                print(self.sum) 
            elif move == 'R':
                print("Move Right:")
                self.right()
                print("Sum:")
                print(self.sum) 
            elif move == 'L':
                print("Move Left:")
                self.left(op)
                print("Sum:")
                print(self.sum) 
            #print(self.history)

            if (self.sum)>n:
                self.history.pop()
                self.matrix,self.sum = (self.history.pop())
                self.print_matrix(self.matrix)
                print("Sum:")
                print(self.sum) 

                new_matrix = copy.deepcopy(self.matrix)
                x = copy.deepcopy(self.sum)
                self.history.append((new_matrix,x)) 
                # print("newMatrix:",self.matrix)
                # print("NewSum:",self.sum)
        
        pass




