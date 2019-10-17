import numpy as np
import csv
import pandas as pd
import psycopg2

try:
    conn = psycopg2.connect("dbname='riscos' user='helio4' host='localhost' password='helio'")

except:
    print ("Falha na conexão")

cur = conn.cursor()

csv.register_dialect('myDialect',delimiter = ';')

with open('arcos_nulo_estado.csv', 'a') as csvFile:

	writer = csv.writer(csvFile,dialect='myDialect')
	csvData = [["origem","destino","estado origem","estado destino"]]
	writer.writerows(csvData)



	arcos = pd.read_csv('ARCOSNULO.csv', sep=';')
	
	origem = arcos.values[:,0]
	destino = arcos.values[:,1]

	
	for i in range(0,len(origem) - 1):
		cur.execute("select uf from aerodromos where icao = %s", (origem[i],))
		pesquisa1 = cur.fetchall()
		conn.commit()
		
		cur.execute("select uf from aerodromos where icao = %s", (destino[i],))
		pesquisa2 = cur.fetchall()
		conn.commit()

		print(pesquisa2[0][0])
		

		csvData = [[origem[i], destino[i],pesquisa1[0][0], pesquisa2[0][0] ]]
		writer.writerows(csvData)
csvFile.close()





