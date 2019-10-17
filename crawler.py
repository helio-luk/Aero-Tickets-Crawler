from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pandas as pd
import time
import datetime
import numpy as np
import csv
import sys

from webdriver_manager.chrome import ChromeDriverManager

preco = []
duracao = []
arquivo_arcos = sys.argv[1]

data_voo = input('Digite a data do voo no formato YYYY-MM-DD')

csv.register_dialect('myDialect',delimiter = ';')

with open('resultado.csv', 'a') as csvFile:

	writer = csv.writer(csvFile,dialect='myDialect')
	csvData = [["origem","destino","precos","duracoes"]]
	writer.writerows(csvData)

	arcos = pd.read_csv(arquivo_arcos, sep=';', usecols=['origem','destino'])
	iata_icao = pd.read_csv('iata-icao.csv', sep=';', usecols=['iata','icao'])

	iata = iata_icao.values[:,0]
	icao = iata_icao.values[:,1]

	origem = arcos.values[:,0]
	destino = arcos.values[:,1]

	for i in range(0, len(origem) - 1):
		try:
			iata_origem = iata[np.where(icao == origem[i])[0][0]]
			iata_destino = iata[np.where(icao == destino[i])[0][0]]
			print(iata_origem,iata_destino)

			browser = webdriver.Chrome(ChromeDriverManager().install())
			link = 'https://www.decolar.com/shop/flights/results/oneway/'+iata_origem+'/'+iata_destino+'/'+data_voo+'/1/0/0/NA/NA/NA/NA?from=SB&di=1-0'
			browser.get(link)
			time.sleep(8)

			flights_only = browser.find_elements_by_xpath("//span[@class='fare main-fare-big']")
			flights_only2 = browser.find_elements_by_xpath("//span[@class='best-duration']")

			for a in flights_only:
				preco.append(int(a.text.replace('R$','').replace('.','')))
			for a in flights_only2:
				duracao.append(a.text)

			print(origem[i],destino[i],preco,duracao)
			csvData = [[origem[i], destino[i], preco, duracao]]
			writer.writerows(csvData)

			preco = []
			duracao = []
			browser.quit()

		except:
			preco = []
			duracao = []
			print(origem[i], destino[i])
			csvData = [[origem[i], destino[i], preco, duracao ]]
			writer.writerows(csvData)
csvFile.close()
