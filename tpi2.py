#encoding: utf8
# 76771, Daniela Simoes
from functools import reduce

from tree_search import *
from semnet import *


class MySemNet(SemanticNetwork):
    def __init__(self,ldecl=[]):
        SemanticNetwork.__init__(self,ldecl)


    # Devolve lista de todos os objectos existentes na rede
    def getObjects(self):
        # obter todas as associações da lista de declarações
        associations = [x.relation for x in self.declarations if isinstance(x.relation, Association)]

        # determinar quais são os objetos, iso é obtido através de cardin=None, em que entity1 e entity2 são necessariamente
        # nomes de objetos
        objetos = list(set(reduce(lambda h, r: h + [r.entity1] + [r.entity2] if r.cardin is None else h, associations, [])))

        # perceber de que tipo esses objetos são
        print("")
        # saber many, one e saber os valores que podemos atribuir

        objs = set()

        for association in associations:
            if association.cardin is None:
                objs.add(association.entity1)
                objs.add(association.entity2)
            continue
            if association.cardin != 'one':
                objs.add(association.entity1)
                objs.add(association.entity2)
            elif association.default is not None:
                objs.add(association.entity1)
                objs.add(association.default)

        return list(objs)

    # Devolve, para o nome de associação dado, uma lista de tuplos 
    # (t1,t2,freq), em que:
    #   t1 - tipo da primeira entidade da associação
    #   t2 - tipo da segunda entidade da associação
    #   freq - frequência relativa com que ocorre
    def getAssocTypes(self,assocname):
        pass
        # IMPLEMENTAR AQUI


    # Devolve uma lista de tuplos (t,freq) para o objecto dado, 
    # em que:
    #    t - tipo do objecto
    #    freq - frequência com que ocorre
    def getObjectTypes(self,obj):
        pass
        # IMPLEMENTAR AQUI

    # Insere uma nova relação "rel" declarada por "user".
    # Se a relação for uma associação fluente entre objectos,
    # tem que fazer a gestão do intervalo de tempo
    # em que a associação se mantém verdadeira
    def insert2(self,user,rel):
        self.tick += len(rel.name)   # simula a passagem do tempo
        pass
        # IMPLEMENTAR AQUI




class MyTree(SearchTree):

    # optimizar e devolver uma solucao previamente 
    # guardada em self.solution
    def optimize(self):
        pass
        # IMPLEMENTAR AQUI


