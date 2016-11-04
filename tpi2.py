# encoding: utf8
# 76771, Daniela Simoes
from functools import reduce

from tree_search import *
from semnet import *
from collections import Counter


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
        if obj not in self.getObjects():
            return []

        types = [x.relation.entity2 for x in self.declarations if (isinstance(x.relation, Association) and
                                                                   ((x.relation.cardin == 'one' and
                                                                     x.relation.default == obj))) or
                 (isinstance(x.relation, Member) and x.relation.entity1 == obj)]

        assoc_names_entity1 = list(set([x.relation.name for x in self.declarations if isinstance(x.relation, Association)  and x.relation.cardin is None and x.relation.entity1 == obj ]))

        for assoc_name in assoc_names_entity1:
            types += [x.relation.entity1 for x in self.declarations if isinstance(x.relation, Association) and x.relation.cardin is not None and x.relation.name==assoc_name]

        assoc_names_entity2 = list(set([x.relation.name for x in self.declarations if isinstance(x.relation, Association)  and x.relation.cardin is None and x.relation.entity2 == obj]))

        for assoc_name in assoc_names_entity2:
            types += [x.relation.entity2 for x in self.declarations if isinstance(x.relation, Association) and x.relation.cardin is not None and x.relation.name==assoc_name]

        return [(x[0], x[1]/len(types)) for x in list(Counter(types).items())]

    # Insere uma nova relação "rel" declarada por "user".
    # Se a relação for uma associação fluente entre objectos,
    # tem que fazer a gestão do intervalo de tempo
    # em que a associação se mantém verdadeira
    def insert2(self, user, rel):
        if not isinstance(rel, Association):
            return None

        self.tick += len(rel.name) # simula a passagem do tempo
        self.declarations.append(Declaration(user,rel))


class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth',detect_repeated=False):
        SearchTree.__init__(self, problem, strategy, detect_repeated)
        self.optimizations = []

    def optimize(self, idx=0):
        # if idx is higher or equal to lenght(self.result) - 2 it ends
        if idx >= len(self.solution) - 2:
            return
        #see the possible actions for the self.result[idx] (ex: actions in Lisboa)
        actions = self.problem.domain.actions(self.solution[idx])
        #hop (ex: Lisboa, Evora)
        hop = self.solution[idx], self.solution[idx + 2]

        #if the hop exists in the possible actions will delete the idx + 1 state
        if hop in actions:
            self.optimizations += [hop]
            del self.solution[idx + 1]
            #and calls the self.optimize() again
            self.optimize()
        self.optimize(idx + 1)
        return self.solution
