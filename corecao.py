import numpy as np
import csv
import pandas as pd
import statistics
import sys

arquivo_arcos = sys.argv[1]

csv.register_dialect('myDialect',delimiter = ';')

with open('arcos_menor_tempo.csv', 'a') as csvFile:

	writer = csv.writer(csvFile,dialect='myDialect')
	csvData = [["origem","destino","media custo","menor tempo"]]
	writer.writerows(csvData)

	arcos = pd.read_csv(arquivo_arcos, sep=';')

	origem = arcos.values[:,0]
	destino = arcos.values[:,1]
	custo = arcos.values[:,2]
	tempo = arcos.values[:,3]

	for i in range(0,len(origem)):

		aux = custo[i].replace('[','').replace(']','').replace(' ','').split(',')
		if(aux[0] != '' ):
			aux = list(map(int,aux))
			mediaCusto = statistics.median(aux)
		else:
			mediaCusto = 0

		aux2 = tempo[i].replace("'",'').replace('[','').replace(']','').replace(' 5m',' 05m')
		if(aux2 != ''):
			aux2 = aux2.replace('h','').replace('m','').replace(' ', '').split(',')
			aux2 = list(map(int,aux2))
			menorTempo = aux2[aux2.index(min(aux2))]

			if(menorTempo != 45):
				if(menorTempo > 100):
					menorTempo = int(menorTempo/100)
				else:
					a=1
			else:
				menorTempo = 0.75

		print(origem[i], destino[i],mediaCusto,menorTempo)
		csvData = [[origem[i], destino[i],mediaCusto,menorTempo]]
		writer.writerows(csvData)
csvFile.close()
