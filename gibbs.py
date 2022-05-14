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
    # etat : l'état des variables que l'on va tenter de perturber
    # var_to_fix : liste des variables non observées dans la requête à fixer
    # return : - un tableau qui compte le nombre d'occurences des valeurs de la variable de la requête
    #          - l'état de l'échantillon à la fin de sa perturbation
    def echantillon(self, etat, var_to_fix):
        compte = [0, 0] #case 0 pour les false et case 1 pour les true
        random.shuffle(var_to_fix)
        for var in var_to_fix:
            prob = self.list_sachants_var(var, etat)
            children = list()
            for name, var_for in self.network.variables.items():
                if(var in var_for.sachants):
                    children.append(var_for)
            tab_proba = [0, 0]
            for i in range(2):
                tab_proba[i] = float(var.proba[prob][i])
                etat[var.name] = i
                for c in children:
                    tab_proba[i] *= float(c.proba[self.list_sachants_var(c, etat)][etat[c.name]])
            #normalisation
            tt = tab_proba[0] + tab_proba[1]
            tab_proba[0] = tab_proba[0] / tt
            tab_proba[1] = tab_proba[1] / tt
            #tirage
            resultat = tirage(tab_proba[1])
            #maj
            etat[var.name] = resultat
            compte[etat[self.network.request.var.name]] += 1
        return compte, etat

    # La fonction principale. Elle s'occupe de générer le nombre d'échantillons demandé
    # et de calculer ensuite la moyenne des probas pour chacune des valeurs
    # nbr_echant : un entier représentant le nombre d'échantillons à générer
    #       ce nombre peut être changé par l'utilisateur à sa guise dans main.py
    def solve(self, nbr_echant):
        etat = dict()
        var_to_fix = list()
        for name, var in self.network.variables.items():
            if(var in self.network.request.sachants.keys()):
                etat[name] = int(self.network.request.sachants[var])
            else:
                etat[name] = tirage(0.5)
                var_to_fix.append(var)
        compte = list()
        for i in range(nbr_echant):
            compte_temp, etat = self.echantillon(etat, var_to_fix)
            compte.append(compte_temp)
        resultat = [0, 0]
        for c in compte:
            resultat[0] += c[0]
            resultat[1] += c[1]
        total = resultat[0] + resultat[1]
        resultat[0] = resultat[0] / total
        resultat[1] = resultat[1] / total
        #print("resultat trouvé avec Gibbs : " + str(resultat))
        return resultat

