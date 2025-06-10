def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    palestras = {}
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
        if linha.endswith("lightning"):
            duracao = 5
            nome = linha[:-len("lightning")].strip()
        else:
            partes = linha.rsplit(' ', 1)
            nome = partes[0]
            duracao = int(partes[1].replace("min", ""))
        palestras[nome] = duracao
    return palestras


def gerar_combinacoes(lista, alvo_min, alvo_max=None):
    if alvo_max is None:
        alvo_max = alvo_min

    n = len(lista)
    resultados = []

    def buscar_combinacao(indice, atual, soma):
        if alvo_min <= soma <= alvo_max:
            resultados.append(list(atual))
        if soma >= alvo_max or indice >= n:
            return

        for i in range(indice, n):
            atual.append(lista[i])
            buscar_combinacao(i + 1, atual, soma + lista[i][1])
            atual.pop()

    buscar_combinacao(0, [], 0)
    return resultados


def imprimir_sessao(palestras, inicio_hora):
    hora = inicio_hora
    minuto = 0
    for nome, duracao in palestras:
        print(f"{hora:02d}:{minuto:02d} {nome} {duracao}min")
        minuto += duracao
        if minuto >= 60:
            hora += minuto // 60
            minuto = minuto % 60
    return hora, minuto


def organizar_tracks(palestras_dict):
    palestras = list(palestras_dict.items())
    tracks = []
    usadas = set()

    while True:
        disponiveis = [p for p in palestras if p[0] not in usadas]

        if not disponiveis:
            break

        combinacoes_manha = gerar_combinacoes(disponiveis, 180)
        if not combinacoes_manha:
            break

        combinacoes_manha.sort(key=lambda x: -len(x))
        manha = combinacoes_manha[0]
        usadas.update([p[0] for p in manha])

        disponiveis = [p for p in palestras if p[0] not in usadas]

        combinacoes_tarde = gerar_combinacoes(disponiveis, 180, 240)
        if combinacoes_tarde:
            combinacoes_tarde.sort(key=lambda x: -sum(p[1] for p in x))
            tarde = combinacoes_tarde[0]
            usadas.update([p[0] for p in tarde])
        else:
            tarde = []

        tracks.append((manha, tarde))

    return tracks


def main():
    palestras_dict = ler_arquivo("proposals.txt")
    tracks = organizar_tracks(palestras_dict)

    for i, (manha, tarde) in enumerate(tracks):
        print(f"\nTrack {chr(ord('A') + i)}:")
        imprimir_sessao(manha, 9)
        print("12:00 Almoço")
        hora_final, minuto_final = imprimir_sessao(tarde, 13)
        if hora_final < 16:
            hora_final = 16
            minuto_final = 0
        elif hora_final == 16 and minuto_final > 0:
            minuto_final = 0
        print(f"{hora_final:02d}:{minuto_final:02d} Evento de Networking")


if __name__ == "__main__":
    main()
