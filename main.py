import random

from network import *

from rejet import *

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
                        probaline[1].split()[0].split(",")[0],
                        probaline[1].split()[1].split(";")[0]
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
            rq.add_proba(probas[0], 1)
            rq.add_proba(probas[1], 0)
            network.add_request(rq)
            break
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
#print(test[0].variables["Alarm"].name)
#print(test[0].variables["Alarm"].sachants)
#print(test[0].variables["Alarm"].proba)

rej = Reject(test[2])
rej.solve(10)
