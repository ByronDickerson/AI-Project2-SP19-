from random import sample, randint,random
from time import time
from math import exp

class NQueens:
    def __init__(self,n):
        self.numQueens = n
        self.tested_options = set()
        self.count = 0

    #generates a board with randomly placed queens
    def boardQ(self):
        chessboard = list(range(self.numQueens))
        chessboard = sample(chessboard, self.numQueens)
        self.tested_options.add(''.join(str(i) for i in chessboard))
        return chessboard

    # a neighbor is defined as a board where index zero is swapped with each of the other indexes
    def calculate_neighbors(self, l):
        Neighbors = []
        for i in range(1,self.numQueens):
            for j in range(i+1,self.numQueens):
                newNeighbor = l.copy()
                newNeighbor[j], newNeighbor[i] = newNeighbor[i], newNeighbor[j]
                if not (''.join(str(i) for i in newNeighbor)) in self.tested_options:
                    Neighbors.append(newNeighbor)
                    self.tested_options.add(''.join(str(i) for i in newNeighbor))
        #print(self.tested_options)
        return Neighbors

    # calculates a single random new neighbor
    def rand_neighbor(self, l):
        newNeighbor = l.copy()
        x = randint(0,self.numQueens - 1)
        y = randint(0,self.numQueens - 1)
        while x == y:
            x = randint(0,self.numQueens - 1)
            y = randint(0,self.numQueens - 1)
        newNeighbor[y], newNeighbor[x] = newNeighbor[x], newNeighbor[y]
        return newNeighbor

    #calculate the score
    def calculate_score(self, node):
        score = 0
        for i in range(self.numQueens-1):
            for j in range(i+1,self.numQueens):
                if j-i == abs(node[i]-node[j]):
                    score += 1
        return score

    # hill climbing algorithm
    def queenHC(self,hc_board):
        start = time()
        if self.numQueens >= 4:
            new_current = False
            hc_Current = hc_board
            hc_current_Score = self.calculate_score(hc_Current)
            print("Current: " + str(hc_Current))
            print("Current's score is: " + str(hc_current_Score))
            while True:
                cNeighbors = self.calculate_neighbors(hc_Current)
                #print("Neighbors: " + str(cNeighbors))
                for i in cNeighbors:
                    Neighbor_score = self.calculate_score(i)
                    #print("Neighbor: "+ str(i)+ "\n Has score: "+ str(Neighbor_score))
                    if Neighbor_score < hc_current_Score:
                        hc_Current = i
                        hc_current_Score = Neighbor_score
                        new_current = True
                        self.count += 1
                        print("Neighbor " + str(self.count) + " is new Current")
                if not new_current:
                    end = time()
                    time_Taken = end - start
                    return hc_Current, hc_current_Score, time_Taken
                else:
                    new_current = False

    #simulated annealing algorithm
    def queenSA(self, sa_board):
        start = time()
        temp = list(range(self.numQueens*4000))
        schedule = [x/100 for x in temp if x % 2 == 0]
        schedule.reverse()
        sa_Current =  sa_board
        sa_Current_Score = self.calculate_score(sa_Current)
        print("Current: " + str(sa_Current))
        print("Current's score is: " + str(sa_Current_Score))
        for T in schedule:
            if T == 0:
                end = time()
                sa_time_Taken = end - start
                return sa_Current, sa_Current_Score, sa_time_Taken
            else:
                sa_Next = self.rand_neighbor(sa_board)
                next_Score = self.calculate_score(sa_Next)
                prob = exp((sa_Current_Score - next_Score) / T)
                if next_Score < sa_Current_Score:
                    sa_Current = sa_Next
                    sa_Current_Score = next_Score
                    #print("next is new current by score")
                elif random() < prob:
                    sa_Current = sa_Next
                    sa_Current_Score = next_Score
                    #print("next is new current by probability "+ str(prob))



amt = int(input("Please enter how many queens there are: "))
while amt > 250:
    amt = int(input("Sorry that is too many queens. Please enter a number smaller than 251: "))

if amt < 4:
    print("Sorry, a N Queens problem of that size is not solvable.")
else:
    r = NQueens(amt)
    newBoard = r.boardQ()
    #Hill climbing
    print("Hill Climbing Algorithm")
    final_node , final_score , total_time = r.queenHC(newBoard)
    print( "Final result for Hill Climbing algorithm: " + str(final_node) +
           "\nwith score: " + str(final_score) + "\nTotal time taken: " + str(total_time)+ " s")
    print("----------------------------------------------------------------------------------")
    #simulated annealing
    print("Simulated Annealing Algorithm")
    sa_final_node , sa_final_score , sa_total_time = r.queenSA(newBoard)
    print( "Final result for simulated annealing algorithm: " + str(sa_final_node) +
           "\nwith score: " + str(sa_final_score) + "\nTotal time taken: " + str(sa_total_time)+ " s")
