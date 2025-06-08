"""
Organizador de palestras para conferência.

"""

from typing import List
from models import Talk, Track


class ConferenceOrganizer:
    """ ORGANIZA PALESTRAS EM TRACKS """
    
    def parse_talks(self, filename: str) -> List[Talk]:
        """
        Lê arquivo de propostas e converte em lista de palestras.
        
        Args:
            filename: Nome do arquivo com as propostas
            
        Retorna:
            Lista de objetos Talk
            
        Erros:
            FileNotFoundError: Se o arquivo não for encontrado
        """
        talks = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                # Verificar se é lightning (5 minutos)
                if line.endswith('lightning'):
                    title = line.replace(' lightning', '').strip()
                    duration = 5
                else:
                    # Extrair duração em minutos
                    parts = line.rsplit(' ', 1)
                    if len(parts) == 2 and parts[1].endswith('min'):
                        title = parts[0].strip()
                        duration = int(parts[1].replace('min', ''))
                    else:
                        continue  # Linha inválida
                
                talks.append(Talk(title=title, duration=duration))
        
        return talks
    
    def organize_tracks(self, talks: List[Talk]) -> List[Track]:
        """
        Organiza palestras em tracks usando algoritmo guloso.
        
        Args:
            talks: Lista de palestras a serem organizadas
            
        Returns:
            Lista de tracks organizadas
        """
        # Ordenação decrescente
        sorted_talks = sorted(talks, key=lambda t: t.duration, reverse=True)
        tracks = []
        remaining_talks = sorted_talks.copy()
        
        while remaining_talks:
            track = Track()
            talks_to_remove = []
            
            # preencher sessão da manhã
            for talk in remaining_talks:
                if track.morning_session.can_add_talk(talk):
                    track.morning_session.add_talk(talk)
                    talks_to_remove.append(talk)
            
            # deleta palestras já alocadas
            for talk in talks_to_remove:
                remaining_talks.remove(talk)
            
            talks_to_remove = []
            
            # preencher sessão da tarde
            for talk in remaining_talks:
                if track.afternoon_session.can_add_talk(talk):
                    track.afternoon_session.add_talk(talk)
                    talks_to_remove.append(talk)
            
            # deleta palestras já alocadas
            for talk in talks_to_remove:
                remaining_talks.remove(talk)
            
            tracks.append(track)
            
            # break loop infinito
            if not talks_to_remove and remaining_talks:
                break
                
        return tracks
    
    def format_output(self, tracks: List[Track]) -> str:
        """
        Formata a saída das tracks no formato especificado.
        
        Args:
            tracks: Lista de tracks organizadas
            
        Returns:
            String formatada com a programação completa
        """
        output = []
        
        for i, track in enumerate(tracks):
            track_name = f"Track {chr(65+i)}:"  # A, B, C, etc.
            output.append(track_name)
            
            # formatar sessão da manhã
            current_time = "09:00"
            for talk in track.morning_session.talks:
                duration_text = "lightning" if talk.duration == 5 else f"{talk.duration}min"
                output.append(f"{current_time} {talk.title} {duration_text}")
                
                # próximo horário
                current_time = self._calculate_next_time(current_time, talk.duration)
            
            output.append("12:00 Almoço")
            
            # formatar sessão da tarde
            current_time = "13:00"
            for talk in track.afternoon_session.talks:
                duration_text = "lightning" if talk.duration == 5 else f"{talk.duration}min"
                output.append(f"{current_time} {talk.title} {duration_text}")
                
                # próximo horário
                current_time = self._calculate_next_time(current_time, talk.duration)
            
            # horário do networking
            networking_time = self._calculate_networking_time(current_time)
            output.append(f"{networking_time} Evento de Networking")
            
            if i < len(tracks) - 1:  # espaço entre tracks
                output.append("")
        
        return "\n".join(output)
    
    def _calculate_next_time(self, current_time: str, duration: int) -> str:
        """
        Calcula o próximo horário após adicionar duração.
        
        Args:
            current_time: Horário atual no formato "HH:MM"
            duration: Duração em minutos a ser adicionada
            
        Returns:
            Novo horário no formato "HH:MM"
        """
        hour, minute = map(int, current_time.split(':'))
        total_minutes = hour * 60 + minute + duration
        new_hour = total_minutes // 60
        new_minute = total_minutes % 60
        return f"{new_hour:02d}:{new_minute:02d}"
    
    def _calculate_networking_time(self, end_time: str) -> str:
        """
        Calcula o horário do networking respeitando a regra 16h-17h.
        
        Args:
            end_time: Horário de término das palestras da tarde
            
        Returns:
            Horário do networking no formato "HH:MM"
        """
        hour, minute = map(int, end_time.split(':'))
        current_minutes = hour * 60 + minute
        
        # terminou antes das 16h, networking às 16h
        if current_minutes < 16 * 60:
            return "16:00"
        # terminou depois das 17h, networking às 17h
        elif current_minutes > 17 * 60:
            return "17:00"
        else:
            return end_time

if __name__ == "__main__":
    organizer = ConferenceOrganizer()
    
    try:
        talks = organizer.parse_talks("proposals.txt")  
        tracks = organizer.organize_tracks(talks)
        output = organizer.format_output(tracks)
        print(output)
    except FileNotFoundError:
        print("Arquivo 'proposals.txt' não encontrado.")
