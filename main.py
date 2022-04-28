import random

from network import *

def read_file():
    networks = list()
    f = open("bn.bif", "r")
    lines = f.readlines()
    for n in range(len(lines)):
        line = lines[n]
        if(line.split()[0] == "network"):
            net = Network(line.split()[1])
            networks.append(net)
            read_network(net, lines, n)
    f.close()
    return networks

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
                    probaline[1].split(",")[0],
                    probaline[2].split(";")[0]
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
                    tabproba = [
                        probaline[0].strip() + ")",
                        probaline[1].split()[0].split(",")[0],
                        probaline[1].split()[1].split(";")[0]
                    ]
                    var.add_proba(tabproba)
                    nn += 1
        elif(line_split[0] == "Prob("):
            pass #revenir sur read_file après
        n += 1


def tirage(proba_true):
    #retourne 1 si true et 0 si false
    x = random.random()
    #de 0 à proba true -> true sinon false
    if(x<=proba_true):
        return 1
    return 0
    
    
#en param: la variable a tirer et les variables fixées si existantes

def tirage_var(variables):
    return int(random.random() * len(variables))

test = read_file()
print(test[0].variables["Alarm"].name)
print(test[0].variables["Alarm"].sachants)
print(test[0].variables["Alarm"].proba)
