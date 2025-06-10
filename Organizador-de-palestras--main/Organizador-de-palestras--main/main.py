from datetime import timedelta, datetime
import re

MANHA_LIMITE = 180  
TARDE_MIN = 180     
TARDE_MAX = 240     

class Palestra:
    def __init__(self, titulo, duracao):
        self.titulo = titulo
        self.duracao = duracao

    def __repr__(self):
        return f"{self.titulo} ({self.duracao}min)"

def parse_propostas(arquivo):
    palestras = []
    with open(arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            duracao = 5 if 'lightning' in linha.lower() else int(re.search(r'(\d+)', linha).group(1))
            titulo = re.sub(r'(\d+min|lightning)', '', linha).strip()
            palestras.append(Palestra(titulo, duracao))
    return palestras

def alocar_palestras(palestras):
    tracks = []
    palestras_restantes = palestras.copy()
    while palestras_restantes:
        manha, palestras_restantes = preencher_sessao(palestras_restantes, MANHA_LIMITE)
        tarde, novas_restantes = preencher_sessao(palestras_restantes, TARDE_MAX, TARDE_MIN)

        if not manha and not tarde:
            break
        tracks.append((manha, tarde))
        palestras_restantes = novas_restantes

    return tracks, palestras_restantes

def preencher_sessao(palestras, limite, minimo=0):
    from itertools import combinations

    for i in range(len(palestras), 0, -1):
        for combo in combinations(palestras, i):
            total = sum(p.duracao for p in combo)
            if minimo <= total <= limite:
                for p in combo:
                    palestras.remove(p)
                return list(combo), palestras
    return [], palestras

def imprimir_tracks(tracks):
    for i, (manha, tarde) in enumerate(tracks, 1):
        print(f"Faixa {chr(64+i)}:")
        hora = datetime.strptime("09:00", "%H:%M")
        for p in manha:
            print(f"{hora.strftime('%H:%M')} {p.titulo} {p.duracao}min")
            hora += timedelta(minutes=p.duracao)
        print("12:00 Almoço")
        hora = datetime.strptime("13:00", "%H:%M")
        for p in tarde:
            print(f"{hora.strftime('%H:%M')} {p.titulo} {p.duracao}min")
            hora += timedelta(minutes=p.duracao)
        hora = max(hora, datetime.strptime("16:00", "%H:%M"))
        print(f"{hora.strftime('%H:%M')} Evento de Networking\n")

if __name__ == "__main__":
    palestras = parse_propostas("propostas.txt")
    tracks, restantes = alocar_palestras(palestras)
    imprimir_tracks(tracks)

    if restantes:
        print("Palestras não alocadas:")
        for p in restantes:
            print(f"- {p.titulo} ({p.duracao}min)")
