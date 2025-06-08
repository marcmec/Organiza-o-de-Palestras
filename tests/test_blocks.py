import unittest
from scheduler import parse_line, allocate_block

class TestEventPlanner(unittest.TestCase):

    def test_parse_valid_talk(self):
        title, duration = parse_line("Nova palestra sensacional 45min")
        self.assertEqual(title, "Nova palestra sensacional")
        self.assertEqual(duration, 45)

    def test_parse_lightning(self):
        title, duration = parse_line("Palestra rápida lightning")
        self.assertEqual(duration, 5)

    def test_block_duration_limit(self):
        talks = [("A", 60), ("B", 60), ("C", 30), ("D", 60)]
        block, _ = allocate_block(talks, 180)
        self.assertLessEqual(sum(d for _, d in block), 180)

if __name__ == "__main__":
    unittest.main()
