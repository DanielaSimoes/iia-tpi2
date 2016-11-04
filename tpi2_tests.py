#encoding: utf8

from tpi2 import *


# ----------------------------------------------------------
# Exemplo de rede semantica
# ----------------------------------------------------------


z = MySemNet()

z.insert('descartes',Association('socrates','professor','filosofia'))
z.insert('descartes',Subtype('mamifero','vertebrado'))
z.insert('descartes',Subtype('homem','mamifero'))
z.insert('descartes',Association('socrates','professor','matematica'))
z.insert('descartes',Member('platao','homem'))
z.insert('descartes',Association('platao','professor','filosofia'))
z.insert('descartes',Association('socrates','peso',80))
z.insert('descartes',Member('socrates','homem'))
z.insert('descartes',Member('aristoteles','homem'))
z.insert('descartes',Association('mamifero','altura','number','one',1.2))
z.insert('descartes',Association('socrates','altura',1.85))

z.insert('darwin',Subtype('homem','mamifero'))
z.insert('darwin',Subtype('mamifero','vertebrado'))
z.insert('darwin',Association('homem','pulsacao','number','one'))
z.insert('darwin',Association('homem','progenitor','homem','many'))

z.insert('simao',Association('socrates','professor','matematica'))
z.insert('simao',Association('platao','professor','filosofia'))
z.insert('simao',Association('sofronisco','progenitor','socrates'))

z.insert('simoes',Association('socrates','professor','matematica'))

z.insert('damasio',Member('socrates','filosofo'))
z.insert('damasio',Association('homem','pulsacao','numero','one'))

z.insert('tracker',Association('agent','at','cell','one',(0,0),True))

z.query_local()
z.show_query_result()

print("\n---------------------------------\n")

lobj = z.getObjects()
print("Current objects: {0}".format(lobj))

print("\n---------------------------------\n")

print("Types of altura: {0}".format(z.getAssocTypes('altura')))
print("Types of pulsacao: {0}".format(z.getAssocTypes('pulsacao')))

print("\n---------------------------------\n")


for x in lobj:
    print("Types of {0}: {1}".format(x,z.getObjectTypes(x)))

print("\n---------------------------------\n")


#z.insert2('tracker',Association('agent','at','cell','one',(0,0),True))
for i in range(10): # snake permanece numa celula durante algumas
                    # iteracoes, e depois muda para outra
    cell = (1,2) if i<7 else (2,3)
    z.insert2('tracker',Association('snake','at',cell))
z.query_local(rel='at')
z.show_query_result()

print("\n---------------------------------\n")
"""

# -------------------------------------------------------------
# Dominio de aplicacao para exercicios sobre pesquisa em arvore
# -------------------------------------------------------------

class Cidades(SearchDomain):
    def __init__(self,connections, coordinates):
        self.connections = connections
        self.coordinates = coordinates
    def actions(self,Cidade):
        actlist = []
        for (C1,C2,D) in self.connections:
            if (C1==Cidade):
                actlist += [(C1,C2)]
            elif (C2==Cidade):
               actlist += [(C2,C1)]
        return actlist 
    def result(self,state,action):
        (C1,C2) = action
        if C1==state:
            return C2
    def cost(self,state,action):
        (A,B) = action
        if A != state:
            return None
        for (P,Q,D) in self.connections:
            if (P==A and Q==B) or (P==B and Q==A):
                return D
        return None

cidades_portugal = Cidades( 
                    # Ligacoes por estrada
                    [
                      ('Coimbra', 'Leiria', 73),
                      ('Aveiro', 'Agueda', 35),
                      ('Porto', 'Agueda', 79),
                      ('Agueda', 'Coimbra', 45),
                      ('Viseu', 'Agueda', 78),
                      ('Aveiro', 'Porto', 78),
                      ('Aveiro', 'Coimbra', 65),
                      ('Figueira', 'Aveiro', 77),
                      ('Braga', 'Porto', 57),
                      ('Viseu', 'Guarda', 75),
                      ('Viseu', 'Coimbra', 91),
                      ('Figueira', 'Coimbra', 52),
                      ('Guarda', 'Castelo Branco', 96),
                      ('Leiria', 'Castelo Branco', 169),
                      ('Figueira', 'Leiria', 62),
                      ('Leiria', 'Santarem', 78),
                      ('Santarem', 'Lisboa', 82),
                      ('Santarem', 'Castelo Branco', 160),
                      ('Castelo Branco', 'Viseu', 174),
                      ('Santarem', 'Evora', 122),
                      ('Lisboa', 'Evora', 132),
                      ('Evora', 'Beja', 80),
                      ('Lisboa', 'Beja', 178),
                      ('Faro', 'Beja', 147) ],

                    # Coordenadas das cidades:
                     { 'Aveiro': (41,215),
                       'Figueira': ( 24, 161),
                       'Coimbra': ( 60, 167),
                       'Agueda': ( 58, 208),
                       'Viseu': ( 104, 217),
                       'Braga': ( 61, 317),
                       'Porto': ( 45, 272),
                       'Lisboa': ( 0, 0),
                       'Santarem': ( 38, 59),
                       'Leiria': ( 28, 115),
                       'Castelo Branco': ( 140, 124),
                       'Guarda': ( 159, 204),
                       'Evora': (120, -10),
                       'Beja': (125, -110),
                       'Faro': (120, -250)
                     } )


p = SearchProblem(cidades_portugal,'Lisboa','Faro')
t = MyTree(p,'depth')
print("Solution: {0}".format(t.search()))
print("Optimized: {0}".format(t.optimize()))
print("Optimizations: {0}".format(t.optimizations))


"""
