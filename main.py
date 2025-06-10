import re
from typing import List, Dict, Tuple

class Palestra:
    def __init__(self, titulo: str, duracao: int):
        self.titulo = titulo
        self.duracao = duracao
    
    def __repr__(self):
        return f"{self.titulo} ({self.duracao}min)"

class Sessao:
    MANHA = "manhã"
    TARDE = "tarde"
    
    def __init__(self, tipo: str):
        self.tipo = tipo
        self.palestras: List[Palestra] = []
        self.tempo_total = 0
    
    def adicionar_palestra(self, palestra: Palestra) -> bool:
        """Tenta adicionar uma palestra à sessão, retorna True se bem-sucedido"""
        duracao_total = self.tempo_total + palestra.duracao
        limite = 180 if self.tipo == self.MANHA else 240  # 3h manhã, 4h tarde (até 17h)
        
        if duracao_total <= limite:
            self.palestras.append(palestra)
            self.tempo_total = duracao_total
            return True
        return False

class Track:
    def __init__(self, nome: str):
        self.nome = nome
        self.sessao_manha = Sessao(Sessao.MANHA)
        self.sessao_tarde = Sessao(Sessao.TARDE)
    
    def adicionar_palestra_manha(self, palestra: Palestra) -> bool:
        return self.sessao_manha.adicionar_palestra(palestra)
    
    def adicionar_palestra_tarde(self, palestra: Palestra) -> bool:
        return self.sessao_tarde.adicionar_palestra(palestra)
    
    def esta_completa(self) -> bool:
        """Verifica se ambas as sessões estão cheias (ou próximas disso)"""
        return (self.sessao_manha.tempo_total >= 180 and 
                self.sessao_tarde.tempo_total >= 180)  # Pelo menos 3h em cada

def parse_propostas(linhas: List[str]) -> List[Palestra]:
    """Converte as linhas de texto em objetos Palestra"""
    palestras = []
    padrao = re.compile(r'(.+)\s(\d+)min|(.+)\slightning')
    
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
        
        match = padrao.match(linha)
        if not match:
            continue
        
        if match.group(2):  # Tem duração em minutos
            titulo = match.group(1)
            duracao = int(match.group(2))
        else:  # lightning
            titulo = match.group(3)
            duracao = 5
        
        palestras.append(Palestra(titulo, duracao))
    
    return palestras

def organizar_palestras(palestras: List[Palestra]) -> List[Track]:
    """Organiza as palestras em tracks com sessões de manhã e tarde"""
    # Ordena as palestras por duração (maiores primeiro) para facilitar o empacotamento
    palestras_ordenadas = sorted(palestras, key=lambda x: x.duracao, reverse=True)
    
    tracks = []
    track_atual = Track(f"Track {len(tracks) + 1}")
    tracks.append(track_atual)
    
    for palestra in palestras_ordenadas:
        adicionada = False
        
        # Tenta adicionar em tracks existentes primeiro
        for track in tracks:
            # Tenta manhã primeiro
            if not track.sessao_manha.tempo_total >= 180:  # Se ainda tem espaço
                if track.adicionar_palestra_manha(palestra):
                    adicionada = True
                    break
            
            # Se não couber na manhã, tenta tarde
            if not track.sessao_tarde.tempo_total >= 240:  # Se ainda tem espaço
                if track.adicionar_palestra_tarde(palestra):
                    adicionada = True
                    break
        
        # Se não couber em nenhuma track existente, cria nova
        if not adicionada:
            nova_track = Track(f"Track {len(tracks) + 1}")
            tracks.append(nova_track)
            if not nova_track.adicionar_palestra_manha(palestra):
                nova_track.adicionar_palestra_tarde(palestra)
    
    return tracks

def formatar_horario(hora_inicio: int, minutos: int) -> str:
    """Formata o horário no formato HH:MM"""
    horas = hora_inicio + (minutos // 60)
    minutos = minutos % 60
    return f"{horas:02d}:{minutos:02d}"

def gerar_saida(tracks: List[Track]) -> str:
    """Gera a saída formatada conforme o exemplo"""
    saida = []
    
    for i, track in enumerate(tracks, 1):
        saida.append(f"Track {chr(64 + i)}:")
        
        # Sessão da manhã
        hora_atual = 9 * 60  # 9:00 em minutos
        for palestra in track.sessao_manha.palestras:
            saida.append(f"{formatar_horario(9, hora_atual - 9*60)} {palestra.titulo} {palestra.duracao}min")
            hora_atual += palestra.duracao
        
        saida.append("12:00 Almoço")
        
        # Sessão da tarde
        hora_atual = 13 * 60  # 13:00 em minutos
        for palestra in track.sessao_tarde.palestras:
            saida.append(f"{formatar_horario(13, hora_atual - 13*60)} {palestra.titulo} {palestra.duracao}min")
            hora_atual += palestra.duracao
        
        # Evento de networking entre 16h e 17h
        if hora_atual <= 16 * 60:
            networking_hora = "16:00"
        else:
            networking_hora = "17:00"
        
        saida.append(f"{networking_hora} Evento de Networking")
        saida.append("")  # Linha em branco entre tracks
    
    return "\n".join(saida)

def main(arquivo_entrada: str = "proposals2.txt"):
    # Lê o arquivo de entrada
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    # Processa as palestras
    palestras = parse_propostas(linhas)
    
    # Organiza em tracks
    tracks = organizar_palestras(palestras)
    
    # Gera a saída formatada
    saida = gerar_saida(tracks)
    print(saida)

if __name__ == "__main__":
    main()