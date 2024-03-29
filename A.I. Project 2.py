"""
Names: Zoe Lambert, Byron Dickerson, Carly Good
Project 2: Hill-Climbing and Simulating Annealing algorithms for the n-Queens and Sudoku problems
Date: 3/1/19
Semester: SP 2019
"""
from random import sample, randint,random
from time import time
from math import exp
import numpy as np

class NQueens:
    def __init__(self,n):
        self.numQueens = n
        self.tested_options = set()

    #generates a board with randomly placed queens
    def boardQ(self):
        chessboard = list(range(self.numQueens))
        chessboard = sample(chessboard, self.numQueens)
        self.tested_options.add(''.join(str(i) for i in chessboard))
        return chessboard

    # calculate the score. which is the total number of conflicts
    def calculate_score(self, node):
        score = 0
        for i in range(self.numQueens - 1):
            for j in range(i + 1, self.numQueens):
                if j - i == abs(node[i] - node[j]):
                    score += 1
        return score

    # calculates the amount of queens that a single queen sees
    def calculate_see(self, node, i):
        see = 0
        for j in range( self.numQueens):
            if i != j:
                if j - i == abs(node[i] - node[j]):
                    see += 1
        return see

    # a neighbor is defined as a board where index i is swapped with each of the other indexes
    def calculate_neighbor(self, l):
        lowest = l
        how_much_better = 0
        for i in range(self.numQueens):
            i_score = self.calculate_see(l, i)
            for j in range(i+1,self.numQueens):
                j_score = self.calculate_see(l, j)
                newNeighbor = l.copy()
                newNeighbor[j], newNeighbor[i] = newNeighbor[i], newNeighbor[j]
                newNeighbor_i = self.calculate_see(newNeighbor, i)
                newNeighbor_j = self.calculate_see(newNeighbor, j)

                calc_diff = (i_score + j_score) - (newNeighbor_i + newNeighbor_j)
                if calc_diff > how_much_better:
                    lowest = newNeighbor
                    how_much_better = calc_diff
        return lowest , how_much_better

    # calculates a the possible neighbors and then selects a random one
    def rand_neighbor(self, l):
        neighbors = []
        for i in range(self.numQueens - 1):
            for j in range(i + 1, self.numQueens):
                newNeighbor = l.copy()
                newNeighbor[i], newNeighbor[j] = newNeighbor[j], newNeighbor[i]
                neighbors.append(newNeighbor)
        x = randint(0,len(neighbors)-1)
        return neighbors[x]

    # hill climbing algorithm
    def queenHC(self,hc_board):
        start = time()
        if self.numQueens >= 4:
            hc_Current = hc_board
            hc_Current_score = self.calculate_score(hc_Current)
            print("Current: " + str(hc_Current))
            print("current score: " + str(hc_Current_score))
            while True:
                next_node,next_node_score = self.calculate_neighbor(hc_Current)
                if next_node_score != 0:
                    hc_Current = next_node
                else:
                    end = time()
                    time_Taken = end - start
                    hc_Current_score = self.calculate_score(hc_Current)
                    return hc_Current, hc_Current_score, time_Taken

    #simulated annealing algorithm
    def queenSA(self, sa_board):
        start = time()
        temp = list(range(10000))
        schedule = [x/25 for x in temp if x % 2 == 0]
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
                prob = exp((sa_Current_Score-next_Score)/ T)
                if next_Score < sa_Current_Score:
                    sa_Current = sa_Next
                    sa_Current_Score = next_Score
                elif random() < prob:
                    sa_Current = sa_Next
                    sa_Current_Score = next_Score

class Sudoku:
    def __init__(self, e):
        self.myFile = np.genfromtxt(e, delimiter=',')
        self.safe_numbers = np.zeros((25,25))

    #create random starting board
    def boardS(self):
        puzzle = self.myFile

        for i in range(len(puzzle)):
            numbers = list(range(26))
            for j in range(len(puzzle)):
                if puzzle[i][j] != 0:
                    self.safe_numbers[i][j] = True
                    numbers.remove( puzzle[i][j])
            for j in range(len(puzzle)):
                if puzzle[i][j] == 0:
                    self.safe_numbers[i][j] = False
                    x = randint(1, 25)
                    while x not in numbers:
                        x = randint(1,25)
                    puzzle[i][j] = x
                    numbers.remove(x)
        return puzzle

    def check_columns(self,y):
        columns_score = 0

        for i in range(len(y)):
            numbers_in_c = []
            for j in range(len(y)):
                if y[j][i] in numbers_in_c:
                    columns_score +=1
                else:
                    numbers_in_c.append(y[j][i])

        return columns_score


    def check_squares(self,y):
        square_score = 0
        for s in range(25):
            numbers_in_squ = []
            for n in range(25):
                a = (s // 5)*5 + (n % 5)
                b = (s % 5)*5 + (n // 5)
                if y[a][b] in numbers_in_squ:
                    square_score +=1
                else:
                    numbers_in_squ.append(y[a][b])
        return square_score


    def scoreOf(self,s):
        score = 0
        score += self.check_columns(s)
        score += self.check_squares(s)
        return score

    def get_neighbors(self, game_board):
        neighbor_list = []
        for row in range(25):
            for index1 in range(24):
                for index2 in range(index1+1,25):
                    newNeighbor = game_board.copy()
                    if self.safe_numbers[row][index1] == 0 and self.safe_numbers[row][index2] == 0:
                        newNeighbor[row][index2],newNeighbor[row][index1] = newNeighbor[row][index1],newNeighbor[row][index2]
                        neighbor_list.append(newNeighbor)
        return neighbor_list

    #hill climbing algorithm for sudoku
    def sudokuHC(self,s_HC_Board):
        start = time()
        puzzle_board = s_HC_Board
        puzzle_score = self.scoreOf(puzzle_board)
        new_board = False
        print("Current:\n " + str(puzzle_board))
        print("current score: " + str(puzzle_score))
        while True:
            next_nodes= self.get_neighbors(puzzle_board)
            for node in next_nodes:
                next_node_score = self.scoreOf(node)
                if next_node_score < puzzle_score:
                    puzzle_board = node
                    puzzle_score = next_node_score
                    new_board = True
            if not new_board:
                end = time()
                s_time_Taken = end - start
                return puzzle_board, puzzle_score, s_time_Taken
            else:
                new_board = False



    #Simulated annealing  algorithm for sudoku
    def sudokuSA(self, s_SA_Board):
        start = time()
        temp = list(range(15000))
        schedule = [x / 15 for x in temp ]
        schedule.reverse()
        sa_puzzle_board = s_SA_Board
        sa_puzzle_score = self.scoreOf(sa_puzzle_board)
        print("Current:\n " + str(sa_puzzle_board))
        print("current score: " + str(sa_puzzle_score))
        for T in schedule:
            if T == 0:
                end = time()
                s_time_Taken_sa = end - start
                return sa_puzzle_board, sa_puzzle_score, s_time_Taken_sa
            else:
                next_nodes = self.get_neighbors(sa_puzzle_board)
                rand = randint(0, len(next_nodes)-1)
                next_node = next_nodes[rand]
                next_node_score = self.scoreOf(next_node)
                prob = exp((sa_puzzle_score-next_node_score)/ T)
                if next_node_score < sa_puzzle_score:
                    sa_puzzle_board= next_node
                    sa_puzzle_score = next_node_score
                elif random() < prob:
                    sa_puzzle_board = next_node
                    sa_puzzle_score = next_node_score



selection = int(input("Please select which problem you would like solved.\n (1) Nqueens\n (2) Sudoku\nselect 1 or 2: "))

if selection == 1:

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


elif selection == 2:

    file = input("Please enter the file name for the board: ")
    r = Sudoku(file)
    gameBoard = r.boardS()
    # Hill climbing
    print("Hill Climbing Algorithm")
    final_node_s , final_score_s, total_time_s = r.sudokuHC(gameBoard)
    print("Final result for Hill Climbing algorithm:\n " + str(final_node_s) +
          "\nwith score: " + str(final_score_s) + "\nTotal time taken: " + str(total_time_s) + " s")
    print("----------------------------------------------------------------------------------")
    # simulated annealing
    print("Simulated Annealing Algorithm")
    sa_final_node_s, sa_final_score_s, sa_total_time_s = r.sudokuSA(gameBoard)
    print("Final result for simulated annealing algorithm:\n " + str(sa_final_node_s) +
          "\nwith score: " + str(sa_final_score_s) + "\nTotal time taken: " + str(sa_total_time_s) + " s")


else:
    print("invalid selection")
