'''
Author: Ziwei Zheng
netid: zz1456
Date: 05/16/2019
'''
import math
import copy

# return the grid in string format for write into the file
def print_grid(arr):
    res = ""
    for i in range(9):
        for j in range(9):
            res += str(arr[i][j]) + " "
        res += "\n"
    return res

'''
A SUDOKU class will have two member variables:
a current state to record each ongoing state in forward checking process
a domain that records the domain at every stage of forward checking before it is reduced
'''

class SUDOKU:
    def __init__(self, currState, currdomain):
        self.currState = currState
        self.domain = currdomain
    # check if we have find result by seeing if there is any 0
    def isResult(self):
        res = True
        for row in self.currState:
            for col in row:
                if col == "0":
                    res = False
        return res

    def getData(self):
        state = self.forwardChecking()
        # only return the valid state data by looking at type
        if type(state) == list:
            return state
        # otherwise search for next valid state
        state = self.backtracking()
        if type(state) == list:
            return state

    # update domain
    def updateDomain(self):
        for row in range(9):
            counter = set()
            # find existing (non-empty) cell's value
            for col in range(9):
                if self.currState[row][col] != "0" and self.currState[row][col] not in counter:
                    counter.add(self.currState[row][col])
            # after find the non-empty cell's value, reduce the domain in each empty cell
            for col in range(9):
                if self.currState[row][col] == "0":
                    self.domain[row * 9 + col] -= counter
                    if len(self.domain[row * 9 + col]) == 0:
                        return
                else:
                    self.domain[row * 9 + col] = set()
        for col in range(9):
            counter = set()
            # find existing (non-empty) cell's value
            for row in range(9):
                if self.currState[row][col] != "0" and self.currState[row][col] not in counter:
                    counter.add(self.currState[row][col])
            # after find the non-empty cell's value, reduce the domain in each empty cell
            for row in range(9):
                if self.currState[row][col] != "0":
                    self.domain[row * 9 + col] = set()
                else:
                    self.domain[row * 9 + col] -= counter
                    if len(self.domain[row * 9 + col]) == 0:
                        return
        for i in range(1, 4):
            for j in range(1, 4):
                counter = set()
                for row in range(3 * j - 3, 3 * j):
                    for col in range(3 * i - 3, 3 * i):
                        # if cell does have value, put its value to counter, later on use it to reduce other empty cells' domain
                        if self.currState[row][col] != "0" and self.currState[row][col] not in counter:
                            counter.add(self.currState[row][col])
                        elif self.currState[row][col] != "0" and self.currState[row][col] in counter:
                            return
                for row in range(3 * j - 3, 3 * j):
                    for col in range(3 * i - 3, 3 * i):
                        # if cell already have a value, it does not have any domain
                        if self.currState[row][col] != "0":
                            self.domain[row * 9 + col] = set()
                        # if cell does not have value, update its domain based on the cells that has value (in counter)
                        else:
                            self.domain[row * 9 + col] -= counter
                            if len(self.domain[row * 9 + col]) == 0:
                                return

    # the function SELECT-UNASSIGNEDVARIABLE uses the minimum remaining values (MRV) heuristic.
    def selectUnassignedVariable(self):
        minLength = 0
        minRemainVals = [] # stores the index of minimum remaining value
        selectedCell = 0 # minimum cell index
        for index in range(len(self.domain)):
            # since domain will be list of constrains
            # need to mathmatically compute row and col of each cell using div and mod
            row = int(math.floor(index / 9))
            col = index % 9
            # check if the cell is unfilled
            isEmptyCell = self.currState[row][col] == "0"
            if isEmptyCell and len(minRemainVals) == 0:
                minLength = len(self.domain[index])
                minRemainVals = [(row, col)]
            elif isEmptyCell and len(self.domain[index]) == minLength and (row, col) not in minRemainVals:
                    minRemainVals.append((row, col))
            elif isEmptyCell and len(self.domain[index]) < minLength:
                minLength = len(self.domain[index])
                minRemainVals = [(row, col)]
        if len(minRemainVals) > 1:
            values = []
            for val in minRemainVals:
                row = val[0]
                col = val[1]
                count = 0
                for i in range(9):
                    if col != i and self.currState[row][i] == "0":
                        count += 1
                for j in range(9):
                    if row != j and self.currState[j][col] == "0":
                        count += 1
                for ind1 in range(row - (row % 3), row - (row % 3) + 3):
                    for ind2 in range(col - (col % 3), col - (col % 3) + 3):
                        if ind1 != row and ind2 != col and self.currState[ind1][ind2] == "0":
                            count += 1
                values.append(count)
            # select cell with lowest remaining value
            lowestVal = min(values)
            selectedCell = values.index(lowestVal)

        return minRemainVals[selectedCell]

    '''
    if an empty cell has only one value left in its domain after domain reduction, 
    we will apply forward checking on the cell’s neighbors. 
    If any empty cell has an empty domain after applying forward checking, 
    we stop the program. 
    '''
    def forwardChecking(self):
        self.updateDomain()
        ind = 0
        FCflag = False # forward checking flag
        for value in self.domain:
            # if an empty cell has only one value left in its domain
            if len(value) == 1:
                FCflag = True
                self.currState[int(math.floor(ind / 9))][ind % 9] = value.pop()
                self.domain[ind] = set()
                break
            ind += 1
        # apply forward checking on the cell’s neighbors
        if FCflag:
            res = self.forwardChecking()
            if type(res) == list:
                return res
        if self.isResult():
            return self.currState
        return True

    def backtracking(self):
        # get index of next cell of the grid
        row = self.selectUnassignedVariable()[0]
        col = self.selectUnassignedVariable()[1]
        domain = self.domain[row * 9 + col]
        # store current state in temp for recursion
        temp = copy.deepcopy(self)
        currState = temp.forwardChecking()
        # print(currState)
        # if no more forward checking exist, just return
        if not currState:
            return
        else:
            self.domain = copy.deepcopy(temp.domain)
            self.currState = copy.deepcopy(temp.currState)
            while len(domain) > 0:
                self.currState[row][col] = domain.pop()
                temp = copy.deepcopy(self)
                currState = temp.forwardChecking()
                # print(currState)
                if (type(currState) == list):
                    return currState
                elif (currState):
                    # if exist, then keep recursively backtrack
                    if temp.isResult() == True:
                        print_grid(temp.currState)
                        return temp.currState
                    next = temp.backtracking()
                    if type(next) == list:
                        return next


def main():
    userInput = input("Please Enter Your Suduko File: ")
    inputFile = open(userInput, "r")
    outputFile = open("Ouput" + userInput[-5]+".txt", "w")
    strLstFile = (inputFile.read().rstrip()).split("\n")
    print(strLstFile)
    for i in range(len(strLstFile)):
        strLstFile[i] = strLstFile[i].rstrip()
        strLstFile[i] = strLstFile[i].split(" ")
    domain = []
    for i in range(81):
        #initialize domains for every cell
        domain.append({"1", "2", "3", "4", "5", "6", "7", "8", "9"})
    initialState = SUDOKU(strLstFile, domain)
    filledState = initialState.getData()
    if (filledState):
        res = print_grid(filledState)
        outputFile.write(res)
        print(res)
    else:
        print("No solution exists")


main()