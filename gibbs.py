import random

def tirage(proba_true):
    #retourne 1 si true et 0 si false
    x = random.random()
    #de 0 à proba true -> true sinon false
    if(x <= float(proba_true)):
        return 1
    return 0

class Gibbs:
    # Constructeur de la classe Gibbs qui implémente l'échantillonnage de Gibbs
    # n : une instance de la classe Network (voir network.py pour l'implémentation d'un réseau)
    def __init__(self, n):
        self.network = n

    def list_sachants_var(self, var, tab_var):
        prob = ""
        if(len(var.sachants) == 0):
            prob = "null"
        else:
            for sachant in var.sachants:
                prob += str(tab_var[sachant.name])
        return prob

    # Implémentation du tirage d'un échantillon avec la méthode de Gibbs
    # return : une liste de 2 entiers :
    #       - le 1er représente la proba normalisé du false pour cet échantillon
    #       - le 2e représente la proba normalisé du true pour cet échantillon
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
            prob = self.list_sachants_var(var, tab_var)
            children = list()
            for name, var_for in self.network.variables.items():
                if(var in var_for.sachants):
                    children.append(var_for)
            tab_proba = [0, 0]
            for i in range(2):
                tab_proba[i] = float(var.proba[prob][1-i])
                for c in children:
                    tab_proba[i] *= float(c.proba[self.list_sachants_var(c, tab_var)][1-i])
            #normalisation
            tt = tab_proba[0] + tab_proba[1]
            tab_proba[0] = tab_proba[0] / tt
            tab_proba[1] = tab_proba[1] / tt
            #tirage
            resultat = tirage(tab_proba[1])
            #maj
            var_fixed[var.name] = resultat
            tab_var[var.name] = resultat
            compte[tab_var[self.network.request.var.name]] += 1
        total = compte[0] + compte[1]
        compte[0] = compte[0] / total
        compte[1] = compte[1] / total
        return compte

    # La fonction principale. Elle s'occupe de générer le nombre d'échantillons demandés
    # et de calculer ensuite la moyenne des probas pour chacune des valeurs
    # nbr_echant : un entier représentant le nombre d'échantillons à générer
    #       ce nombre peut être changé par l'utilisateur à sa guise dans main.py
    def solve(self, nbr_echant):
        echantillons = list()
        while(len(echantillons) < nbr_echant):
            echantillons.append(self.echantillon())
        resultat = [0, 0]
        for e in echantillons:
            resultat[0] += e[0]
            resultat[1] += e[1]
        resultat[0] = resultat[0] / nbr_echant
        resultat[1] = resultat[1] / nbr_echant
        #print("resultat trouvé avec Gibbs : " + str(resultat))
        return resultat

