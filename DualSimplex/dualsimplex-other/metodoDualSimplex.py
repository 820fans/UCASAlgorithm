# -*- coding: utf-8 -*-
import sys
import math
import numpy as np
from solution import Solution

class MetodoDualSimplex(object):
	def __init__(self, matrix):
		self.s = Solution(matrix)

	#realiza segunda fase
	def dualsimplex(self, matrix):
		print "Tableau inicial:"
		print matrix
		print ""

		numLinhas = len(matrix) - 1
		numColunas = len(matrix[0]) - 1
		passo = 0

		if self.s.noSolution(matrix):
			sys.exit(1)

		if self.s.optimalSolution(matrix):
			print "Quadro ótimo:"
			print(matrix)

			if self.s.multipleSolution(matrix):
				print "Problema possui múltiplas soluções..."
			else:
				print "Solucao única encontrada."

			if self.s.degenerada(matrix):
				print "Problema possui solução degenerada."

			x,z = self.s.mountSolution(matrix)

			print "\nX* = ", x
			print "Z* = ", z

			return matrix, x, z

		while not self.s.optimalSolution(matrix):
			linhaMenor, = np.unravel_index(matrix[1:, 0].argmin(), matrix[1:, 0].shape)
			linhaMenor = linhaMenor + 1 #precisa incrementar, visto que retorna a posicao relativa ao slice

			#cria um vetor para armazenar divisoes
			div = np.zeros(numColunas)
			for i in range(numColunas):
				div[i] = float("inf")

			for i in range(1, numColunas + 1):
				if matrix[linhaMenor][i] < 0:
					div[i-1] = matrix[0][i] / matrix[linhaMenor][i]

			#Procura o menor da divisao e guarda coluna
			colunaMenor, = np.unravel_index(div.argmin(), div.shape)
			colunaMenor = colunaMenor + 1

			pivo = matrix[linhaMenor][colunaMenor]

			if pivo != 1:
				matrix[linhaMenor, :] = matrix[linhaMenor, :] / pivo


			for i in range(numLinhas + 1):
				if i != linhaMenor:
					if matrix[i][colunaMenor] != 0:
						#calcula todas as linhas
						matrix[i, :] = matrix[i, :] - matrix[i][colunaMenor] * matrix[linhaMenor, :]

			if self.s.noSolution(matrix):
				sys.exit(1)

			if self.s.optimalSolution(matrix):
				print "\nQuadro ótimo:"
				print(matrix), "\n"

				if self.s.multipleSolution(matrix):
					print "Problema possui múltiplas soluções..."
				else:
					print "Solucao única encontrada."

				if self.s.degenerada(matrix):
					print "Problema possui solução degenerada."

				x,z = self.s.mountSolution(matrix)

				print "\nX* = ", x
				print "Z* = ", z
			else:
				passo = passo + 1
				print "Tableu do passo: ", passo
				print matrix
				print ""
