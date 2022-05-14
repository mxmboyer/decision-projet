class Network:
    # Constructeur de la classe Network qui représente un réseau bayésien
    # name : une chaine de caractères représentant le nom du réseau 
    def __init__(self, name):
        self.name = name
        self.variables = dict()
        self.ordre_var = list()

    # Ajoute une variable dans le réseau bayésien
    # var : une instance de la classe Variable 
    def add_variable(self, var):
        self.variables[var.name] = var

    # Associe une requete au réseau bayésien
    # rq : une instance de la classe Request
    def add_request(self, rq):
        self.request = rq

    # Génère un texte donnant les caractéristiques du réseau
    # return : le texte
    def __str__(self):
        txt = "network name : " + self.name
        txt += "\nvariables : " + self.variables
        return txt

class Variable:
    # Constructeur de la classe Variable qui représente une variable du réseau bayésien
    # name : une chaine de caractères représentant le nom de la variable
    def __init__(self, name):
        self.name = name
        self.sachants = list()
        self.proba = dict()

    # Ajoute un parent à cette variable
    # sachant : une instance de la classe Variable
    def add_sachant(self, sachant):
        self.sachants.append(sachant)

    # Ajoute une probabilité à cette variable
    # proba : un tableau de 3 cases si la variable a des parents:
    #           la 1e case indique la valeur des parents (true ou false), la 2e la probabilité que la variable soit false et la 3e true
    #       un tableau de 2 cases si la variable n'a pas de parents :
    #           la 1e case indique la probabilité que la variable soit false et la 2e true
    def add_proba(self, proba):
        if(len(self.sachants) == 0):
            self.proba["null"] = proba
        else:
            self.proba[proba[0]] = [proba[1], proba[2]]

    
    def __str__(self):
        txt = "var name : " + self.name
        txt += "\nsachants : " + self.sachants
        txt += "\nproba : " + self.proba
        return txt

class Request:
    # Constructeur de la classe Request qui représente une requête d'un réseau bayésien
    # var : une instance de la classe Variable qui correspond à la variable dont la probabilité est recherchée
    def __init__(self, var):
        self.var = var
        self.sachants = dict()
        self.proba = dict()

    # Ajoute des variables observées à la requête
    # sachant : une instance de la classe Variable qui correspond à une variable observée
    # state : un caractère représentant l'état de cette variable observée
    def add_sachant(self, sachant, state):
        self.sachants[sachant] = state

    # Ajoute la probabilité véritable de cette requête
    # key : un entier : 0 pour la probabilité false et 1 pour true
    # proba : donne la valeur de la probabilité correspondante à la clé pour la requête
    def add_proba(self, proba, key):
        self.proba[key] = proba

    # Génère un texte donnant les caractéristiques de la requête
    # return : le texte
    def __str__(self):
        txt = "Variable for the proba : " + self.var.name
        txt += "\n knowing : "
        for s in self.sachants:
            txt += s.name + "=" + self.sachants[s] + ", "
        txt += "\nexact probability : "
        txt += "0=" + self.proba[0] + " , "
        txt += "1=" + self.proba[1]
        return txt
            
