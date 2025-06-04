"""
Modelos de dados para o organizador de palestras.

"""

from dataclasses import dataclass
from typing import List


@dataclass
class Talk:
    """
    Representa uma palestra individual.
    
    Attributes:
        title: O título da palestra
        duration: A duração em minutos (5 para lightning talks)
    """
    title: str
    duration: int  # em minutos


@dataclass 
class Session:
    """
    Representa uma sessão de palestras (manhã ou tarde).
    
    Attributes:
        talks: Lista de palestras na sessão
        start_time: Horário de início (formato "HH:MM")
        max_duration: Duração máxima permitida em minutos
    """
    talks: List[Talk]
    start_time: str
    max_duration: int
    
    def get_total_duration(self) -> int:
        """Retorna a duração total das palestras na sessão"""
        return sum(talk.duration for talk in self.talks)
    
    def can_add_talk(self, talk: Talk) -> bool:
        """Verifica se uma palestra pode ser adicionada na sessão"""
        new_total = self.get_total_duration() + talk.duration
        
        # Para sessão da tarde, garantir que seja antes das 17h
        if self.start_time == "13:00":
            # 13:00 + new_total não pode ultrapassar 17:00 (240 minutos)
            return new_total <= 240  # 4 horas máximo
        
        return new_total <= self.max_duration
    
    def add_talk(self, talk: Talk) -> bool:
        """Adiciona uma palestra na sessão se possível"""
        if self.can_add_talk(talk):
            self.talks.append(talk)
            return True
        return False


class Track:
    """
    Representa uma track completa com sessão da manhã e da tarde.
    
    Uma track é composta por:
    - Sessão manhã: 9h-12h (180 minutos)
    - Almoço: 12h-13h
    - Sessão tarde: 13h-17h (240 minutos máximo)
    - Networking: 16h-17h
    """
    def __init__(self):
        self.morning_session = Session([], "09:00", 180)  # 9h-12h = 180min
        # tarde: 13h-17h = 240min máximo, networking entre 16h-17h
        self.afternoon_session = Session([], "13:00", 240)  # 240min = limite 
