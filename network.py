class Network:
    def __init__(self, name):
        self.nom = name
        self.variables = dict()

    def add_variable(self, var):
        self.variables[var.name] = var


class Variable:
    def __init__(self, name):
        self.name = name
        self.sachants = dict()
        self.proba = dict()

    def add_sachant(self, sachant):
        self.sachants[sachant.name] = sachant
    
    def add_proba(self, proba):
        if(len(self.sachants) == 0):
            self.proba = proba
        else:
            self.proba[proba[0]] = [proba[1], proba[2]]
