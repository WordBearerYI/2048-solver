from BaseAI import BaseAI
from random import randint
import math
import numpy as np
import time
import Grid

class PlayerAI(BaseAI):

    def HeuVal(self,grid):
        Smoothness, Mono, Emptiness, SmallNum = self.SmooAndMono(grid)
        MaxAtCorner = self.MaxAtCorners(grid)
        var=self.var(grid)
        #return Smoothness*2 + Mono*6 + MaxAtCorner*5 + Emptiness*2
        return   Emptiness*3  + Smoothness + MaxAtCorner*5 + NewNum

    def SmooAndMono(self,grid):
        Smoodic = [[0 for i in range(4)] for j in range(4)]
        Monodici = [[0 for i in range(3)] for j in range(3)]
        Monodicj = [[0 for i in range(3)] for j in range(3)]
        Smoothie = 0; Mono=0; Emptiness=0;SmallNum=0;
        for i in range(4):
            for j in range(4):
                Smoodic[i][j]=grid.getCellValue((i,j))
                if Smoodic[i][j] != 0:
                   Emptiness += 1
                if Smoodic[i][j] == 2 or Smoodic[i][j] ==4:
                   SmallNum += 1

        Emptiness = -Emptiness * 5
        SmallNum  = SmallNum * (-4)

        for i in range(3):
            for j in range(3):
                difi = Smoodic[i + 1][j] - Smoodic[i][j]
                #diff in vertical neighbors
                difj = Smoodic[i][j+1] - Smoodic[i][j]
                #diff in horizontal neighbors
                Monodici[i][j] = difi
                Monodicj[i][j] = difj
                Smoothie += abs(difj) + abs(difi)

        def Monopenalty(x,y):
            if x * y < 0:
                return (abs(x)+abs(y))*(-3)
            if x * y >= 0:
                return 0

        for j in range(3):
            Mono += Monopenalty(Monodici[0][j], Monodici[1][j]) + Monopenalty(Monodici[1][j], Monodici[2][j])+ Monopenalty(Monodicj[j][0] , Monodicj[j][1]) + Monopenalty(Monodicj[j][1], Monodicj[j][2])

        return Smoothie,Mono,Emptiness,SmallNum

    def var(self,grid):
        sum=0;var=0
        for i in range(4):
            for j in range(4):
                sum += grid.getCellValue((i,j))
        sum = sum/16
        for i in range(4):
            for j in range(4):
                var += pow((sum-grid.getCellValue((i,j))),2)
        return var

    def MaxAtCorners(self,grid):
        max= grid.getMaxTile()
        if grid.getCellValue((0, 0)) == max or grid.getCellValue((0, 3)) == max or \
        grid.getCellValue((3, 3)) == max or grid.getCellValue((3, 0)) == max:
            return max*3
        else:
            return max

    def AlphaBeta(self, grid, alpha, beta, depth, MoM,):
        AvailableMoves = grid.getAvailableMoves()
        if AvailableMoves:
            bestMove = AvailableMoves[randint(0, len(AvailableMoves) - 1)]
        else:
            bestMove = None
        if depth == 0:
            return (self.HeuVal(grid),None)
        if MoM:
            bestScore = alpha
            if len(AvailableMoves) > 0:
                for move in AvailableMoves:
                    gridCp = grid.clone()
                    gridCp.move(move)
                    result = self.AlphaBeta(gridCp, alpha, beta, depth - 1,False)
                    if result[0] > bestScore:
                        bestScore = result[0]
                        bestMove = move
                    if bestScore >= beta:
                        return (beta, bestMove)
            return (bestScore, bestMove)

        else:
            bestScore = beta
            for cell in grid.getAvailableCells():
                for cell_values in [2, 4]:
                    gridCpy = grid.clone()
                    gridCpy.setCellValue(cell, cell_values)
                    result = self.AlphaBeta(gridCpy, alpha, beta, depth - 1, True)
                    gridCpy.setCellValue(cell, 0)
                    if result[0] < bestScore:
                        bestScore = result[0]
                    if bestScore <= alpha:
                        return (alpha, None)
                return (bestScore, None)
            return (bestScore, bestMove)


    def getMove(self, grid):
        return self.AlphaBeta(grid, float("-inf"), float("inf"),4,True,)[1]

