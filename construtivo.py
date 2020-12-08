# -*- coding: utf-8 -*-
import math


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


def algoritmo_construtivo(**kwargs):
    matriz = kwargs.get("matriz")
    instance = kwargs.get("instance")
    distritos_atendidos = set()  # indice dos distritos ja atendidos
    contagem_dist = 0 # número de distritos ja atendidos
    X = instance.dmax1  # Distância máxima até a upa mais próxima
    Y = instance.dmax2  # Distância máxima até a segunda upa mais próxima
    num_dist = instance.numeroDistritos 
    upas = [] # Array que armazena em quais distritos já foi construído uma upa
    
    dist_atual = 0
    upas.append(dist_atual) 

    while contagem_dist < num_dist:   
        dist_atual += 1
        upas.append(dist_atual)

        for indice_distrito in range(num_dist):
            count_x = 0
            count_y = 0
            for indice_upas in upas:
                if matriz[indice_distrito][indice_upas] <= X:
                    count_x += 1
                elif matriz[indice_distrito][indice_upas] <= Y:
                    count_y += 1

            if (count_x >= 2) or ((count_x == 1) and (count_y >= 1)):
                distritos_atendidos.add(indice_distrito)
        
        contagem_dist = len(distritos_atendidos)       
    return upas


# Printa quem são os distritos que possuem upa construida e quais distritos essa upa atende
def checar(matriz, upas, instance):
    num_dist = instance.numeroDistritos

    for i in upas:
        count = 0
        distritos = []
        for j in range(instance.numeroDistritos):
            if matriz[i][j] <= instance.dmax2:
                distritos.append(j)
                count += 1
        print(f"distrito {i} possui {count} distritos proximos que estao sendo atendidos pela sua upa")
        print(f"eles sao {distritos}")


def print_vizinhos_validos(matriz, instance):
    for i in range(instance.numeroDistritos):
        vizinhos = set()
        for j in range(instance.numeroDistritos):
            if matriz[i][j] <= instance.dmax2:
                vizinhos.add(j)
        print(f"vizinhos validos para o distrito {i} sao: {vizinhos} {len(vizinhos)}")


def vizinhanca(**kwargs):
    upas = kwargs.get("upas")
    matriz = kwargs.get("matriz")
    instance = kwargs.get("instance")

    num_dist = instance.numeroDistritos
    distritos_atendidos = set()
    count_dist = 0
    X = instance.dmax1
    Y = instance.dmax2
    upas_vizinhanca = []

    # guarda os vizinhos de cada distrito
    vizinhos = {i: set() for i in range(num_dist)}

    # obtem listas de vizinhos para cada vértice
    for distrito in range(num_dist):
        for vizinho in range(num_dist):
            if matriz[distrito][vizinho] <= Y:
                vizinhos[distrito].add(vizinho)
   
    melhor_candidato = -1

    # Procura o distrito dentre as upas que possui a maior quantidade de vizinhos
    for indice_distrito in upas:
        if melhor_candidato == -1:
            melhor_candidato = indice_distrito
            continue

        # armazena o melhor candidato entre os distritos
        if len(vizinhos[indice_distrito]) > len(vizinhos[melhor_candidato]):
            melhor_candidato = indice_distrito

    upas_vizinhanca.append(melhor_candidato)


    while count_dist < num_dist:
        vizinhos_utilizados = []
      
        # percorre todos os distritos pegando os vizinhos do melhor candidato
        for distrito in vizinhos[melhor_candidato]:             
            # se o distrito atual ja tiver sido atendido pula ele
            if distrito in distritos_atendidos:
                continue
            
            if distrito == melhor_candidato:
                continue

            # Adicionando a vizinhança
            if matriz[melhor_candidato][distrito] <= Y:
                vizinhos_utilizados.append(distrito)
                   
        # caso não tenha nenhum vizinho que não esteja sendo atendido e seja menor que y
        if not vizinhos_utilizados:
            # print(f"Vizinhos do 19 {vizinhos[melhor_candidato]}")
            for vizinho in range(num_dist):
                if vizinho in distritos_atendidos:
                    continue
                if matriz[melhor_candidato][vizinho] > Y:
                    upas_vizinhanca.append(vizinho)
                    melhor_candidato = vizinho
                    break
            continue
        print(melhor_candidato)
        # print(f"melhor candidato {melhor_candidato}")
        print(f"vizinhos utilizados: {vizinhos_utilizados}")
        melhor_candidato = -1
        for indice_distrito in vizinhos_utilizados:
            for distrito_vizinho in range(num_dist):
                if matriz[indice_distrito][distrito_vizinho] <= Y:
                    vizinhos[indice_distrito].add(distrito_vizinho)
                
            if melhor_candidato == -1:
                melhor_candidato = indice_distrito
                continue
                
            if len(vizinhos[indice_distrito]) > len(vizinhos[melhor_candidato]):
                melhor_candidato = indice_distrito
        
            
        # constroi a upa no melhor candidato
        upas_vizinhanca.append(melhor_candidato)

        # verifica se a legislacao esta sendo atendida
        for indice_distrito in vizinhos:
            count_x = 0
            count_y = 0
            for distrito_upa in upas_vizinhanca:
                if matriz[indice_distrito][distrito_upa] <= X:
                    count_x += 1
                elif matriz[indice_distrito][distrito_upa] <= Y:
                    count_y += 1

            if (count_x >= 2) or ((count_x == 1) and (count_y >= 1)):
                distritos_atendidos.add(indice_distrito) 

        #print(upas_vizinhanca)
        count_dist = len(distritos_atendidos) 

    return upas_vizinhanca


# roda o algoritmo passado com os parametros
def run_algo(function, **kwargs):
    return function(**kwargs)


def check_solution(solution, matriz, instance):
    num_dist = instance.numeroDistritos
    X = instance.dmax1
    Y = instance.dmax2

    checker = {index: False for index in range(num_dist)}

    for index in range(num_dist):
        count_x = 0
        count_y = 0
        for upa in solution:
            if matriz[index][upa] <= X:
                count_x += 1
            elif matriz[index][upa] <= Y:
                count_y += 1
            if (count_x >= 2) or ((count_x == 1) and (count_y >= 1)):
                checker[index] = True

    if False in checker.values():
        return False

    return True


if __name__ == "__main__":
    instance = Instance("instance4.data")
    matriz_distancias = criar_matriz(instance.numeroDistritos, instance.distritos)

    upas1 = run_algo(algoritmo_construtivo, matriz=matriz_distancias, instance=instance)
    upas2 = run_algo(vizinhanca, upas=upas1, matriz=matriz_distancias, instance=instance)

    print(upas1)
    print(upas2)

    aaaa = check_solution(upas2, matriz_distancias, instance)

    if(aaaa):
        print("ta certo")
    #checar(matriz_distancias, upas, instance)

    #print_vizinhos_validos(matriz_distancias, instance)

    #vizinhanca2(upas, matriz_distancias, instance)
    #print(upas_vizinhanca)
