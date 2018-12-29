# -*- coding: utf-8 -*-
import sys
import numpy as np

class Solution(object):
	def __init__(self, matrix):
		self.linhas = len(matrix)
		self.colunas = len(matrix[0])

	#verifica se vetor é canonico (compara com vetor canonico)
	def canonico(self, vector):
		base = np.eye(len(vector))

		for i in range(len(vector)):
			if np.array_equal(vector, base[i,:]):
				return True

		return False

	#verifica solucao, caso alguma coluna da matriz tenha todos elementos menores ou iguais a zero significa que nao possui solucao
	def noSolution(self, matrix):
		for i in range(1, self.linhas):
			if all(j >= 0 for j in matrix[i, 1:]):
				if matrix[i][0] < 0:
					print "Tableau não possui solução única viável."
					print "W = +inf"
					print "Abortando..."
					return True

		return False

	#Verifica se se ja é solução otima,
	#ou seja, se todos os zj - cj são menores ou iguais a zero
	def optimalSolution(self, matrix):
		if all(i >= 0 for i in matrix[1:, 0]):
			return True
		else:
			return False

	#Verifica se existe alguma variável não básica cujo zj-cj = 0
	#se houver, significa que há soluções infinitas
	def multipleSolution(self, matrix):
		for i in range(1, self.colunas):
			if (not self.canonico(matrix[:,i])) and matrix[0][i] == 0:
				return True

		return False

	#Verifica no quadro ótimo existe alguma variável básica igual a zero
	#significa que solução é degenerada
	def degenerada(self, matrix):
		for i in range(1, self.colunas):
			if self.canonico(matrix[:,i]):
				posicao, = np.unravel_index(matrix[:,i].argmax(), matrix[:,i].shape)

				if matrix[posicao][0] == 0:
					return True

		return False

	#monta os vetores X* e Z*
	def mountSolution(self, matrix):
		x = np.zeros(self.colunas -1)

		for i in range(1, self.colunas):
			if self.canonico(matrix[:,i]):
				posicao, = np.unravel_index(matrix[:,i].argmax(), matrix[:,i].shape)
				x[i-1] = matrix[posicao][0]

		z = matrix[0][0]

		return x, z
