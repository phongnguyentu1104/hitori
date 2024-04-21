from timeit import default_timer
from inspect import stack
import os
import psutil

class HitoriPuzzleSolover:
    def __init__(self, array: list, level: int):
        self.begin_array = array
        self.array = array
        self.level = level
        self.log = []
        self.latest = array
        
    def print_array(self, array, step=-1):
        if step == 0:
            print('-----Init-----')
        elif step == -1:
            if array:
                print('------Result-----')
            else:
                print('=====Can not Solve=====')
                return
        else:
            print('-----Step '+str(step)+'-----')
        for row in array:
            for e in row:
                print(e, end='  ')
            print()
    
    def print_log(self):
        # In ra lịch sử các bước giải quyết
        for i, v in enumerate(self.log[::-1]):
            self.print_array(v, i)
        self.print_array(self.array)

    def copy_array(self, array):
        return [row.copy() for row in array]

    def solve(self):
        self.array = self.explore_and_fill(self.array)

    def explore_and_fill(self, array, row=0, col=0, step=0):
        # tìm kiếm và điền giá trị vào ma trận
        if array != self.latest:
            self.print_array(array, step)
            self.latest = array

        if row == self.level:
            self.log.append(array)
            return array

        t_array = self.copy_array(array)
        
        if t_array[row][col] != 'x' and self.is_not_good_position(t_array, row, col) and self.is_valid_move(t_array, row, col, t_array[row][col], True):
            stacks.append((row, col, step))
        
        if t_array[row][col] != 'x' and not self.is_not_good_position(t_array, row, col) and self.is_valid_move(t_array, row, col, t_array[row][col], True):
            t_array[row][col] = 'x'
            res = self.explore_and_fill(t_array, (row if col < self.level-1 else row+1), (col+1 if col < self.level-1 else 0), step+1)
            if res:
                self.log.append(array)
                return res
        
        if self.is_valid_move(t_array, row, col, self.begin_array[row][col], False):
            t_array[row][col] = self.begin_array[row][col]
            res = self.explore_and_fill(t_array, (row if col < self.level-1 else row+1), (col+1 if col < self.level-1 else 0), step)
            if res:
                self.log.append(array)
                return res
            elif len(stacks) > 0:
                temp = stacks.pop()
                new_step = step
                if self.is_valid_move(t_array, row, col, t_array[row][col], True):
                    t_array[temp[0]][temp[1]] = 'x'
                else:
                    t_array[temp[0]][temp[1]] = 'x'
                    row = temp[0]
                    col = temp[1]
                    new_step = temp[2]
                    for i in range (input_level):
                        for j in range (input_level):
                            if (i > temp[0]):
                                t_array[i][j] = self.begin_array[i][j]
                            if i == temp[0] and j > temp[1]:
                                t_array[i][j] = self.begin_array[i][j]
                
                res = self.explore_and_fill(t_array, (row if col < self.level-1 else row+1), (col+1 if col < self.level-1 else 0), new_step+1)
                if res:
                    self.log.append(array)
                    return res
        
        return None

    def count_adjacent_occurrences(self, array, row, col):
        # Đếm số lần xuất hiện của giá trị tại ô (row, col) trong hàng và cột tương ứng
        m = 0
        for i in range(input_level):
            if array[row][i] == array[row][col] and i != col:
                m += 1
            if array[i][col] == array[row][col] and i != row:
                m += 1
        return m

    def is_not_good_position(self, matrix, r, c):
        listOfOp = []
        countBefore = 0
        for i in range (input_level):
            if i<r and matrix[i][c] == matrix[r][c]:
                countBefore = countBefore+1
            if i<c and matrix[r][i] == matrix[r][c]:
                countBefore = countBefore+1
        if countBefore > 0:
            return False
        countLast = 0
        for i in range (input_level):
            if i>r and matrix[i][c] == matrix[r][c]:
                countLast = countLast+1
            if i>c and matrix[r][i] == matrix[r][c]:
                countLast = countLast+1
        if countLast == 0:
            return False
        listOfOp = []
        for i in range (input_level):
            if c != i and matrix[r][c] == matrix[r][i]:
                listOfOp.append(self.count_adjacent_occurrences(matrix,r,i))
            if r != i and matrix[r][c] == matrix[i][c]:
                listOfOp.append(self.count_adjacent_occurrences(matrix,i,c))
        
        if len(listOfOp)==0 or self.count_adjacent_occurrences(matrix,r,c) < min(listOfOp):
            return True
        return False
    def is_valid_move(self, array, row, col, op, is_fill):
        #Kiểm tra nước đi có hợp lệ.
        def check_row_column(lst: list):
            return True if lst.count(op) > 1 else False

        def has_adjacent_patterns():
            
            if (row > 0 and row < self.level - 1 and (array[row-1][col] == 'x' or array[row+1][col] == 'x')):
                return False
            elif (col > 0 and col < self.level - 1 and (array[row][col-1] == 'x' or array[row][col+1] == 'x')):
                return False
            elif (row == col == 0 and (array[0][1] == 'x' or array[1][0] == 'x')):
                return False
            elif (row == col == self.level - 1 and (array[row][col-1] == 'x' or array[row-1][col] == 'x')):
                return False
            elif (row == 0 and col == self.level - 1 and (array[row][col-1] == 'x' or array[1][col] == 'x')):
                return False
            elif (row == self.level - 1 and col == 0 and (array[row-1][col] == 'x' or array[row][col+1] == 'x')):
                return False
            elif (row == self.level - 1 and col > 0 and col < self.level - 1 and (array[row-1][col] == 'x')):
                return False
            elif (col == self.level - 1 and row > 0 and row < self.level - 1 and (array[row][col-1] == 'x')):
                return False
            elif (row == 0 and col > 0 and col < self.level - 1 and (array[row+1][col] == 'x')):
                return False
            elif (col == 0 and row > 0 and row < self.level - 1 and (array[row][col+1] == 'x')):
                return False
            return True

        def non_shape_pattern(i: int, j: int):
            temp = array
            temp[row][col] = 'x'
            if (i == j == 0 and array[0][1] == 'x' and array[1][0] == 'x'):
                return True
            elif (i == 0 and j == self.level - 1 and array[0][j-1] == 'x' and array[1][j] == 'x'):
                return True
            elif (i == self.level - 1 and j == 0 and array[i][1] == 'x' and array[i-1][0] == 'x'):
                return True
            elif (i == j == self.level - 1 and array[i-1][j] == 'x' and array[i][j-1] == 'x'):
                return True
            elif (j == self.level - 1 and i > 0 and i < self.level - 1 and array[i-1][j] == 'x' and array[i+1][j] == 'x' and array[i][j-1] == 'x'):
                return True
            elif (i == self.level - 1 and j > 0 and j < self.level - 1 and array[i-1][j] == 'x' and array[i][j-1] == 'x' and array[i][j+1] == 'x'):
                return True
            elif (i == 0 and j > 0 and j < self.level - 1 and array[i][j-1] == 'x' and array[i][j+1] == 'x' and array[i+1][j] == 'x'):
                return True
            elif (j == 0 and i > 0 and i < self.level - 1 and array[i-1][j] == 'x' and array[i+1][j] == 'x' and array[i][j+1] == 'x'):
                return True
            elif (i > 0 and i < self.level - 1 and j > 0 and j < self.level - 1 and array[i-1][j] == 'x' and array[i+1][j] == 'x' and array[i][j+1] == 'x' and array[i][j-1] == 'x'):
                return True
            return False

        def is_non_shaded_valid():
            for i in range(self.level):
                for j in range(self.level):
                    if (array[i][j] != 'x' and non_shape_pattern(i, j)):
                        return False
            return True
        
        if is_fill == True:
            if (check_row_column(array[row]) or check_row_column([array[i][col] for i in range(self.level)])) and has_adjacent_patterns() and is_non_shaded_valid():
                return True
        if is_fill == False:
            for i in range(col):
                if (array[row][i] == op):
                    return False
            for i in range(row):
                if (array[i][col] == op):
                    return False
            return True

f = open('testcase5x5.txt', 'r')
input_data = f.read().split('\n')
input_level = 0
input_array = []
stacks = []
for i in range(len(input_data)):
        temp = input_data[i].split(',')
        input_level = len(temp)
        input_row = []
        
        for j in range(input_level):
            input_row.append(temp[j])
        input_array.append(input_row)

def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

start = default_timer()
memory_before = process_memory()

solver = HitoriPuzzleSolover(input_array, input_level)
solver.solve()
memory_after = process_memory()
print('Memory Usage:', memory_after - memory_before, 'bytes')
stop = default_timer()
print('Execution Time: ', stop - start)