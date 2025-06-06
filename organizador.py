import re
from datetime import datetime, timedelta

# --- CONSTANTES ---
MORNING_DURATION = 180
AFTERNOON_MIN = 180
AFTERNOON_MAX = 240

# --- Função para converter texto da palestra em minutos ---
def parse_talk(line):
    match = re.match(r"(.+?)\s(\d+min|relâmpago|lightning)$", line.strip(), re.IGNORECASE)
    if not match:
        raise ValueError(f"Linha inválida: {line}")
    
    title, duration = match.groups()
    duration = duration.lower()
    if duration in ["relâmpago", "lightning"]:
        minutes = 5
    else:
        minutes = int(duration.replace("min", ""))
    
    return {"title": title.strip(), "duration": minutes}

# --- Função para imprimir agenda formatada ---
def print_schedule(tracks):
    for i, track in enumerate(tracks, 1):
        print(f"\nDia {i}:")
        time = datetime.strptime("09:00", "%H:%M")
        for talk in track["morning"]:
            print(f"{time.strftime('%H:%M')} {talk['title']} {talk['duration']}min")
            time += timedelta(minutes=talk['duration'])
        print("12:00 Almoço")
        time = datetime.strptime("13:00", "%H:%M")
        for talk in track["afternoon"]:
            print(f"{time.strftime('%H:%M')} {talk['title']} {talk['duration']}min")
            time += timedelta(minutes=talk['duration'])
        networking = max(time, datetime.strptime("16:00", "%H:%M"))
        print(f"{networking.strftime('%H:%M')} Evento de Networking")

# --- Função principal para alocar palestras nas trilhas ---
def organize_talks(talks):
    talks = sorted(talks, key=lambda x: -x['duration'])  # maiores primeiro
    unallocated = talks[:]
    tracks = []

    while unallocated:
        track = {"morning": [], "afternoon": []}
        morning_time = MORNING_DURATION
        afternoon_time = AFTERNOON_MAX

        # Sessão da manhã
        allocated = []
        for talk in unallocated:
            if talk['duration'] <= morning_time:
                track["morning"].append(talk)
                morning_time -= talk['duration']
                allocated.append(talk)
        for a in allocated:
            unallocated.remove(a)

        # Sessão da tarde
        allocated = []
        for talk in unallocated:
            if talk['duration'] <= afternoon_time:
                track["afternoon"].append(talk)
                afternoon_time -= talk['duration']
                allocated.append(talk)
        for a in allocated:
            unallocated.remove(a)

        tracks.append(track)

    return tracks

# --- Execução principal ---
if __name__ == "__main__":
    try:
        filename = input("Digite o nome do arquivo .txt com as palestras: ").strip()
        with open(filename, encoding="utf-8") as f:
            talks = [parse_talk(line) for line in f if line.strip()]
        trilhas = organize_talks(talks)
        print_schedule(trilhas)
    except Exception as e:
        print("Erro:", e)
