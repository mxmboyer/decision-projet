import random

def tirage(proba_true):
    #retourne 1 si true et 0 si false
    x = random.random()
    #de 0 à proba true -> true sinon false
    if(x <= float(proba_true)):
        return 1
    return 0

class Reject:
    # Constructeur de la classe Rejet qui implémente la méthode des rejets
    # n : un réseau instance de la classe Network
    def __init__(self, n):
        self.network = n

    # Tire au sort l'état des variables du réseau en respectant les probabilités
    # return : un dictionnaire avec les variables et leur état respectif
    def echantillon(self):
        var_fixed = dict()
        tab_var_racine = list()
        tab_var = list()
        for name, var in self.network.variables.items():
                var_fixed[name] = -1
        for name, var in self.network.variables.items():
            if(len(var.sachants) == 0):
                resultat = tirage(var.proba["null"][1])
                var_fixed[name] = resultat
            else:
                prob = ""
                for sachant in var.sachants:
                    prob += str(var_fixed[sachant.name])
                resultat = tirage(var.proba[prob][1])
                var_fixed[name] = resultat
        return var_fixed

    # Fonction principale de la méthode des rejets
    # Elle vérifie que les échantillons tirés respectent les variables observées de la requête avant de les garder
    # Elle cumulera tous les échantillons en les normalisant pour approximer les probabilités de la requête
    # nbr_echant : un entier représentant le nombre d'échantillons voulu par l'utilisateur
    # return : un tableau de deux nombres représentant les probabilités normalisées
    def solve(self, nbr_echant):
        echantillons = list()
        compte = [0,0] #case 0: false et case 1: true
        resultat = [0,0]
        while(len(echantillons) < nbr_echant):
            e = self.echantillon()
            ok = 0
            for var, result in e.items():
                for sachant, state in self.network.request.sachants.items():
                    if(var == sachant.name and str(result) == state):
                        ok += 1
            if(ok == len(self.network.request.sachants)):    
                echantillons.append(e)
        for e in echantillons:
            if(e[self.network.request.var.name] == 0):
                compte[0] += 1
            else:
                compte[1] += 1
        resultat[0] = compte[0]/nbr_echant
        resultat[1] = compte[1]/nbr_echant
        #print('résultat trouvé avec les rejets: ' + str(resultat))
        return resultat
        

            
