#include <cmath>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#define DEBUG_IMPORT

using namespace std;

struct District {
    int id = -1;
    int latitude = 0;
    int longitude = 0;
};

struct Instance {
    vector<int> x;
    int numeroDistritos = 0;
    int dmax1 = 0;
    int dmax2 = 0;
    int dmax  = 0;
    vector<District> districts;
};

Instance import(const std::string& filename) {
    Instance instance;
    ifstream ifs(filename.c_str(), ios::in);
    string line;
    vector<int> x;
    vector<int> y;
    if (ifs.is_open()) {
        getline(ifs, line); // # Numero de destritos
        getline(ifs, line);
        instance.numeroDistritos = atoi(line.c_str());
        getline(ifs, line); // # Linha em branco
        getline(ifs, line); // # Distancia maxima ate UPA mais proxima | Distancia maxima ate segunda UPA mais proxima | Distancia maxima entre 2 UPAs
        getline(ifs, line, ' '); instance.dmax1 = atoi(line.c_str());
        getline(ifs, line, ' '); instance.dmax2 = atoi(line.c_str());
        getline(ifs, line, ' '); instance.dmax = atoi(line.c_str());
        getline(ifs, line, ' '); // # Linha em branco
        getline(ifs, line); // # ID do destrito | latitude | longitude
        while (ifs.good()) {
            District district;
            getline(ifs, line, ' ');
            district.id = atoi(line.c_str());
            getline(ifs, line, ' ');
            district.latitude = atoi(line.c_str());
            getline(ifs, line, '\n');
            district.longitude = atoi(line.c_str());
            instance.districts.push_back(district);
        }
        ifs.close();
    }
#ifdef DEBUG_IMPORT
    clog << "Numero de distritos: " << instance.numeroDistritos << endl;
    clog << "Distancia maxima ate UPA mais proxima: " << instance.dmax1 << endl;
    clog << "Distancia maxima ate segunda UPA mais proxima: " << instance.dmax2 << endl;
    clog << "Distancia maxima entre 2 UPAs: " << instance.dmax << endl;
    for (std::vector<District>::iterator it = instance.districts.begin(); it != instance.districts.end(); it++) {
        clog << "Id: " << it->id << "\tLatitude: " << it->latitude << "\tLongitude: " << it->longitude << endl;
    }
    clog << "Distritos: " << instance.districts.size() << endl;
#endif
    return instance;
}

vector<vector<int> > criarMatriz(int numeroDistritos, vector<District> distrito) {
    vector<vector<int> > matriz(numeroDistritos, vector<int>(numeroDistritos));

    for(int i = 0; i < numeroDistritos; i++){
        for(int j = 0; j < numeroDistritos; j++){
            matriz.at(i).at(j) = 0;
        }
    }

    for(int i = 0; i < numeroDistritos; i++){
        for(int j = 0; j < numeroDistritos; j++){
            //Quando tiver checando o mesmo distrito a dist dele com ele mesmo é 0
            if(i == j){
                matriz.at(i).at(j) = 0;
                continue;
            }
            //se tiver checando um distrito que nao foi calculado ainda calcula a distancia dele
            else if(j > i){
                int dist = sqrt(pow(distrito.at(i).latitude - distrito.at(j).latitude, 2) + pow(distrito.at(i).longitude - distrito.at(j).longitude, 2));
                //clog << i << ", " << j << " dist: " << dist << endl;
                matriz.at(i).at(j) = dist;
            }
            //se tiver checando um distrito que ja foi calculado pega a distancia que já foi calculada.
            else{
                matriz.at(i).at(j) = matriz.at(j).at(i);
            }
        }
    }

    return matriz;
}

void printMatriz(int numeroDistritos, vector<vector<int> > matriz){
    for(int i = 0; i < numeroDistritos; i++){
        for(int j = 0; j < numeroDistritos; j++){
            cout << matriz.at(i).at(j) << " ";
        }
        cout << endl;
    }
}

int main(){
    Instance instance = import("instance1.data");
    vector<vector<int> > matrizDist;
    // int distUpaMaisProx, dist2UpaMaisProx, distanciaMax;

    matrizDist = criarMatriz(instance.numeroDistritos, instance.districts);

     //matrizDist = criarMatriz(instance);
     printMatriz(instance.numeroDistritos, matrizDist);

    return 0;
}
