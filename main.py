class Palestra:
    def _init_(self, titulo, duracao):
        self.titulo, self.duracao = titulo, duracao

    def _str_(self):
        return f"{self.titulo} {'lightning' if self.duracao == 5 else f'{self.duracao}min'}"

class Slot:
    def _init_(self, tipo):
        self.tipo = tipo
        self.limite = 180 if tipo == 'manhã' else 240
        self.palestras = []

    def adicionar(self, palestra):
        if self.tempo_restante() >= palestra.duracao:
            self.palestras.append(palestra)
            return True
        return False

    def tempo_restante(self):
        return self.limite - sum(p.duracao for p in self.palestras)

    def horarios(self):
        h, m = (9, 0) if self.tipo == 'manhã' else (13, 0)
        agenda = []
        for p in self.palestras:
            agenda.append(f"{h:02d}:{m:02d} {p}")
            m += p.duracao
            h += m // 60
            m %= 60
        return agenda

class Track:
    def _init_(self, nome):
        self.nome = nome
        self.manha = Slot('manhã')
        self.tarde = Slot('tarde')

    def adicionar(self, palestra):
        return self.manha.adicionar(palestra) or self.tarde.adicionar(palestra)

    def _str_(self):
        linhas = [f"{self.nome}:"]
        linhas += self.manha.horarios()
        linhas.append("12:00 Almoço")
        linhas += self.tarde.horarios()
        linhas.append("17:00 Evento de Networking")
        return "\n".join(linhas)

def ler_palestras(arquivo):
    palestras = []
    try:
        with open(arquivo, encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if not linha: continue
                try:
                    if 'lightning' in linha:
                        titulo, duracao = linha.replace('lightning', '').strip(), 5
                    else:
                        titulo, t = linha.rsplit(' ', 1)
                        duracao = int(t.replace('min', ''))
                    palestras.append(Palestra(titulo, duracao))
                except: print(f"Linha inválida: {linha}")
    except FileNotFoundError:
        print(f"Arquivo '{arquivo}' não encontrado.")
    return sorted(palestras, key=lambda p: -p.duracao)

def organizar(palestras):
    tracks, restantes = [], palestras[:]
    while restantes:
        t = Track(f"Track {chr(65 + len(tracks))}")
        i = 0
        while i < len(restantes):
            if t.adicionar(restantes[i]): restantes.pop(i)
            else: i += 1
        tracks.append(t)
    return tracks

def main():
    import sys
    arquivo = sys.argv[1] if len(sys.argv) > 1 else 'proposals.txt'
    palestras = ler_palestras(arquivo)
    if not palestras:
        print("Nenhuma palestra válida encontrada.")
        return
    for t in organizar(palestras):
        print(t, "\n")

if _name_ == "_main_":
    main()
