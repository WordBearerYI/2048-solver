from BaseAI import BaseAI
from random import randint
import Grid

import numpy as np
import time
import math


class PlayerAI(BaseAI):

    def getMove(self, grid):
        return self.AlphaBetaPr(grid, float("-inf"), float("inf"), 1, 4 )[1]

    def moveSelect(self,grid):
        avMove = grid.getAvailableMoves()
        num = len(avMove)
        if num >0:
            bestMove = avMove[randint(0, num - 1)]
        else:
            bestMove = None
        return num, avMove, bestMove

    def AlphaBetaPr(self, grid, alpha, beta, MinMax, depth):
        num, avMove, bestMove =self.moveSelect(grid)
        if depth <= 0:
            return (self.HeuriVal(grid),None)
        if MinMax == 1:
            bestScore = alpha
            if num > 0:
                for m in avMove:
                    gridCp = grid.clone()
                    gridCp.move(m)
                    result = self.AlphaBetaPr(gridCp, alpha, beta, 0, depth - 1)
                    if  bestScore < result[0]:
                        bestMove = m
                        bestScore = result[0]
                    if bestScore >= beta:
                        return (beta, bestMove)
            return (bestScore, bestMove)

        elif MinMax == 0:
            bestScore = beta
            for cell in grid.getAvailableCells():
                for valueCell in [4, 2]:
                    gridCpy = grid.clone()
                    gridCpy.setCellValue(cell, valueCell)
                    result = self.AlphaBetaPr(gridCpy, alpha, beta, 1, depth - 1)
                    gridCpy.setCellValue(cell, 0)
                    if bestScore>result[0]:
                        bestScore = result[0]
                    if bestScore <= alpha:
                        return (alpha, None)
                return (bestScore, None)
            return (bestScore, bestMove)

    def HeuriVal(self, grid):
        #NewNum, Emptiness,Large = self.Smooth(grid)
        #MaxAtBorder,sum = self.MaxAtBorders(grid)
        # return Smoothness*2 + Mono*6 + MaxAtCorner*5 + Emptiness*2
        #return Emptiness * 5 + NewNum * 5 + MaxAtBorder * 8 + Large*3
        return  self.Mask(grid)- self.MergeEnc(grid)


    def Mask(self,grid):
        #mask = [[6-i-j for i in range(4)] for j in range(4)]
        mask = [[2,4,8,16],[128,96,64,32],[156,192,238,276],[488,400,368,322]]
        score = 0
        for i in range(4):
            for j in range(4):
                score += grid.getCellValue((i, j)) *mask[i][j]
        return score

    def MergeEnc(self,grid):
        penalty = 0
        for i in range(4):
            for j in range(4):
                for n in self.getNeighbor(grid,i,j):
                    penalty += abs(grid.getCellValue((i, j)) - n)
        return penalty*0.5

    def getNeighbor(self,grid,i,j):
        res =[]
        if not grid.crossBound((i-1,j)):
            res.append(grid.getCellValue((i-1, j)))
        if not grid.crossBound((i+1,j)):
            res.append(grid.getCellValue((i+1, j)))
        if not grid.crossBound((i,j-1)):
            res.append(grid.getCellValue((i, j-1)))
        if not grid.crossBound((i,j+1)):
            res.append(grid.getCellValue((i, j+1)))
        return res

    def Smooth(self, grid):
        smooth ={}
        for i in range(4):
            for j in range(4):
                  smooth[(i,j)] = 0
        Emp = 0;
        NewNum = 0;
        Large = grid.getMaxTile()
        for i in range(4):
            for j in range(4):
                smooth[(i,j)] = grid.getCellValue((i, j))
                if  smooth[(i,j)] == 0:
                    Emp += 1
                elif smooth[(i,j)] == 2 or smooth[(i,j)] == 4:
                    NewNum += 1

        Emptiness = Emp
        NewNum = - NewNum


        #for i in range(3):
        #    for j in range(3):
        #        difi = Smoodic[i + 1][j] - Smoodic[i][j]
         #       # diff in vertical neighbors
         #       difj = Smoodic[i][j + 1] - Smoodic[i][j]
        #        # diff in horizontal neighbors
        #        Monodici[i][j] = difi
        #        Monodicj[i][j] = difj
        #        Smoothie += abs(difj) + abs(difi)


        return  NewNum, Emptiness,Large

   # def AndMono:
       # Monodici = [[0 for i in range(3)] for j in range(3)]
       # Monodicj = [[0 for i in range(3)] for j in range(3)]
       # Mono = 0;
       # def Monopenalty(x, y):
       #     if x * y < 0:
       #         return (abs(x) + abs(y)) * (-3)
       #     if x * y >= 0:
       #         return 0

        #for j in range(3):
        #    Mono += Monopenalty(Monodici[0][j], Monodici[1][j]) + Monopenalty(Monodici[1][j],
        #                                                                      Monodici[2][j]) + Monopenalty(
        #        Monodicj[j][0], Monodicj[j][1]) + Monopenalty(Monodicj[j][1], Monodicj[j][2])


    def MaxAtBorders(self, grid):
        sum = self.sumBoard(grid)
        max = grid.getMaxTile()
        if grid.getCellValue((0, 0)) == max or grid.getCellValue((0, 3)) == max or \
                        grid.getCellValue((3, 3)) == max or grid.getCellValue((3, 0)) == max:
            return max/(sum-max),sum
        elif grid.getCellValue((1, 0)) == max or grid.getCellValue((2, 0)) == max or \
                        grid.getCellValue((0, 1)) == max or grid.getCellValue((0, 2)) == max or \
                            grid.getCellValue((3, 1)) == max or grid.getCellValue((3, 2)) == max or \
                                    grid.getCellValue((1, 3)) == max or grid.getCellValue((2, 3)) == max:

            return max/(sum - max/2),sum
        else:
            return 0,sum

    def sumBoard(self,grid):
        sum = 0
        for i in range(4):
            for j in range(4):
                sum += grid.getCellValue((i, j))
        return sum


