#encoding: utf8

# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#


class Relation:
    def __init__(self,e1,name,e2):
        self.entity1 = e1
        self.name = name
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)
    def toTriple(self):
        return (self.entity1,self.name,self.entity2)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,name,e2,cardin=None,default=None,fluent=False):
        Relation.__init__(self,e1,name,e2)
        self.cardin = cardin
        self.default = default
        self.fluent = fluent
        self.time = None
    def __str__(self):
        default = ""
        time = ""
        if self.cardin==None:
            if self.time!=None:
                time = ","+str(self.time)
        elif self.default==None:
            default = "[=?]"
        else:
            default = "[=" + str(self.default) + "]"
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + default + time + ")"

#   Exemplos:
#   a = Association('socrates','professor','filosofia')
#   b = Association('mamifero','altura','number','one',1.2)
#   c = Association('mamifero','amigo','mamifero','many')


# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)

#   Exemplo:
#   s = Subtype('homem','mamifero')


# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')


# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+", "+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)


# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=[]):
        self.declarations = ldecl
        self.tick = 0
    def __str__(self):
        return my_list2string(self.declarations)
    def insert(self,user,relation):
        self.tick += len(relation.name) # simula a passagem do tempo
        self.declarations.append(Declaration(user,relation))
    def query_local(self,user=None,e1=None,rel=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))


# Funcao auxiliar para converter para cadeias de caracteres
# listas cujos elementos sejam convertiveis para
# cadeias de caracteres
def my_list2string(list):
   if list == []:
       return "[]"
   s = "[ " + str(list[0])
   for i in range(1,len(list)):
       s += ", " + str(list[i])
   return s + " ]"
    

