import re
from datetime import datetime, timedelta

MORNING_START = datetime.strptime("09:00", "%H:%M")
AFTERNOON_START = datetime.strptime("13:00", "%H:%M")
LUNCH_TIME = "12:00 Almoço"
NETWORKING_EVENT = "Evento de Networking"
MORNING_DURATION = 180
AFTERNOON_MIN = 180
AFTERNOON_MAX = 240

def parse_line(line):
    match = re.match(r"(.+?)\s(\d+min|lightning)$", line)
    if not match:
        raise ValueError(f"Formato inválido: '{line}'")

    title, duration = match.groups()
    minutes = 5 if duration == "lightning" else int(duration.replace("min", ""))
    
    if minutes <= 0:
        raise ValueError(f"Duração inválida: '{line}' (tempo deve ser positivo)")
    if minutes > 240:
        raise ValueError(f"Duração muito longa (> 240min): '{line}'")

    return {"title": title.strip(), "duration": minutes}


def read_proposals(filename="proposals.txt"):
    talks = []
    seen_titles = set()

    try:
        with open(filename, encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    talk = parse_line(line)
                    if talk["title"] in seen_titles:
                        print(f"Linha {i}: palestra duplicada ignorada -> '{talk['title']}'")
                        continue
                    talks.append(talk)
                    seen_titles.add(talk["title"])
                except ValueError as ve:
                    print(f"Linha {i}: {ve}")
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado.")
        exit(1)

    return talks


def format_schedule(start_time, talks):
    result = []
    current_time = start_time

    for talk in talks:
        time_str = current_time.strftime("%H:%M")
        result.append(f"{time_str} {talk['title']} {talk['duration']}min")
        current_time += timedelta(minutes=talk['duration'])
    return result, current_time


def find_combinations(talks, target_time, allow_less=False):
    result = []
    def backtrack(start, path, total):
        if (not allow_less and total == target_time) or (allow_less and total >= target_time and total <= AFTERNOON_MAX):
            result.append(path[:])
            return
        if total > target_time or (allow_less and total > AFTERNOON_MAX):
            return

        for i in range(start, len(talks)):
            if talks[i] not in path:
                path.append(talks[i])
                backtrack(i + 1, path, total + talks[i]["duration"])
                path.pop()
    backtrack(0, [], 0)
    return result

def schedule_tracks(talks):
    talks_left = talks[:]
    tracks = []

    while talks_left:
        morning_options = find_combinations(talks_left, MORNING_DURATION)
        afternoon_options = find_combinations(talks_left, AFTERNOON_MIN, allow_less=True)

        if not morning_options or not afternoon_options:
            break

        morning = morning_options[0]
        remaining = [t for t in talks_left if t not in morning]
        afternoon_candidates = [a for a in afternoon_options if all(t in remaining for t in a)]

        if not afternoon_candidates:
            break

        afternoon = afternoon_candidates[0]

        for t in morning + afternoon:
            talks_left.remove(t)

        tracks.append({"morning": morning, "afternoon": afternoon})

    return tracks

def print_schedule(tracks):
    if not tracks:
        print("Nenhuma trilha pôde ser criada. Verifique se há palestras suficientes com durações válidas.")
        return

    for i, track in enumerate(tracks):
        print(f"Track {chr(ord('A') + i)}:")
        morning_schedule, _ = format_schedule(MORNING_START, track["morning"])
        for line in morning_schedule:
            print(line)
        print(LUNCH_TIME)
        afternoon_schedule, end_time = format_schedule(AFTERNOON_START, track["afternoon"])
        for line in afternoon_schedule:
            print(line)
        networking_time = max(end_time, datetime.strptime("16:00", "%H:%M"))
        print(f"{networking_time.strftime('%H:%M')} {NETWORKING_EVENT}\n")

if __name__ == "__main__":
    proposals = read_proposals()
    if not proposals:
        print("Nenhuma proposta de palestra válida foi encontrada.")
    else:
        scheduled_tracks = schedule_tracks(proposals)
        print_schedule(scheduled_tracks)
