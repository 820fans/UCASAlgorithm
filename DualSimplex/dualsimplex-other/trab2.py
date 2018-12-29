# -*- coding: utf-8 -*-
import sys
import os.path
import numpy as np
from solution import Solution
from metodoDualSimplex import MetodoDualSimplex

def main(argv):
	#filename = raw_input('Digite o Nome do Arquivo com a Matriz de Entrada: ')
	filename = "matriz1.txt"

	if not os.path.exists(filename):
		print('Arquivo inválido.\nAbortando')
		sys.exit(1)

	matrix = []

	matrix = np.loadtxt(filename, delimiter = " ")

	#pega o ultimo da lista
	#apaga o ultimo da lista
	#adiciona no começo
	newmatrix = []
	for row in matrix:
		last = row[-1]
		row = np.delete(row, -1)
		row = np.insert(row, 0, last)
		newmatrix.append(row)

	matrix = np.array(newmatrix)
	# vb = np.zeros(len(matrix))

	#cria classe MetodoDualSimplex
	simplex = MetodoDualSimplex(matrix)

	#executa dual simlex
	print "Iniciando dual simplex..."
	matrix[0,:] = (-1) * matrix[0,:]
	simplex.dualsimplex(matrix)


if __name__ == '__main__':
	main(sys.argv)
