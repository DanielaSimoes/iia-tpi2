#encoding: utf8
import unittest
from tpi2 import *


class Tpi2Tests(unittest.TestCase):
    def setUp(self):
        self.z = MySemNet()

        self.z.insert('descartes', Association('socrates', 'professor', 'filosofia'))
        self.z.insert('descartes', Subtype('mamifero', 'vertebrado'))
        self.z.insert('descartes', Subtype('homem', 'mamifero'))
        self.z.insert('descartes', Association('socrates', 'professor', 'matematica'))
        self.z.insert('descartes', Member('platao', 'homem'))
        self.z.insert('descartes', Association('platao', 'professor', 'filosofia'))
        self.z.insert('descartes', Association('socrates', 'peso', 80))
        self.z.insert('descartes', Member('socrates', 'homem'))
        self.z.insert('descartes', Member('aristoteles', 'homem'))
        self.z.insert('descartes', Association('mamifero', 'altura', 'number', 'one', 1.2))
        self.z.insert('descartes', Association('socrates', 'altura', 1.85))

        self.z.insert('darwin', Subtype('homem', 'mamifero'))
        self.z.insert('darwin', Subtype('mamifero', 'vertebrado'))
        self.z.insert('darwin', Association('homem', 'pulsacao', 'number', 'one'))
        self.z.insert('darwin', Association('homem', 'progenitor', 'homem', 'many'))

        self.z.insert('simao', Association('socrates', 'professor', 'matematica'))
        self.z.insert('simao', Association('platao', 'professor', 'filosofia'))
        self.z.insert('simao', Association('sofronisco', 'progenitor', 'socrates'))

        self.z.insert('simoes', Association('socrates', 'professor', 'matematica'))

        self.z.insert('damasio', Member('socrates', 'filosofo'))
        self.z.insert('damasio', Association('homem', 'pulsacao', 'numero', 'one'))

        self.z.insert('tracker', Association('agent', 'at', 'cell', 'one', (0, 0), True))

    def test_getObjects(self):
        lobj = self.z.getObjects()

        self.assertEqual(len(lobj), len(['filosofia', 1.2, 1.85, (0, 0), 'socrates', 80, 'platao', 'sofronisco', 'aristoteles', 'matematica']))

        for row in ['filosofia', 1.2, 1.85, (0, 0), 'socrates', 80, 'platao', 'sofronisco', 'aristoteles', 'matematica']:
            self.assertEqual(True, row in lobj)

    def test_getAssocTypes(self):
        self.assertEqual(self.z.getAssocTypes('altura'), [('mamifero', 'number', 1.0)])
        self.assertEqual(sorted(self.z.getAssocTypes('pulsacao')), sorted([('homem', 'numero', 0.5), ('homem', 'number', 0.5)]))

    def test_getObjectTypes(self):
        lobj = self.z.getObjects()

        result = []

        for x in lobj:
            result += self.z.getObjectTypes(x)

        self.assertEqual(len(result), len([('number', 1.0), ('number', 1.0), ('cell', 1.0), ('mamifero', 0.25), ('homem', 0.5), ('filosofo', 0.25), ('homem', 1.0), ('homem', 1.0), ('homem', 1.0)]))

        print(result)

        for row in [('number', 1.0), ('number', 1.0), ('cell', 1.0), ('mamifero', 0.25), ('homem', 0.5), ('filosofo', 0.25), ('homem', 1.0), ('homem', 1.0), ('homem', 1.0)]:
            self.assertEqual(True, row in result)

    def test_insert2(self):
        # z.insert2('tracker',Association('agent','at','cell','one',(0,0),True))
        for i in range(10):  # snake permanece numa celula durante algumas
            # iteracoes, e depois muda para outra
            cell = (1, 2) if i < 7 else (2, 3)
            self.z.insert2('tracker', Association('snake', 'at', cell))
        self.z.query_local(rel='at')
        self.z.show_query_result()

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
