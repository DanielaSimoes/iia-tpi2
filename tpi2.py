# encoding: utf8
# 76771, Daniela Simoes
from functools import reduce

from tree_search import *
from semnet import *


class MySemNet(SemanticNetwork):
    def __init__(self, ldecl=[]):
        SemanticNetwork.__init__(self, ldecl)

    # Devolve lista de todos os objectos existentes na rede
    def getObjects(self):
        return list(set(reduce(lambda h, r: h + [r.entity1] + [r.entity2] if r.cardin is None else h + [
            r.default] if r.cardin == 'one' and r.default is not None else h,
                               [x.relation for x in self.declarations if isinstance(x.relation, Association)], []) + [
                            d.relation.entity1 for d in self.declarations if isinstance(d.relation, Member)]))

    # Devolve, para o nome de associação dado, uma lista de tuplos
    # (t1,t2,freq), em que:
    #   t1 - tipo da primeira entidade da associação
    #   t2 - tipo da segunda entidade da associação
    #   freq - frequência relativa com que ocorre
    def getAssocTypes(self, assocname):
        objs = self.getObjects()
        relations = [x.relation for x in self.declarations if isinstance(x.relation, Association) and x.relation.name==assocname and x.relation.entity1 not in objs and x.relation.entity2 not in objs]

        count = {}
        total_ocur = 0

        for relation in relations:
            if (relation.entity1, relation.entity2) not in count:
                count[(relation.entity1, relation.entity2)] = 1
            else:
                count[(relation.entity1, relation.entity2)] += 1

            total_ocur += 1

        return [(key)+(value/total_ocur,) for key, value in count.items()]

    # Devolve uma lista de tuplos (t,freq) para o objecto dado,
    # em que:
    #    t - tipo do objecto
    #    freq - frequência com que ocorre
    def getObjectTypes(self, obj):
        # sabendo o obj, vamos procurar declaracoes em que obj esta em e1 ou em e2
        decs = self.query_local(e1=obj) + self.query_local(e2=obj)

        # vamos saber das declaracoes encontradas, quais são as "Member"
        members = []

        for dec in decs:
            if isinstance(dec.relation, Member):
                members += dec.relation

        print("")
        pass
        # IMPLEMENTAR AQUI

    # Insere uma nova relação "rel" declarada por "user".
    # Se a relação for uma associação fluente entre objectos,
    # tem que fazer a gestão do intervalo de tempo
    # em que a associação se mantém verdadeira
    def insert2(self, user, rel):
        self.tick += len(rel.name)  # simula a passagem do tempo
        pass
        # IMPLEMENTAR AQUI


class MyTree(SearchTree):
    # optimizar e devolver uma solucao previamente
    # guardada em self.solution
    def optimize(self):
        pass
        # IMPLEMENTAR AQUI
