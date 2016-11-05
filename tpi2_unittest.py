#encoding: utf8
import unittest
from tpi2 import *


class Tpi2Tests(unittest.TestCase):

    def setUp(self):
        self.z = MySemNet()

        if len(self.z.declarations) != 22:

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

        self.lobj = self.z.getObjects()
        self.assertEqual(len(self.z.declarations), 22)

    def test_getObjects(self):
        self.assertEqual(len(self.lobj), len(['filosofia', 1.2, 1.85, (0, 0), 'socrates', 80, 'platao', 'sofronisco', 'aristoteles', 'matematica']))

        for row in ['filosofia', 1.2, 1.85, (0, 0), 'socrates', 80, 'platao', 'sofronisco', 'aristoteles', 'matematica']:
            self.assertEqual(True, row in self.lobj)

    def test_getAssocTypes(self):
        self.assertEqual(self.z.getAssocTypes('altura'), [('mamifero', 'number', 1.0)])
        self.assertEqual(sorted(self.z.getAssocTypes('pulsacao')), sorted([('homem', 'numero', 0.5), ('homem', 'number', 0.5)]))

    def test_getObjectTypes(self):
        result = []

        for x in self.lobj:
            result += self.z.getObjectTypes(x)

        self.assertEqual(len(result), 9)

        for row in [('number', 1.0), ('number', 1.0), ('cell', 1.0), ('mamifero', 0.25), ('homem', 0.5), ('filosofo', 0.25), ('homem', 1.0), ('homem', 1.0), ('homem', 1.0)]:
            self.assertEqual(True, row in result)


if __name__ == '__main__':
    unittest.main()
