import unittest
from main import Talk, parse_talks, schedule_session

class SchedulerTest(unittest.TestCase):
    def test_parse_talks(self):
        talks = parse_talks("proposals.txt")
        self.assertTrue(any(t.title.startswith("Rails para") for t in talks))
        self.assertTrue(all(isinstance(t.duration, int) for t in talks))

    def test_schedule_session(self):
        talks = [Talk("Test Talk 1", "60min"), Talk("Test Talk 2", "45min"), Talk("Test Talk 3", "30min")]
        session, remaining = schedule_session(talks, 90)
        self.assertLessEqual(sum(t.duration for t in session), 90)

if __name__ == "__main__":
    unittest.main()
