'''
Author: Ziwei Zheng
Date: 04/11/2019
'''
import copy

# calculate how many linear conflict there are
def linearConflict(currState, goalState):
    count = 0
    resLst = [] #store all the linear conflict nodes
    tLst = [[],[],[]]
    goalLst = [[],[],[]]
    #to generate all initial index number
    for row in range(len(currState[0])):
        for col in range(len(currState)):
            tLst[row].append([row,col])

    #to calculate all the goal position in each node
    for row in range(len(currState[0])):
        for col in range(len(currState)):
            target = currState[row][col]
            goalLst[row].append(getGoalPosition(target, goalState)) #append each value's position in goalState into the the temparory list to compare the indexes later

    # examine if tj and tk are both in the same line
    # and tj is to the right of tk (cond1)
    # and goal position of tj is to the left of tk (cond2)

    # first check each row
    for i in range(3):
        for j in range(3):
            increment = 1
            while (j+increment < 3):
                cond0 = currState[i][j] != 0 and currState[i][j + increment] != 0
                cond1 = tLst[i][j][1] < tLst[i][j + increment][1] # check if tj is to the right of tk
                cond2 = goalLst[i][j][1] > goalLst[i][j + increment][1] # check if goal position of tj is to the left of tk
                cond3 = goalLst[i][j][0] == goalLst[i][j + increment][0] # check if goal position of tj is on the same line
                if (cond0 and cond1 and cond2 and cond3):
                    resLst.append((currState[i][j], currState[i][j+increment]))
                    count+=1
                increment += 1

    # second check each column
    for row in range(3):
        for col in range(3):
            increment = 1
            while (row+increment < 3):
                cond0 = currState[row][col] != 0 and currState[row + increment][col] != 0
                cond1 = tLst[row][col][0] < tLst[row + increment][col][0] # check if tj is to the down of tk
                cond2 = goalLst[row][col][0] > goalLst[row + increment][col][0] # check if goal position of tj is to the up of tk
                cond3 = goalLst[row][col][1] == goalLst[row + increment][col][1] # check if goal position of tj is on the same column
                if (cond0 and cond1 and cond2 and cond3):
                    resLst.append((currState[row][col], currState[row+increment][col]))
                    count+=1
                increment += 1
    # print(resLst)
    # print("Init [row, col]", tLst)
    # print("Goal [row, col]: ",goalLst)
    return count

def getGoalPosition(target,glState):
    goalPosX = 0
    goalPosY = 0
    while (target != glState[goalPosX][goalPosY]):
        if (goalPosX < 2):
            goalPosX += 1  # increase column index until it reaches to rightmost column index
        else:
            goalPosX = 0  # start over from first column index when reach to the rightmost of last column
            goalPosY = (goalPosY + 1) % 3  # increase row index
    return [goalPosX,goalPosY] #return target's Position in Goal State



def manhattanSum(currState, glState):
    sum = 0
    #currPos = (0,0) #record current position, will be updated throughout the search
    #isDone = False #false if did not go through all nodes to find manhattan sum
    for row in range(len(currState[0])):
        for col in range(len(currState)):
            # the current value in current State, we want to find its position in goal state
            target = currState[row][col]
            #print("Target is",target,"\n")
            if (target != 0):
                goalPos = getGoalPosition(target, glState)
                sum += (abs(row-goalPos[0]) + abs(col-goalPos[1]))
                #print("Now the sum is",sum,"\n")
    return sum

#convert string to int when read file
def strToInt(stateLst):
    print(stateLst)
    for lst in stateLst:
        for i in range(len(lst)):
            lst[i] = int(lst[i])

# convert int to string when output file
def display(initTile, currTile, resultTile):
    step1 = ""
    step2 = ""
    res= ""
    pathList = []
    res += initTile.outputFormat()+ "\n"+resultTile.outputFormat()+ "\n" + str(resultTile.pathCost) + "\n" + str(currTile.countGenerated) + "\n"

    if resultTile.lastAction != None and resultTile.prevState != None:
        addToPath(resultTile.prevState, pathList)
        pathList.append((resultTile.lastAction, resultTile.prevState))

    for tile in pathList:
        step1 += str(tile[0]) + " "
        step2 += str(tile[1].funcCost) + " "
    res += step1 + "\n" + step2 + "\n"
    return res

def addToPath(currTile, path):
    if currTile.lastAction == None and currTile.prevState == None:
        return
    else:
        addToPath(currTile.prevState, path)
        path.append((currTile.lastAction, currTile.prevState))

class eightPuzzle:
    def __init__(self, initialNode, goalState):
        # initialize variables to track A start search process: queue visited nodes, goal state
        self.queueLst = [initialNode]
        self.visitedNodes = []
        self.goalState = goalState
        # initialize variable to count how many nodes generated and how many node has spanned
        self.countGenerated = 1
        self.countSpanned = 0

    def AstarSearch(self):
        result = self.queueLst[-1]
        while (result.currState != self.goalState):
            if (len(self.queueLst) == 0):
                return
            # We span the first node in the queue with the smallest function cost
            currNode = self.queueLst.pop()
            childLst = currNode.GenerateChildren()
            self.countSpanned += 1 #update how many nodes generated
            self.visitedNodes.append(currNode)
            # check if each child generated is already visited, if it isn't, add to our queue
            for child in childLst:
                isVisited = False
                for node in self.visitedNodes:
                    if child.currState == node.currState:
                        # we find the same existing tile in visited node
                        isVisited = True
                if not isVisited:
                    self.queueLst.append(child)
                    self.countGenerated += 1
            self.queueLst.sort(key=lambda x : x.funcCost, reverse=True)
            result=self.queueLst[-1]
        return result

class state:
    '''Initialize the state variables'''
    def __init__(self, currState, goalState, pathCost, typeH="Y", lastAction=None, prevState=None):
        self.currState = currState
        self.goalState = goalState
        self.pathCost = pathCost
        self.typeInput = typeH
        try:
            if (self.typeInput == "Y"):
                self.funcCost = manhattanSum(self.currState, goalState)+ 2 * linearConflict(self.currState, self.goalState) + self.pathCost
            elif (self.typeInput == "N"):
                self.funcCost = manhattanSum(self.currState, goalState) + self.pathCost
        except:
            print("Invalid Input, please try again")
        self.lastAction = lastAction
        self.prevState = prevState
    '''Movement of the node will result in a new tile'''
    def left(self, targetPos):
        # node generated after left move
        newTile = copy.deepcopy(self.currState)
        newTile[targetPos[0]][targetPos[1]] = newTile[targetPos[0]][targetPos[1] - 1]
        newTile[targetPos[0]][targetPos[1] - 1] = 0
        leftChildNode = state(newTile, self.goalState, self.pathCost + 1, self.typeInput, "L", self)
        return leftChildNode

    def right(self, targetPos):
        # node generated after right move
        newTile = copy.deepcopy(self.currState)
        newTile[targetPos[0]][targetPos[1]] = newTile[targetPos[0]][targetPos[1] + 1]
        newTile[targetPos[0]][targetPos[1] + 1] = 0
        rightChildNode = state(newTile, self.goalState, self.pathCost + 1, self.typeInput, "R", self)
        return rightChildNode

    def up(self, targetPos):
        # node generated after up move
        newTile = copy.deepcopy(self.currState)
        newTile[targetPos[0]][targetPos[1]] = newTile[targetPos[0] - 1][targetPos[1]]
        newTile[targetPos[0] - 1][targetPos[1]] = 0
        upChildNode = state(newTile, self.goalState, self.pathCost + 1, self.typeInput, "U", self)
        return upChildNode

    def down(self, targetPos):
        # node generated after down move
        newTile = copy.deepcopy(self.currState)
        newTile[targetPos[0]][targetPos[1]] = newTile[targetPos[0] + 1][targetPos[1]]
        newTile[targetPos[0] + 1][targetPos[1]] = 0
        DownChildNode = state(newTile, self.goalState, self.pathCost + 1, self.typeInput, "D", self)
        return DownChildNode

    ''' find zero position in the state'''
    def findZeroPosition(self):
        for row in range(3):
            for col in range(3):
                if self.currState[row][col]== 0:
                    return (row, col)


    ''' the children nodes generated by the spanning node'''
    def GenerateChildren(self):
        targetPos = self.findZeroPosition()
        newChildLst = []

        # depending on zero's position, we can move up, down, left, or right.
        if (targetPos[0] > 0):
            newChildNode=self.up(targetPos)
            newChildLst.append(newChildNode)

        if (targetPos[0] < 2):
            newChildNode=self.down(targetPos)
            newChildLst.append(newChildNode)

        if (targetPos[1] > 0):
            newChildNode=self.left(targetPos)
            newChildLst.append(newChildNode)

        if (targetPos[1] < 2):
            newChildNode=self.right(targetPos)
            newChildLst.append(newChildNode)

        return newChildLst

    # format our output
    def outputFormat(self):
        output = ""
        for row in self.currState:
            for val in row:
                output += str(val) + " "
            output += "\n"
        return output



def main():
    # read inpute file name from user
    userFile = input("Please enter your file name: ")
    typeHeuristic = input("Would you like to add Linear Conflict? \nPlease Enter (Y/N): ")
    file = open(userFile, "r")
    # format the string from input file
    allState = (file.read().rstrip()).split("\n")
    allState.remove("")
    # initialize list to save initial state and goal state from input file
    initState = []
    goalState = []
    # seperate the string into initial state and goal state
    for rowInd in range(len(allState)):
        # the previous three line of info store into inite state
        if rowInd < 3:
            initState.append(allState[rowInd].split(" "))
        # the last three line of info store into goal state
        else:
            goalState.append(allState[rowInd].split(" "))
    # convert string into integer in each state
    strToInt(initState)
    strToInt(goalState)
    # store our initial state as our root tile
    rootTile = state(initState,goalState,0,typeHeuristic,None,None)
    problem = eightPuzzle(rootTile, goalState)
    result = problem.AstarSearch()
    resultStr = display(rootTile, problem, result)
    print(resultStr)
    file.close()
    # depending on heuristic type, generate different file name
    if typeHeuristic == "Y":
        userFile = "LC"+userFile
    if typeHeuristic == "N":
        userFile = "ans"+userFile
    # write files
    outputFile = open(userFile,"w")
    outputFile.write(resultStr)
    outputFile.close()
main()