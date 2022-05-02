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
        for var in self.network.ordre_var:
            var_fixed[var.name] = -1
            for sachant, state in self.network.request.sachants.items():
                if(var.name == sachant.name):
                    var_fixed[var.name] = int(state)
                    break
        for var in self.network.ordre_var:
            if(var_fixed[var.name] == -1):
                if(len(var.sachants) == 0):
                    resultat = tirage(var.proba["null"][0])
                    var_fixed[var.name] = resultat
                else:
                    prob = ""
                    for sachant in var.sachants:
                        prob += str(var_fixed[sachant.name])
                    resultat = tirage(var.proba[prob][0])
                    var_fixed[var.name] = resultat
            else:
                if(len(var.sachants) == 0):
                    w = w * float(var.proba["null"][var_fixed[var.name]])
                else:
                    prob = ""
                    for sachant in var.sachants:
                        prob += str(var_fixed[sachant.name])
                    w = w * float(var.proba[prob][var_fixed[var.name]])
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
        resultat[0] = compte[1]/total
        resultat[1] = compte[0]/total
        print('résultat trouvé pour likelihood weighting: ' + str(resultat))
            
            
        
