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
        self.dmax  = 0
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
                        self.dmax  = int(line.split(' ')[2])
                        print("Distancia maxima ate UPA mais proxima: {}".format(self.dmax1))
                        print("Distancia maxima ate segunda UPA mais proxima: {}".format(self.dmax2))
                        print("Distancia maxima entre 2 UPAs: {}".format(self.dmax))
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

# def achar_caminho(start, matriz):
#     atual = start
#     candidato = tuple(-1, 999) # (indice do distrito, distancia em relação ao atual)
#     candidato2 = tuple(-1, 999)
#     upas = set()

#     # achar menor distancia entre vizinhos
#     for i in range(len(matriz[0]):
#         if i == atual:
#             continue
        
#         if matriz[atual][i] < candidato[1]:
#             candidato[0], candidato[1] = i, matriz[atual][i]

#         if matriz[atual][i] > candidato[1] and matriz[atual][i] < candidato2[1]
#             candidato2[0], candidato2[1] = i, matriz[atual][i]

#     if candidato[1] < 30 and candidato2[1] < 60 and matriz[candidato[0]][candidato2[0]] >= 90:
#         array[candidato[0]] = 1
     

#     return

# def algoritmo_construtivo(matriz):
#     for i in range(len(matriz[0])):
#         achar_caminho(i, matriz)

#     return


instance = Instance("instance4.data")
matriz_distancias = criar_matriz(instance.numeroDistritos, instance.distritos)

for i in matriz_distancias:
    print(i)

# algoritmo_construtivo(matriz_distancias)