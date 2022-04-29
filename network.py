class Network:
    def __init__(self, name):
        self.name = name
        self.variables = dict()

    def add_variable(self, var):
        self.variables[var.name] = var

    def add_request(self, rq):
        self.request = rq

    def __str__(self):
        txt = "network name : " + self.name
        txt += "\nvariables : " + self.variables

class Variable:
    def __init__(self, name):
        self.name = name
        self.sachants = list()
        self.proba = dict()

    def add_sachant(self, sachant):
        self.sachants.append(sachant)
    
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
    def __init__(self, var):
        self.var = var
        self.sachants = dict()
        self.proba = dict()

    def add_sachant(self, sachant, state):
        self.sachants[sachant] = state

    def add_proba(self, proba, key):
        self.proba[key] = proba

    def __str__(self):
        txt = "Variable for the proba : " + self.var.name
        txt += "\n knowing : "
        for s in self.sachants:
            txt += s.name + "=" + self.sachants[s] + ", "
        txt += "\nexact probability : "
        txt += "1=" + self.proba[1] + ", "
        txt += "0=" + self.proba[0]
        return txt
            
