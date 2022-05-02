import random

def tirage(proba_true):
    #retourne 1 si true et 0 si false
    x = random.random()
    #de 0 à proba true -> true sinon false
    if(x <= float(proba_true)):
        return 1
    return 0

class Gibbs:
    def __init__(self, n):
        self.network = n

    def echantillon(self):
        var_fixed = dict()
        tab_var = dict()
        var_to_fix = list()
        compte = [0, 0] #case 0 pour les false et case 1 pour les true
        for name, var in self.network.variables.items():
            if(name in self.network.request.sachants.keys()):
                tab_var[name] = int(self.network.request.sachants[name])
                var_fixed[name] = int(self.network.request.sachants[name])
            else:
                tab_var[name] = tirage(0.5)
                var_fixed[name] = -1
                var_to_fix.append(var)
        random.shuffle(var_to_fix)
        for var in var_to_fix:
            prob = ""
            if(len(var.sachants) == 0):
                prob = "null"
            else:
                for sachant in var.sachants:
                    prob += str(tab_var[sachant.name])
            resultat = tirage(var.proba[prob][0])
            var_fixed[var.name] = resultat
            tab_var[var.name] = resultat
            compte[tab_var[self.network.request.var.name]] += 1
        total = compte[0] + compte[1]
        compte[0] = compte[0] / total
        compte[1] = compte[1] / total
        return compte
        
    def solve(self, nbr_echant):
        echantillons = list()
        while(len(echantillons) < nbr_echant):
            echantillons.append(self.echantillon())
        resultat = [0, 0]
        for e in echantillons:
            resultat[0] += e[1]
            resultat[1] += e[0]
        resultat[0] = resultat[0] / nbr_echant
        resultat[1] = resultat[1] / nbr_echant
        print("resultat trouvé avec Gibbs : " + str(resultat) + "\nrésultat exact : " + str(self.network.request.proba))

