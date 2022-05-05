import random

def tirage(proba_true):
    #retourne 1 si true et 0 si false
    x = random.random()
    #de 0 à proba true -> true sinon false
    if(x <= float(proba_true)):
        return 1
    return 0

class Likelihood_weighting:
    def __init__(self, n):
        self.network = n

    def echantillon(self):
        w = 1
        var_fixed = dict()
        for name, var in self.network.variables.items():
            var_fixed[name] = -1
        for sachant, state in self.network.request.sachants.items():
            var_fixed[sachant.name] = int(state)
        for name, var in self.network.variables.items():
            if(var_fixed[name] == -1):
                if(len(var.sachants) == 0):
                    resultat = tirage(var.proba["null"][0])
                    var_fixed[name] = resultat
                else:
                    prob = ""
                    for sachant in var.sachants:
                        prob += str(var_fixed[sachant.name])
                    resultat = tirage(var.proba[prob][0])
                    var_fixed[name] = resultat
            else:
                if(len(var.sachants) == 0):
                    w = w * float(var.proba["null"][1 - var_fixed[name]])
                else:
                    prob = ""
                    for sachant in var.sachants:
                        prob += str(var_fixed[sachant.name])
                    w = w * float(var.proba[prob][1 - var_fixed[name]])
        return var_fixed, w
                    

    def solve(self, nbr_echant):
        echantillons = dict()
        compte = [0,0] #case 0: false et case 1: true
        resultat = [0,0]
        total = 0
        for i in range(nbr_echant):
            e, w = self.echantillon()
            if(e[self.network.request.var.name] == 0):
                compte[0] += w
            else:
                compte[1] += w
            total += w
        resultat[0] = compte[0]/total
        resultat[1] = compte[1]/total
        #print('résultat trouvé pour likelihood weighting: ' + str(resultat))
        return resultat
            
            
        
