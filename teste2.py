import re

class Palestra:
    def __init__(self, titulo, duracao):
        self.titulo = titulo
        self.duracao = duracao
        self.usada = False

def ler_propostas(arquivo):
    palestras = []
    with open(arquivo, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            match = re.match(r"^(.*)\s(\d+min|lightning)$", linha)
            if not match:
                print(f"Linha ignorada (formato inválido): {linha}")
                continue
            titulo = match.group(1)
            duracao_str = match.group(2)
            duracao = 5 if duracao_str == "lightning" else int(duracao_str.replace("min", ""))
            palestras.append(Palestra(titulo, duracao))
    return palestras

def formatar_hora(total_minutos):
    h = total_minutos // 60
    m = total_minutos % 60
    return f"{h:02d}:{m:02d}"

def montar_sessao(palestras, min_tempo, max_tempo):
    melhor_sessao = []
    melhor_tempo = 0
    n = len(palestras)

    def backtrack(indice, sessao_atual, tempo_atual):
        nonlocal melhor_sessao, melhor_tempo
        if tempo_atual > max_tempo:
            return

        if tempo_atual >= min_tempo and tempo_atual > melhor_tempo:
            melhor_tempo = tempo_atual
            melhor_sessao = sessao_atual  # ERRO: Referência direta, melhor_sessao = sessao_atual[:], assim não estão apontando para o mesmo espaço na memoria

        if indice == n:
            return

        if palestras[indice].usada:
            backtrack(indice + 1, sessao_atual, tempo_atual)
        else:
            sessao_atual.append(indice)
            backtrack(indice + 1, sessao_atual, tempo_atual + palestras[indice].duracao)
            sessao_atual.pop()
            backtrack(indice + 1, sessao_atual, tempo_atual)

    backtrack(0, [], 0)

    for i in melhor_sessao:
        palestras[i].usada = True

    return melhor_sessao, melhor_tempo

def organizar_tracks(palestras):
    track_num = 1
    while any(not p.usada for p in palestras):
        print(f"Track {track_num}:")
        indices_manha, duracao_manha = montar_sessao(palestras, 180, 180)
        hora_atual = 9 * 60
        for i in indices_manha:
            print(f"{formatar_hora(hora_atual)} {palestras[i].titulo} {palestras[i].duracao}min")
            hora_atual += palestras[i].duracao
        print("12:00 Almoço")

        indices_tarde, duracao_tarde = montar_sessao(palestras, 180, 240)
        hora_atual = 13 * 60
        for i in indices_tarde:
            print(f"{formatar_hora(hora_atual)} {palestras[i].titulo} {palestras[i].duracao}min")
            hora_atual += palestras[i].duracao

        if hora_atual < 16 * 60:
            hora_atual = 16 * 60
        print(f"{formatar_hora(hora_atual)} Evento de Networking\n")
        track_num += 1

palestras = ler_propostas("proposals.txt")
if not palestras:
    print("nenhuma palestra carregada.")
else:
    organizar_tracks(palestras)
