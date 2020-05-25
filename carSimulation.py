import numpy as np

def value(utilityMatrix,i,j,direction):
    size=len(utilityMatrix)
    if i>=0 and j>=0 and i<=size-1 and j<=size-1:
        return utilityMatrix[i][j]
    else:
        if direction=="UP":
            return utilityMatrix[i+1][j]
        if direction=="DOWN":
            return utilityMatrix[i-1][j]
        if direction=="LEFT":
            return utilityMatrix[i][j+1]
        if direction=="RIGHT":
            return utilityMatrix[i][j-1]

def inRange(i,j,size):
    return i>=0 and j>=0 and i<=size-1 and j<=size-1

fin=open("input.txt","r")
fout=open("output.txt","w")
fout.write("")
inputLines=fin.readlines()
gridSize=0
noOfCars=0
noOfObstacles=0
obstacles=[]
cars=[]
ends=[]
for index,f in enumerate(inputLines):
    if index==0:
        gridSize=int(f.strip())
        
    if index==1:
        noOfCars=int(f.strip())

    if index==2:
        noOfObstacles=int(f.strip())

    if index in range(3,3+noOfObstacles):
        l=[int(f.strip()[0]),int(f.strip()[2])]
        obstacles.append(l)

    if index in range(3+noOfObstacles,3+noOfObstacles+noOfCars):
        l=[int(f.strip()[0]),int(f.strip()[2])]
        cars.append(l)

    if index in range(3+noOfObstacles+noOfCars,3+noOfObstacles+(2*noOfCars)):
        l=[int(f.strip()[0]),int(f.strip()[2])]
        ends.append(l)


turn_left={"LEFT":"DOWN","RIGHT":"UP","UP":"LEFT","DOWN":"RIGHT"}
turn_right={"LEFT":"UP","RIGHT":"DOWN","UP":"RIGHT","DOWN":"LEFT"}
outputString=""

for k in range(len(cars)):
    rewardMatrix=[[-1]*gridSize for i in range(gridSize)]
    utilityMatrix=[[0]*gridSize for i in range(gridSize)]
    updatedUtilityMatrix=[[-1]*gridSize for i in range(gridSize)]
    moveMatrix=[["NULL"]*gridSize for i in range(gridSize)]
    previousMoveMatrix=[["NULL"]*gridSize for i in range(gridSize)]
    rewardsList=[0]*10
    gamma=0.9
    
    for i in range(0,gridSize):
            for j in range(0,gridSize):
                if [i,j] in obstacles:
                    
                    rewardMatrix[i][j]=-101
                    continue
                if [i,j]==ends[k]:
                    
                    rewardMatrix[i][j]=99
                    utilityMatrix[i][j]=99
                    updatedUtilityMatrix[i][j]=99
                    continue
    
    
    done=False
    while not done:
        for i in range(0,gridSize):
            for j in range(0,gridSize):
                if i==ends[k][0] and j==ends[k][1]:
                    continue
                else:
                    sumList=[]
                    
                    #direction UP
                    s=0
                    s=0.7*((value(utilityMatrix,i-1,j,"UP")*gamma))
                    s+=0.1*((value(utilityMatrix,i+1,j,"DOWN")*gamma))
                    s+=0.1*((value(utilityMatrix,i,j-1,"LEFT")*gamma))
                    s+=0.1*((value(utilityMatrix,i,j+1,"RIGHT")*gamma))
                    sumList.append(s)
                    
                    #direction DOWN

                    s=0.7*((value(utilityMatrix,i+1,j,"DOWN")*gamma))
                    s+=0.1*((value(utilityMatrix,i-1,j,"UP")*gamma))
                    s+=0.1*((value(utilityMatrix,i,j-1,"LEFT")*gamma))
                    s+=0.1*((value(utilityMatrix,i,j+1,"RIGHT")*gamma))
                    sumList.append(s)
                          
                    #direction RIGHT

                    s=0.7*((value(utilityMatrix,i,j+1,"RIGHT")*gamma))
                    s+=0.1*((value(utilityMatrix,i+1,j,"DOWN")*gamma))
                    s+=0.1*((value(utilityMatrix,i-1,j,"UP")*gamma))
                    s+=0.1*((value(utilityMatrix,i,j-1,"LEFT")*gamma))
                    sumList.append(s)

                    #direction LEFT

                    s=0.7*((value(utilityMatrix,i,j-1,"LEFT")*gamma))
                    s+=0.1*((value(utilityMatrix,i+1,j,"DOWN")*gamma))
                    s+=0.1*((value(utilityMatrix,i-1,j,"UP")*gamma))
                    s+=0.1*((value(utilityMatrix,i,j+1,"RIGHT")*gamma))
                    sumList.append(s)

                    updatedUtilityMatrix[i][j]=rewardMatrix[i][j]+max(sumList)

        c=0       
        for i in range(gridSize):
                for j in range(gridSize):
                    if abs(utilityMatrix[i][j]-updatedUtilityMatrix[i][j])<=0.1:
                        c+=1
                    
        if c==gridSize**2:
            done=True
            
        if not done:
            
            for i in range(gridSize):
                for j in range(gridSize):
                    utilityMatrix[i][j]=updatedUtilityMatrix[i][j]
                    
            updatedUtilityMatrix=[[0]*gridSize for i in range(gridSize)]
            updatedUtilityMatrix[ends[k][0]][ends[k][1]]=99
                        
        else:
            for i in range(gridSize):
                for j in range(gridSize):
                    if [i,j]==ends[k]:
                        continue
                    maxList=[-float('inf')]*4
                    if inRange(i-1,j,gridSize):
                        maxList[0]=utilityMatrix[i-1][j]
                    if inRange(i+1,j,gridSize):
                        maxList[1]=utilityMatrix[i+1][j]
                    if inRange(i,j+1,gridSize):
                        maxList[2]=utilityMatrix[i][j+1]
                    if inRange(i,j-1,gridSize):
                        maxList[3]=utilityMatrix[i][j-1]

                    maxSum=max(maxList)    
                    index=maxList.index(maxSum)
                    if index==0:
                        moveMatrix[i][j]="UP"
                    elif index==1:
                        moveMatrix[i][j]="DOWN"
                    elif index==2:
                        moveMatrix[i][j]="RIGHT"
                    else:
                        moveMatrix[i][j]="LEFT"
        
    print(moveMatrix)    
    for j in range(10):
        pos = cars[k]
        np.random.seed(j)
        swerve = np.random.random_sample(1000000)
        m=0
        
        while pos != ends[k]:
            move = moveMatrix[pos[0]][pos[1]]
            if swerve[m] > 0.7:
                if swerve[m] > 0.8:
                    if swerve[m] > 0.9:
                        move = turn_left[turn_left[move]]
                    else:
                        move = turn_left[move]
                else:
                    move = turn_right[move]
            m+=1
               
            if move=="UP":
                if inRange(pos[0]-1,pos[1],gridSize):
                    pos=[pos[0]-1,pos[1]]
                rewardsList[j]+=rewardMatrix[pos[0]][pos[1]]
            if move=="DOWN":
                if inRange(pos[0]+1,pos[1],gridSize):
                    pos=[pos[0]+1,pos[1]]
                rewardsList[j]+=rewardMatrix[pos[0]][pos[1]]
            if move=="RIGHT":
                if inRange(pos[0],pos[1]+1,gridSize):
                    pos=[pos[0],pos[1]+1]
                rewardsList[j]+=rewardMatrix[pos[0]][pos[1]]
            if move=="LEFT":
                if inRange(pos[0],pos[1]-1,gridSize):
                    pos=[pos[0],pos[1]-1]
                rewardsList[j]+=rewardMatrix[pos[0]][pos[1]]
            
    outputString+=str(int(np.floor(sum(rewardsList)/10)))+"\n"

fout.write(outputString)
fin.close()
fout.close()

    
        
