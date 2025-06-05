from datetime import datetime, timedelta

#Transformar o texto em numero
def parse_duracao(duracao_str):
    return 5 if duracao_str == "lightning" else int(duracao_str)

def format_hora(hora):
    return hora.strftime("%H:%M")

def montar_agenda(palestras, hora_inicio):
    agenda = []
    hora_atual = hora_inicio
    for titulo, duracao_min, duracao_str in palestras:
        #Cria a linha do horário
        agenda.append(f"{format_hora(hora_atual)} {titulo} {duracao_str}")
        #Aumenta a hora
        hora_atual += timedelta(minutes=duracao_min)
    return agenda


def preencher_turno(palestras_disponiveis, tempo_disponivel):
    selecionadas = []
    restantes = palestras_disponiveis.copy()
    tempo_usado = 0

    for titulo, duracao_min, duracao_str in sorted(restantes, key=lambda x: -x[1]):
        if tempo_usado + duracao_min <= tempo_disponivel:
            selecionadas.append((titulo, duracao_min, duracao_str))
            tempo_usado += duracao_min
            restantes.remove((titulo, duracao_min, duracao_str))

    for titulo, duracao_min, duracao_str in sorted(restantes, key=lambda x: x[1]):
        if tempo_usado + duracao_min <= tempo_disponivel:
            selecionadas.append((titulo, duracao_min, duracao_str))
            tempo_usado += duracao_min
            restantes.remove((titulo, duracao_min, duracao_str))

    return selecionadas, restantes

# Carregar palestras
palestras = []
with open("proposals.txt", "r", encoding="utf-8") as file:
    for linha in file:
        linha = linha.strip()
        if linha.endswith("lightning"):
            titulo = linha.rsplit(" ", 1)[0]
            duracao_min = 5
            duracao_str = "lightning"
        else:
            titulo, duracao = linha.rsplit(" ", 1)
            duracao_min = int(duracao.replace("min", ""))
            duracao_str = f"{duracao_min}min"
        palestras.append((titulo, duracao_min, duracao_str))


lista_palestras = palestras 

# TRACK 1 - MANHÃ
track1_manha, restantes = preencher_turno(lista_palestras, 180)
# TRACK 2 - MANHÃ
track2_manha, restantes = preencher_turno(restantes, 180)
# TRACK 1 - TARDE
track1_tarde, restantes = preencher_turno(restantes, 240)
# TRACK 2 - TARDE
track2_tarde, restantes = preencher_turno(restantes, 240)

# Gerar agendas
agenda_track1_manha = montar_agenda(track1_manha, datetime.strptime("09:00", "%H:%M"))
agenda_track2_manha = montar_agenda(track2_manha, datetime.strptime("09:00", "%H:%M"))
agenda_track1_tarde = montar_agenda(track1_tarde, datetime.strptime("13:00", "%H:%M"))
agenda_track2_tarde = montar_agenda(track2_tarde, datetime.strptime("13:00", "%H:%M"))

# Exibir
def exibir_agenda(agenda):
    for linha in agenda:
        print(linha)

print("===== TRACK 1 =====")
exibir_agenda(agenda_track1_manha)
print("12:00 Almoço")
exibir_agenda(agenda_track1_tarde)
print("17:00 Evento de Networking")

print("\n===== TRACK 2 =====")
exibir_agenda(agenda_track2_manha)
print("12:00 Almoço")
exibir_agenda(agenda_track2_tarde)
print("17:00 Evento de Networking")
