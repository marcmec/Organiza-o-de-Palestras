class Palestra:
    def __init__(self, titulo, duracao):
        self.titulo = titulo
        self.duracao = duracao
    
    def __str__(self):
        return f"{self.titulo} {self.duracao_str()}"
    
    def duracao_str(self):
        return "lightning" if self.duracao == 5 else f"{self.duracao}min"

class Sessao:
    DURACAO_MANHA = 180
    DURACAO_TARDE = 240
    
    def __init__(self, periodo):
        self.periodo = periodo
        self.palestras = []
        self.tempo_total = 0
    
    @property
    def tempo_restante(self):
        max_duracao = self.DURACAO_MANHA if self.periodo == 'manhã' else self.DURACAO_TARDE
        return max_duracao - self.tempo_total
    
    def adicionar_palestra(self, palestra):
        if palestra.duracao <= self.tempo_restante:
            self.palestras.append(palestra)
            self.tempo_total += palestra.duracao
            return True
        return False
    
    def horarios_formatados(self):
        horarios = []
        hora_atual = 9 if self.periodo == 'manhã' else 13
        minuto_atual = 0
        
        for palestra in self.palestras:
            horario = f"{hora_atual:02d}:{minuto_atual:02d} {palestra}"
            horarios.append(horario)
            minuto_atual += palestra.duracao
            hora_atual += minuto_atual // 60
            minuto_atual %= 60
        
        return horarios

class Track:
    def __init__(self, nome):
        self.nome = nome
        self.sessao_manha = Sessao('manhã')
        self.sessao_tarde = Sessao('tarde')
    
    def adicionar_palestra(self, palestra):
        if self.sessao_manha.adicionar_palestra(palestra):
            return True
        return self.sessao_tarde.adicionar_palestra(palestra)
    
    def __str__(self):
        output = [f"{self.nome}:"]

        for horario in self.sessao_manha.horarios_formatados():
            output.append(horario)
            output.append("")
        
        output.append("12:00 Almoço")
        output.append("")
        
        for horario in self.sessao_tarde.horarios_formatados():
            output.append(horario)
            output.append("")
        
        output.append("17:00 Evento de Networking")
        
        return "\n".join(output)

def ler_palestras(arquivo):
    palestras = []
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue
                
                try:
                    if 'lightning' in linha:
                        titulo = linha.replace('lightning', '').strip()
                        duracao = 5
                    else:
                        partes = linha.rsplit(' ', 1)
                        titulo = partes[0]
                        duracao = int(partes[1].replace('min', ''))
                    
                    palestras.append(Palestra(titulo, duracao))
                except (ValueError, IndexError):
                    print(f"Formato inválido na linha: {linha}")
                    continue
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo}' não encontrado.")
        return []
    
    return sorted(palestras, key=lambda x: -x.duracao)

def organizar_conferencia(palestras):
    if not palestras:
        return []
    
    tracks = []
    palestras_restantes = palestras.copy()
    
    while palestras_restantes:
        track = Track(f"Track {chr(65 + len(tracks))}")
        
        i = 0
        while i < len(palestras_restantes):
            if track.adicionar_palestra(palestras_restantes[i]):
                palestras_restantes.pop(i)
            else:
                i += 1
        
        tracks.append(track)
    
    return tracks

def main():
    import sys
    arquivo = sys.argv[1] if len(sys.argv) > 1 else 'proposals.txt'
    palestras = ler_palestras(arquivo)
    
    if not palestras:
        print("Nenhuma palestra válida encontrada.")
        return
    
    tracks = organizar_conferencia(palestras)
    
    for track in tracks:
        print(track)
        print()

if __name__ == "__main__":
    main()