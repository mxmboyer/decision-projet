import random
import time
import pandas as pd

from network import *

from rejet import *
from gibbs import *
from gibbs_analyse import *
from likelihood_weighting import *


# Cette fonction s'occupe de lire les données d'un fichier
# file_name : une chaîne de caractères contenant le chemin du fichier à lire
# return : un liste d'instances de la classe Network
def read_file(file_name):
    networks = list()
    f = open(file_name, "r")
    lines = f.readlines()
    for n in range(len(lines)):
        line = lines[n]
        if(line.split()[0] == "network"):
            net = Network(line.split()[1])
            networks.append(net)
            read_network(net, lines, n)
    f.close()
    return networks

# Cette fonction s'occupe de lire les informations d'un réseau et de mettre ces informations
# dans une instance de la classe Network
# network : une instance de la classe Network dans laquelle les informations du réseau seront rentrées
# lines : une liste contenant les lignes du fichier à lire
# n : un entier permettant de savoir à quelle ligne en est la lecture
def read_network(network, lines, n):
    while(n < len(lines)):
        line = lines[n]
        line_split = line.split()
        if(line_split[0] == "variable"):
            var = Variable(line_split[1])
            network.add_variable(var)
        elif(line_split[0] == "probability"):
            if line_split[3] == ")":
                probaline = lines[n+1].split()
                tabproba = [
                    probaline[2].split(";")[0],
                    probaline[1].split(",")[0]
                ]
                network.variables[line_split[2]].add_proba(tabproba)
            else:
                i = 4
                var = network.variables[line_split[2]]
                while(line_split[i] != ")"):
                    var.add_sachant(network.variables[line_split[i].split(",")[0]])
                    i += 1
                nn = n+1
                while(lines[nn] != "}\n"):
                    probaline = lines[nn].split(")")
                    cond = probaline[0].strip().split("(")[1].split(", ")
                    txt = ""
                    for c in cond:
                        if(c == "True"):
                            txt += "1"
                        elif(c == "False"):
                            txt += "0"
                        else:
                            print("erreur lecture sachants probabilité")
                    tabproba = [
                        txt,
                        probaline[1].split()[1].split(";")[0],
                        probaline[1].split()[0].split(",")[0]
                    ]
                    var.add_proba(tabproba)
                    nn += 1
        elif(line.split("(")[0] == "Prob"):
            l = ""
            for ll in line_split:
                l += ll
            var = network.variables[l.split("|")[0].split("(")[1]]
            rq = Request(var)
            tab_sachants = l.split("|")[1].split(")")[0].split(",")
            for ts in tab_sachants:
                sachant = network.variables[ts.split("=")[0]]
                if(ts.split("=")[1].lower() == "true" or ts.split("=")[1].lower() == "1"):
                    rq.add_sachant(sachant, "1")
                elif(ts.split("=")[1].lower() == "false" or ts.split("=")[1].lower() == "0"):
                    rq.add_sachant(sachant, "0")
            probas = l.split("[")[1].split("]")[0].split(",")
            rq.add_proba(probas[0], 0)
            rq.add_proba(probas[1], 1)
            network.add_request(rq)
            break
        n += 1

test = read_file("bn.bif")
reseau = 2
nbr_echantillons = 1000000

print(test[reseau].request)

'''
        # Exemples d'utilisation des différentes méthodes
        
gibbs = Gibbs(test[reseau])
gibbs.solve(nbr_echantillons)

likelihood_weighting = Likelihood_weighting(test[reseau])
likelihood_weighting.solve(nbr_echantillons)

rej = Reject(test[reseau])
rej.solve(100)
'''

'''
        #Analyse de la performance des méthodes

for r in range(1, 5):
    rej = Reject(test[r])
    resultat = list()
    n = 0
    while(n < nbr_echantillons):
        resultat.append(rej.solve(1000))
        n += 1000
    df_rej = pd.DataFrame(resultat, columns=["prob_false", "prob_true"])
    df_rej.to_csv("rejet_" + test[r].name + ".csv", index=False)

for r in range(5):
    likelihood_weighting = Likelihood_weighting(test[r])
    resultat = list()
    n = 0
    while(n < nbr_echantillons):
        resultat.append(likelihood_weighting.solve(1000))
        n += 1000
    df_lw = pd.DataFrame(resultat, columns=["prob_false", "prob_true"])
    df_lw.to_csv("lw_" + test[r].name + ".csv", index=False)

for r in range(5):
    gibbs = Gibbs_Analyse(test[r])
    resultat = gibbs.solve(nbr_echantillons, 1000)
    df_g = pd.DataFrame(resultat, columns=["prob_false", "prob_true"])
    df_g.to_csv("gibbs_" + test[r].name + ".csv", index=False)



        # Analyse du temps d'exécution des méthodes
        
for r in range(5):
    likelihood_weighting = Likelihood_weighting(test[r])
    resultat = list()
    n = 1000
    while(n < nbr_echantillons):
        start = time.time()
        likelihood_weighting.solve(n)
        temps = time.time() - start
        resultat.append(temps)
        n += 1000
    df_lw = pd.DataFrame(resultat, columns=["temps_execution"])
    df_lw.to_csv("lw_time_" + test[r].name + ".csv", index=False)

for r in range(5):                  
    gibbs = Gibbs(test[r])                   
    resultat = list()
    n = 1000
    while(n < nbr_echantillons):
        start = time.time()
        gibbs.solve(n)
        temps = time.time() - start
        resultat.append(temps)
        n += 1000
    df_g = pd.DataFrame(resultat, columns=["temps_execution"])
    df_g.to_csv("gibbs_time_" + test[r].name + ".csv", index=False)

for r in range(1, 2):
    rej = Reject(test[r])
    resultat = list()
    n = 100000
    while(n <= 1000000):
        start = time.time()
        rej.solve(n)
        temps = time.time() - start
        resultat.append(temps)
        n += 100000
    df_rej = pd.DataFrame(resultat, columns=["temps_execution"])
    df_rej.to_csv("rejet_time_" + test[r].name + ".csv", index=False)
'''
