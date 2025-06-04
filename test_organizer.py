"""
testes unitários para o organizador de palestras
"""

import unittest
import tempfile
import os
from models import Talk, Session, Track
from organizer import ConferenceOrganizer


class TestTalk(unittest.TestCase):
    """testes para a classe talk"""
    
    def test_talk_creation(self):
        talk = Talk("Teste", 60)
        self.assertEqual(talk.title, "Teste")
        self.assertEqual(talk.duration, 60)


class TestSession(unittest.TestCase):
    """testes para a classe session"""
    
    def setUp(self):
        self.session = Session([], "09:00", 180)
    
    def test_empty_session_duration(self):
        self.assertEqual(self.session.get_total_duration(), 0)
    
    def test_add_talk_success(self):
        talk = Talk("Palestra teste", 60)
        result = self.session.add_talk(talk)
        self.assertTrue(result)
        self.assertEqual(len(self.session.talks), 1)
        self.assertEqual(self.session.get_total_duration(), 60)
    
    def test_add_talk_exceeds_limit(self):
        talk1 = Talk("Palestra 1", 120)
        talk2 = Talk("Palestra 2", 90)
        
        self.session.add_talk(talk1)
        result = self.session.add_talk(talk2)  # 120 + 90 = 210 > 180
        
        self.assertFalse(result)
        self.assertEqual(len(self.session.talks), 1)
    
    def test_can_add_talk(self):
        talk1 = Talk("Palestra 1", 120)
        talk2 = Talk("Palestra 2", 60)
        talk3 = Talk("Palestra 3", 30)
        
        self.assertTrue(self.session.can_add_talk(talk1))
        self.session.add_talk(talk1)
        
        self.assertTrue(self.session.can_add_talk(talk2))
        self.session.add_talk(talk2)
        
        self.assertFalse(self.session.can_add_talk(talk3))  # 120 + 60 + 30 = 210 > 180


class TestTrack(unittest.TestCase):
    """testes para a classe track"""
    
    def test_track_creation(self):
        track = Track()
        self.assertEqual(track.morning_session.start_time, "09:00")
        self.assertEqual(track.morning_session.max_duration, 180)
        self.assertEqual(track.afternoon_session.start_time, "13:00")
        self.assertEqual(track.afternoon_session.max_duration, 240)


class TestConferenceOrganizer(unittest.TestCase):
    """testes para a classe conferenceorganizer"""
    
    def setUp(self):
        self.organizer = ConferenceOrganizer()
    
    def test_parse_talks_regular(self):
        content = """Palestra teste 60min
Outra palestra 45min
Lightning talk lightning"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_filename = f.name
        
        try:
            talks = self.organizer.parse_talks(temp_filename)
            
            self.assertEqual(len(talks), 3)
            self.assertEqual(talks[0].title, "Palestra teste")
            self.assertEqual(talks[0].duration, 60)
            self.assertEqual(talks[1].title, "Outra palestra")
            self.assertEqual(talks[1].duration, 45)
            self.assertEqual(talks[2].title, "Lightning talk")
            self.assertEqual(talks[2].duration, 5)
        finally:
            os.unlink(temp_filename)
    
    def test_parse_talks_lightning(self):
        content = "Palestra rápida lightning"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_filename = f.name
        
        try:
            talks = self.organizer.parse_talks(temp_filename)
            self.assertEqual(len(talks), 1)
            self.assertEqual(talks[0].title, "Palestra rápida")
            self.assertEqual(talks[0].duration, 5)
        finally:
            os.unlink(temp_filename)
    
    def test_organize_tracks_basic(self):
        talks = [
            Talk("Palestra longa", 60),
            Talk("Palestra média", 45),
            Talk("Palestra curta", 30),
        ]
        
        tracks = self.organizer.organize_tracks(talks)
        
        self.assertGreater(len(tracks), 0)
        
        total_allocated = 0
        for track in tracks:
            total_allocated += len(track.morning_session.talks)
            total_allocated += len(track.afternoon_session.talks)
        
        self.assertEqual(total_allocated, len(talks))
    
    def test_format_output_basic(self):
        track = Track()
        track.morning_session.talks = [Talk("Teste manhã", 60)]
        track.afternoon_session.talks = [Talk("Teste tarde", 45)]
        
        output = self.organizer.format_output([track])
        
        self.assertIn("Track A:", output)
        self.assertIn("09:00 Teste manhã 60min", output)
        self.assertIn("12:00 Almoço", output)
        self.assertIn("13:00 Teste tarde 45min", output)
        self.assertIn("Evento de Networking", output)


class TestRequirements(unittest.TestCase):
    """testes específicos para validar os requisitos do problema"""
    
    def setUp(self):
        self.organizer = ConferenceOrganizer()
    
    def test_morning_session_duration_limit(self):
        """sessão manhã deve respeitar limite de 180 minutos (9h-12h)"""
        session = Session([], "09:00", 180)
        
        talks_180 = [Talk("Talk 1", 60), Talk("Talk 2", 60), Talk("Talk 3", 60)]
        for talk in talks_180:
            self.assertTrue(session.can_add_talk(talk))
            session.add_talk(talk)
        
        extra_talk = Talk("Extra", 30)
        self.assertFalse(session.can_add_talk(extra_talk))
    
    def test_afternoon_session_duration_limit(self):
        """sessão tarde deve respeitar limite de 240 minutos (13h-17h)"""
        session = Session([], "13:00", 240)
        
        talks_240 = [Talk("Talk 1", 60), Talk("Talk 2", 60), Talk("Talk 3", 60), Talk("Talk 4", 60)]
        for talk in talks_240:
            self.assertTrue(session.can_add_talk(talk))
            session.add_talk(talk)
        
        extra_talk = Talk("Extra", 30)
        self.assertFalse(session.can_add_talk(extra_talk))
    
    def test_lightning_talks_parsing(self):
        """lightning talks devem ser parseadas como 5 minutos"""
        content = "Rails para usuários de Django lightning"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(content)
            temp_filename = f.name
        
        try:
            talks = self.organizer.parse_talks(temp_filename)
            self.assertEqual(len(talks), 1)
            self.assertEqual(talks[0].duration, 5)
        finally:
            os.unlink(temp_filename)
    
    def test_networking_time_constraints(self):
        """evento de networking deve estar entre 16h e 17h"""
        track1 = Track()
        track1.afternoon_session.talks = [Talk("Curta", 30)]  # termina 13:30
        
        track2 = Track()
        track2.afternoon_session.talks = [
            Talk("Longa 1", 60),  # 13:00-14:00
            Talk("Longa 2", 60),  # 14:00-15:00  
            Talk("Longa 3", 60),  # 15:00-16:00
            Talk("Média", 45)     # 16:00-16:45
        ]
        
        output = self.organizer.format_output([track1, track2])
        
        lines = output.split('\n')
        networking_lines = [line for line in lines if 'Evento de Networking' in line]
        
        for line in networking_lines:
            time = line.split()[0]
            hour = int(time.split(':')[0])
            self.assertGreaterEqual(hour, 16)  # >= 16h
            self.assertLessEqual(hour, 17)     # <= 17h


if __name__ == '__main__':
    unittest.main()
