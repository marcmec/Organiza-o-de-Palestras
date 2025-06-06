import unittest
from scheduler import parse_line, find_combinations, schedule_tracks

class TestScheduler(unittest.TestCase):

    def test_parse_line_valid(self):
        self.assertEqual(
            parse_line("Minha palestra legal 60min"),
            {"title": "Minha palestra legal", "duration": 60}
        )
        self.assertEqual(
            parse_line("Palestra relâmpago lightning"),
            {"title": "Palestra relâmpago", "duration": 5}
        )

    def test_parse_line_invalid(self):
        with self.assertRaises(ValueError):
            parse_line("Formato inválido")
        with self.assertRaises(ValueError):
            parse_line("Palestra 60 minutos")

    def test_find_combinations_exact(self):
        talks = [
            {"title": "Talk 1", "duration": 60},
            {"title": "Talk 2", "duration": 60},
            {"title": "Talk 3", "duration": 60},
            {"title": "Talk 4", "duration": 45}
        ]
        result = find_combinations(talks, 180)
        self.assertTrue(any(sum(t["duration"] for t in combo) == 180 for combo in result))

    def test_schedule_tracks_basic(self):
        talks = [
            {"title": f"Talk {i}", "duration": 60} for i in range(6)
        ] + [{"title": f"Talk {i+6}", "duration": 30} for i in range(4)]
        tracks = schedule_tracks(talks)
        self.assertGreaterEqual(len(tracks), 1)
        total_minutes = sum(t["duration"] for track in tracks for t in track["morning"] + track["afternoon"])
        self.assertLessEqual(total_minutes, sum(t["duration"] for t in talks))

if __name__ == "__main__":
    unittest.main()
