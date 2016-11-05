# encoding: utf8
__author__ = "Daniela Pereira Simões"
__nmec__ = 76771

from functools import reduce
from tree_search import *
from semnet import *
from collections import Counter


class MySemNet(SemanticNetwork):
    def __init__(self, ldecl=[]):
        SemanticNetwork.__init__(self, ldecl)
        self.last_tick = self.tick

    # Devolve lista de todos os objectos existentes na rede
    def getObjects(self):
        # um objeto é:
        # para declarações do tipo Association:
        # - entity1 e entity2 se cardinalidade == None
        # - default se cardinalidade == "one" e esse valor != None
        # para declarações do tipo Member:
        # - entity1
        return list(set(reduce(lambda h, r: h + [r.entity1] + [r.entity2] if r.cardin is None else h +
                                [r.default] if r.cardin == 'one' and r.default is not None else h,
                                [x.relation for x in self.declarations if isinstance(x.relation, Association)], []) +
                        [d.relation.entity1 for d in self.declarations if isinstance(d.relation, Member)]))

    # Devolve, para o nome de associação dado, uma lista de tuplos
    # (t1,t2,freq), em que:
    #   t1 - tipo da primeira entidade da associação
    #   t2 - tipo da segunda entidade da associação
    #   freq - frequência relativa com que ocorre
    def getAssocTypes(self, assocname):
        objs = self.getObjects()

        # as relações devem ter nome == assocname
        # x.relation.entity1 e x.relation.entity2 não pode ser object, é apenas entre "tipos"
        relations = [(x.relation.entity1, x.relation.entity2) for x in self.declarations
                     if isinstance(x.relation, Association)
                     and x.relation.cardin is not None
                     and x.relation.name == assocname
                     and x.relation.entity1 not in objs
                     and x.relation.entity2 not in objs]

        return [(x[0][0], x[0][1], x[1]/len(relations)) for x in list(Counter(relations).items())]

    # Devolve uma lista de tuplos (t,freq) para o objecto dado,
    # em que:
    #    t - tipo do objecto
    #    freq - frequência com que ocorre
    def getObjectTypes(self, obj):
        if obj not in self.getObjects():
            return []

        # - se a relação for do tipo Association e a cardin == "one" e o valor default == obj, quer dizer que iremos
        #   adicionar o tipo, senfo esse tipo dado pela entity2.
        # - se for membro, e a entity1 == obj, então quer dizer que iremos adicionar o tipo do objeto, que corresponde
        #   também à entity2
        # - adicionamos como sendo a sua ajuda à frequência relativa, de 1 unidade
        types = [(x.relation.entity2, 1) for x in self.declarations if (isinstance(x.relation, Association) and
                                                                   ((x.relation.cardin == 'one' and
                                                                     x.relation.default == obj))) or
                 (isinstance(x.relation, Member) and x.relation.entity1 == obj)]

        # no caso de uma associação em que a entity1 é == obj, e a sua cadinalidade é None, quer dizer, que é uma
        # associação entre objetos entity1 e entity2; pelo que guardando numa lista os nomes das associações, depois
        # usando a função getAssocTypes com os nomes das associações guardadas, conseguimos obter os tipos que faltam
        assoc_names_entity1 = list(set([x.relation.name for x in self.declarations
                                        if isinstance(x.relation, Association)
                                        and x.relation.cardin is None and x.relation.entity1 == obj ]))

        # caso seja a entity1 == obj, quer dizer que do resultado do getAssocTypes só  nos interessa o primeiro registo
        # do tuplo para type e a sua frequência relativa, sendo assim, o tuplo adicionado será x[0], x[2]
        for assoc_name in assoc_names_entity1:
            types += [(x[0], x[2]) for x in self.getAssocTypes(assoc_name)]

        # no caso de uma associação em que a entity2 é == obj, e a sua cadinalidade é None, quer dizer, que é uma
        # associação entre objetos entity1 e entity2; pelo que guardando numa lista os nomes das associações, depois
        # usando a função getAssocTypes com os nomes das associações guardadas, conseguimos obter os tipos que faltam
        assoc_names_entity2 = list(set([x.relation.name for x in self.declarations
                                        if isinstance(x.relation, Association)
                                        and x.relation.cardin is None
                                        and x.relation.entity2 == obj]))

        # caso seja a entity2 == obj, quer dizer que do resultado do getAssocTypes só nos interessa o segundo registo
        # do tuplo para type e a sua frequência relativa, sendo assim, o tuplo adicionado será x[1], x[2]
        for assoc_name in assoc_names_entity2:
            types += [(x[1], x[2]) for x in self.getAssocTypes(assoc_name)]

        # - de forma a eliminar as contribuições duplicadas e somar as frequências relativas dos duplicados, é necessário
        #   iterar sobre a lista type, criar um dicionário, e na iteração da lista type a parte [0] do tuplo fica como
        #   key do dicionário e o value como a soma das frequências relativas correspondentes.
        # - aproveita-se a iteração da lista de types para somar as frequências relativas
        result = {}
        total_freq = 0

        for x in types:
            if x[0] in result:
                result[x[0]] += x[1]
            else:
                result[x[0]] = x[1]
            total_freq += x[1]

        # no final, itera-se o dicionário e usando uma lista de compreensão, divide-se a parte [1] do tuplo pela soma
        # das frequências relativas obtidas
        return [(x[0], x[1]/total_freq) for x in result.items()]

    # Insere uma nova relação "rel" declarada por "user".
    # Se a relação for uma associação fluente entre objectos,
    # tem que fazer a gestão do intervalo de tempo
    # em que a associação se mantém verdadeira
    def insert2(self, user, rel):
        # se:
        # - a relation != Association, coloca-se diretamente na lista de declarações
        # - for Association e rel.fluent == True, também se coloca diretamente na lista de declarações
        if not isinstance(rel, Association) or rel.fluent is True:
            return self.insert(user, rel)

        # para o uso do parâmetro time, é necessário  existir uma declaração já declarada na lista de declarações
        # que seja do tipo entre tipos com fluent=True, e que o nome da relation seja igual ao rel.name, para ser uma
        # declaração entre tipos tem que ser diferente de None
        declaration_fluent = [dec.relation for dec in self.declarations if isinstance(dec.relation, Association) and
                              dec.relation.fluent is True and
                              dec.relation.name == rel.name and
                              dec.relation.cardin is not None and
                              dec.user == user]

        # caso não exista uma declaração, então não é possível usar o parâmetro time
        if len(declaration_fluent) == 0:
            return self.insert(user, rel)

        # simula a passagem do tempo
        self.tick += len(rel.name)

        # - agora vamos obter as declarações com relation.name == rel.name, e que tenham relation.fluent == False,
        #   e com as entitidades iguais, caso não exista, tem de ser inserido com time novo
        # - outra condição para fazer update ao tempo, no i2 é este ser igual a self.last_tick que corresponde
        #   ao tempo anterior em que foi alterado o time; não pode ser == self.tick - len(rel.name) porque temos de
        #   garantir que foi uma declaração declarada usando este método
        for i in range(0, len(self.declarations)):
            if isinstance(self.declarations[i].relation, Association) \
                    and self.declarations[i].relation.name == rel.name \
                    and self.declarations[i].relation.entity1 == rel.entity1 \
                    and self.declarations[i].relation.entity2 == rel.entity2 \
                    and self.declarations[i].relation.time[1] == self.last_tick:
                self.declarations[i].relation.time = (self.declarations[i].relation.time[0], self.tick)
                self.last_tick = self.tick
                return

        rel.time = (self.tick, self.tick)
        self.declarations.append(Declaration(user,rel))
        self.last_tick = self.tick


class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth',detect_repeated=False):
        SearchTree.__init__(self, problem, strategy, detect_repeated)
        self.optimizations = []

    def optimize(self, idx=0):
        # se idx é maior ou igual a length(self.solution) - 2 termina com return []
        if idx >= len(self.solution) - 2:
            return []

        # ver as possíveis ações para self.solution[idx] (ex: acção in Lisboa)
        actions = self.problem.domain.actions(self.solution[idx])

        # ex: Lisboa, Evora
        hop = self.solution[idx], self.solution[idx + 2]

        # se o salto existe nas acções possíveis então iremos apagar o idx + 1
        if hop in actions:
            self.optimizations += [hop]
            del self.solution[idx + 1]

            # chama de novo self.optimize()
            self.optimize()

        self.optimize(idx + 1)

        return self.solution
