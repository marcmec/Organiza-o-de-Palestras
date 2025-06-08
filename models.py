from dataclasses import dataclass
from typing import List

@dataclass
class Talk:
    """ PALESTRA INDIVIDUAL """
    title: str
    duration: int  # em minutos

@dataclass
class Session:
    """ SESSÃO DE PALESTRAS (Manhã - Tarde) """
    talks: List[Talk]
    start_time: str  # HH:MM
    max_duration: int  # em minutos

    def get_total_duration(self) -> int:
        return sum(talk.duration for talk in self.talks)

    def can_add_talk(self, talk: Talk) -> bool:
        new_total = self.get_total_duration() + talk.duration
        if self.start_time == "13:00":
            return new_total <= 240  # 4 horas máximo
        return new_total <= self.max_duration

    def add_talk(self, talk: Talk) -> bool:
        if self.can_add_talk(talk):
            self.talks.append(talk)
            return True
        return False

class Track:
    """ TRACK COMPLETA (SESSÃO MANHÃ + TARDE) """
    def __init__(self):
        self.morning_session = Session([], "09:00", 180)  # 180min = limite de 3 horas
        self.afternoon_session = Session([], "13:00", 240)  # 240min = limite de 4 horas
