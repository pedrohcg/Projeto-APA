# -*- coding: utf-8 -*-

import math
import sys

class District:
    def __init__(self, id = 0, latitude = 0, longitude = 0):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude

class Instance:
    def __init__(self, filename):
        self.numeroDistritos = 0
        self.dmax1 = 0
        self.dmax2 = 0
        #self.dmax  = 0
        self.distritos = list()
        self.load(filename)

    def load(self, filename):
        count = 0
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if (line):
                    if (line.startswith('#')):
                        continue
                    if (count == 0):
                        self.numeroDistritos = int(line)
                        print("Numero de distritos: {}".format(self.numeroDistritos))
                        count += 1
                    elif (count == 1):
                        self.dmax1 = int(line.split(' ')[0])
                        self.dmax2 = int(line.split(' ')[1])
                        #self.dmax  = int(line.split(' ')[2])
                        print("Distancia maxima ate UPA mais proxima: {}".format(self.dmax1))
                        print("Distancia maxima ate segunda UPA mais proxima: {}".format(self.dmax2))
                        #print("Distancia maxima entre 2 UPAs: {}".format(self.dmax))
                        count += 1
                    elif (count == 2):
                        distrito = District(int(line.split(' ')[0]), int(line.split(' ')[1]), int(line.split(' ')[2]))
                        self.distritos.append(distrito)
                        print("Distrito -> Id: {} Latitude: {} Longitude: {}".format(distrito.id, distrito.latitude, distrito.longitude))
                        

def criar_matriz(numero_distritos, distritos):
    # inicializar a matriz com zeros
    matriz = [[0 for i in range(numero_distritos)] for j in range(numero_distritos)]

    for i in range(numero_distritos):
        for j in range(numero_distritos):
            # comparação de um distrito com ele mesmo
            if (i == j):
                continue

            # distrito que não foi calculado ainda
            elif(j > i):
                dist = math.sqrt(pow(distritos[i].latitude - distritos[j].latitude, 2) + pow(distritos[i].longitude - distritos[j].longitude, 2))
                matriz[i][j] = int(dist)

            # distrito que ja foi calculado
            else:
                matriz[i][j] = matriz[j][i]


    return matriz



def algoritmo_construtivo(matriz, instance):
    
    distritos_atendidos = set()  # indice dos distritos ja atendidos
    contagem_dist = 0 # número de distritos ja atendidos
    X = instance.dmax1
    Y = instance.dmax2
    num_dist = instance.numeroDistritos
    upas = []

    while contagem_dist < num_dist - 1:
        qualquer_nome = { i:{"menorQueX":set(), "menorQueY":set() } for i in range(num_dist) }

        for line in range(num_dist):
            for column in range(num_dist):
                if (line in distritos_atendidos) or (column in distritos_atendidos):
                    continue
                if line == column:
                    continue
                if matriz[line][column] <= X:
                    qualquer_nome[line]["menorQueX"].add(column)
                elif matriz[line][column] <= Y:
                    qualquer_nome[line]["menorQueY"].add(column)
            
        # Definir melhor candidato
        melhor_candidato = 0
        for i in range(1, len(qualquer_nome)):
            soma1 = len(qualquer_nome[i]["menorQueX"]) + len(qualquer_nome[i]["menorQueY"])
            soma2 = len(qualquer_nome[melhor_candidato]["menorQueX"]) + len(qualquer_nome[melhor_candidato]["menorQueY"])
            if soma1 > soma2:
                melhor_candidato = i

        # Definir distritos ja atendidos
        distritos_atendidos.add(melhor_candidato)
        upas.append(melhor_candidato)

        distritos_atendidos = distritos_atendidos.union(qualquer_nome[melhor_candidato]["menorQueX"])
        # print(f"MenorQueX para {melhor_candidato}: {qualquer_nome[melhor_candidato]['menorQueX']}")
        if len(qualquer_nome[melhor_candidato]["menorQueX"]) >= 2:
            distritos_atendidos = distritos_atendidos.union(qualquer_nome[melhor_candidato]["menorQueY"])
            # print(f"MenorQueY para {melhor_candidato}: {qualquer_nome[melhor_candidato]['menorQueY']}")

        

        #print(f"distritos atendidos para {melhor_candidato}: {distritos_atendidos}")
        contagem_dist = len(distritos_atendidos)
        # print(contagem_dist)
        # print(f"upas: {upas}")
    
    return upas



    # while(contagemDist < numDist){
    #  for(int i =0; i < numDist; i++) {
    #    for(int j =0; j < numDist; j++) {
    #      if(i == j){}  
    #      else if(matriz[i][j] <= X){
    #        contadorMenorX[i]++;
    #      } 
    #      else if(matriz[i][j] <= Y){
    #         contadorMenorY[i]++;
    #       }
    #    }
    #  }
    
    #  maisDistritosAtendidos = 0;
    
    #  for(int i = 0; i < numDist; i++){
    #    if(contadorMenorX[i] >= 1 || contadorMenorY[i] >= 1){
    #      distritosAtendidos[i] = contadorMenorX[i] + contadorMenorY[i];
    #    }
    #    if(maisDistritosAtendidos > distritosAtendidos[i]){
    #       maisDistritosAtendidos = distritosAtendidos[i];
    #    }
    #  }
    
    #  contagemDist += maisDistritosAtendidos;
    # }


instance = Instance("instance1.data")
matriz_distancias = criar_matriz(instance.numeroDistritos, instance.distritos)

upas = algoritmo_construtivo(matriz_distancias, instance)

for i in range(len(matriz_distancias[0])):
    if i in upas:
        print(f"linha {i}:\n{matriz_distancias[i]}")

# for i in range(len(matriz_distancias[0])):
#     print(matriz_distancias[i])