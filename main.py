from datetime import datetime, timedelta

def format_hora(hora):
    return hora.strftime("%H:%M")

def montar_agenda(palestras, inicio):
    agenda = []
    hora_atual = inicio
    for titulo, duracao, duracao_str in palestras:
        agenda.append(f"{format_hora(hora_atual)} {titulo} {duracao_str}")
        hora_atual += timedelta(minutes=duracao)
    return agenda

def preencher_turno(palestras, limite):
    selecionadas, restantes = [], palestras[:]
    tempo_total = 0

    # Tenta encaixar primeiro as maiores, depois as menores
    for ordem in [True, False]:
        for p in sorted(restantes, key=lambda x: x[1], reverse=ordem):
            if tempo_total + p[1] <= limite:
                selecionadas.append(p)
                tempo_total += p[1]
                restantes.remove(p)

    return selecionadas, restantes

def carregar_palestras(arquivo):
    palestras = []
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha.endswith("lightning"):
                titulo = linha.rsplit(" ", 1)[0]
                palestras.append((titulo, 5, "lightning"))
            else:
                titulo, duracao = linha.rsplit(" ", 1)
                minutos = int(duracao.replace("min", ""))
                palestras.append((titulo, minutos, f"{minutos}min"))
    return palestras

def exibir_agenda(titulo, manha, tarde):
    print(f"===== {titulo} =====")
    for linha in manha:
        print(linha)
    print("12:00 Almoço")
    for linha in tarde:
        print(linha)
    print("17:00 Evento de Networking\n")

# ===== Execução principal =====

palestras = carregar_palestras("proposals.txt")

turnos = [("09:00", 180), ("13:00", 240)]
tracks = [[], []]
sobras = palestras[:]

# Preencher os turnos (manhã e tarde) para as duas tracks
for i in range(2):  # Duas tracks
    for hora_str, limite in turnos:
        slot, sobras = preencher_turno(sobras, limite)
        tracks[i].append(montar_agenda(slot, datetime.strptime(hora_str, "%H:%M")))


for i, (manha, tarde) in enumerate(tracks, start=1):
    exibir_agenda(f"TRACK {i}", manha, tarde)
