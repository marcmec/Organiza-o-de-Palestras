import unittest
from ME import ler_palestras, agendar_trilhas

class TesteME(unittest.TestCase):
    def testar_total_palestras(self):
        palestras = ler_palestras("proposals.txt")
        self.assertEqual(len(palestras), 19)

    def testar_trilhas_geradas(self):
        palestras = ler_palestras("proposals.txt")
        trilhas = agendar_trilhas(palestras)
        self.assertTrue(len(trilhas) >= 2)

    def testar_todas_palestras_agendadas(self):
        palestras = ler_palestras("proposals.txt")
        trilhas = agendar_trilhas(palestras.copy())
        total_agendadas = sum(len(m) + len(t) for _, m, t in trilhas)
        self.assertEqual(total_agendadas, 19)

if __name__ == "__main__":
    unittest.main()
